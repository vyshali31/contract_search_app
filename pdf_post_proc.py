import numpy as np
import unidecode
from copy import deepcopy
import json


def convert_to_chunk_list(azure_output, lang="eng"):
    """
    Function that converts form recogonized output
    chunk list.

    Args:
        :azure_output: Ms form recognized response in dictionary
        :lang: processed document language

    Returns:
         chunk list
    """
    chunk_list = list()
    chunk_list_page = list()
    chunk_list_aux = list()

    az_pages = azure_output['pages']
    az_styles = azure_output['styles']


    # borrar este if o poner mas if paragraph, selection box, word, table
    if 'pages' in azure_output:
        for page_idx, page in enumerate(azure_output['pages']):
            chunk_list_page = list()
            # get unit inch pixel
            unit = page['unit']
            
            # transform word
            new_words = transform_words(page['words'], unit)
            
            # get shape
            height = convert_unit_to_pixel(page['height'], unit)
            width = convert_unit_to_pixel(page['width'], unit)
            # paragraph and selection mark
            chunk_list_aux = convert_to_chunk_list_page(azure_output, [height, width], 0, page_idx, unit, new_words,
                                                        lang)
            chunk_list_page = chunk_list_page + chunk_list_aux
            # table
            chunk_list_aux = list()
            for table_idx, table in enumerate(azure_output['tables']):
                if page_idx == table['bounding_regions'][0]['page_number'] - 1:
                    if chunk_list_page != []:
                        last_id = chunk_list_page[-1]['id']
                        chunk_list_aux = generate_FR_chunk_table(table, [height, width], last_id, table_idx, unit,
                                                                   new_words, lang)
                        chunk_list_page = delete_duplicate(chunk_list_page, chunk_list_aux)

                    else:
                        last_id = -1
                        chunk_list_aux = generate_FR_chunk_table(table, [height, width], last_id, table_idx, unit,
                                                                   new_words, lang)
                        chunk_list_page = delete_duplicate(chunk_list_page, chunk_list_aux)

            chunk_list.append(chunk_list_page)

    return chunk_list


def delete_duplicate(list_chunk, list_table_aux):
    new_list = list()

    if list_chunk != []:

        for idx, chunk in enumerate(list_chunk):
            if len(list_table_aux) == 0:
                new_list = new_list + list_chunk[idx:]
                return new_list
                # new_list.append(chunk)
            else:
                list_aux, idx2 = sort_list(chunk, list_table_aux)
                if len(list_aux) != 0:
                    new_list = new_list + list_aux
                    list_table_aux.pop(idx2)
                else:
                    new_list.append(chunk)

    elif list_chunk == []:

        new_list = list_table_aux

    return new_list


def sort_list(chunk, list_table):
    new_list = list()
    for idx2, chunk2 in enumerate(list_table):
        if chunk['bounding_box'] == chunk2['bounding_box']:
            chunk2['id'] = chunk['id']
            new_list.append(chunk2)
            return new_list, idx2
    return list(), -1


def convert_to_chunk_list_page(azure_output, shape, id_chunk, page_number, unit, new_words, lang):
    """
    Function that converts azure text recognizer output
    chunk list.

    Args:
        :azure_output: Ms form recognizer response
        :shape: Image shape of page. (height, width)
        :page_number: Processed number page
        :unit: 
        :new_words: list of all the words page with your confidence
        :lang: processed document language

    Returns:
        chunk list
    """
    # Normaly only 1 bounding box
    sub_bounding = 0
    chunk_list = list()
    if 'paragraphs' in azure_output:
        az_chunk_list = azure_output['paragraphs']
        for idx, az_chunk in enumerate(az_chunk_list):
            if page_number == az_chunk['bounding_regions'][0]['page_number'] - 1:
                az_chunk['bounding_regions'][sub_bounding]['polygon'] = convert_polygon(
                    az_chunk['bounding_regions'][sub_bounding]['polygon'], unit)
                FR_chunk = generate_FR_chunk_paragraphs(az_chunk, shape, id_chunk, page_number, new_words, lang)
                chunk_list.append(FR_chunk)
                id_chunk = id_chunk + 1
        az_chunk_list = azure_output['pages'][page_number]['selection_marks']
        for idx_2, az_chunk in enumerate(az_chunk_list):
            az_chunk['polygon'] = convert_polygon(az_chunk['polygon'], unit)
            FR_chunk = generate_FR_chunk_selection_marks(az_chunk, shape, id_chunk, page_number, lang)
            chunk_list.append(FR_chunk)
            id_chunk = id_chunk + 1
    return chunk_list


def generate_FR_chunk_paragraphs(chunk, img_shape, count, page_number, new_words, lang):
    """
    Generates the structure of a chunk for paragraphs.

    Args:
        :chunk: Chunk with another format to be converted.
        :img_shape: Image shape of page. (height, width)
        :count: Counter to assign sequential ids.
        :page_number: Page of the original document that corresponds to the
            image.
        :new_words: list of all the words page with your confidence
        :lang: processed document language
    Returns:
        :new_chunk: Chunk with the updated format.

    """
    coords = chunk['bounding_regions'][0]['polygon']
    #   0  3
    #   1  2 
    x1 = coords[0]['x']
    y1 = coords[0]['y']
    x2 = coords[2]['x']
    y2 = coords[2]['y']
    list_polygon = list()
    for coord in coords:
        list_polygon.append(coord['x'])
        list_polygon.append(coord['y'])
    words = search_for_words_in_paragraph(new_words, list_polygon)

    if words is None or len(words) == 0:
        words = []

    new_chunk = {
        'id': count,
        'page': page_number,
        'bounding_box': list_polygon,
        'rectangle': {'left': x1,
                      'top': y1,
                      'right': x2,
                      'bottom': y2},
        'chunk_text': {
            lang: {
                'text': chunk['content'],
            }
        },
        'words': words
    }

    return new_chunk


def generate_FR_chunk_selection_marks(chunk, img_shape, count, page_number, lang):
    """
    Generates the structure of a chunk for checkbox/selection_marks.

    Args:
        :chunk: Chunk with another format to be converted.
        :img_shape: shape of page. (height, width)
        :count: Counter to assign sequential ids.
        :page_number: Page of the original document that corresponds to the
            image.
    Returns:
        :new_chunk: Chunk with the updated format.

    """

    coords = chunk['polygon']
    #   0  3
    #   1  2 
    x1 = coords[0]['x']
    y1 = coords[0]['y']
    x2 = coords[2]['x']
    y2 = coords[2]['y']
    chunk_confidence = int(chunk['confidence'])
    list_polygon = list()
    for coord in chunk['polygon']:
        list_polygon.append(coord['x'])
        list_polygon.append(coord['y'])
    new_chunk = {
        'id': count,
        'page': page_number,
        'bounding_box': list_polygon,
        'rectangle': {'left': x1,
                      'top': y1,
                      'right': x2,
                      'bottom': y2},
        'chunk_text': {
            lang: {
                'text': chunk['state'],
            }
        },
        'span': chunk['span'],
        'words': []
    }

    return new_chunk


def generate_FR_chunk_cell(chunk, img_shape, count, num_table, new_words, lang):
    """
    Generates the structure of a chunk for cell of table.

    Args:
        :chunk: Chunk with another format to be converted.
        :img_shape: shape of page. (height, width)
        :count: Counter to assign sequential ids.
        :num_table: Counter to assign sequential ids of table.
        :page_number: Page of the original document that corresponds to the
            image.
        :new_words: list of all the words page with your confidence
        :lang: processed document language
    Returns:
        :new_chunk: Chunk with the updated format.

    """
    coords = chunk['bounding_regions'][0]['polygon']
    #   0,1  6,7
    #   2,3  4,5 
    x1 = coords[0]['x']
    y1 = coords[0]['y']
    x2 = coords[2]['x']
    y2 = coords[2]['y']
    list_polygon = list()
    words = []
    for coord in coords:
        list_polygon.append(coord['x'])
        list_polygon.append(coord['y'])

    words = search_for_words_in_paragraph(new_words, list_polygon)
    
    if words is None:
        words = []
    
    new_chunk = {
        'id': count,
        'page': chunk['bounding_regions'][0]['page_number'] - 1,
        'bounding_box': list_polygon,
        'rectangle': {'left': x1,
                      'top': y1,
                      'right': x2,
                      'bottom': y2},
        'chunk_text': {
            lang: {
                'text': chunk['content'],
            }
        },
        'words': words
    }

    return new_chunk


def generate_FR_chunk_table(table, img_shape, count, num_table, unit_type, new_words, lang):
    """
    Function that iterates through all the cells in a table 

    Args:
        :chunk: Chunk with another format to be converted.
        :img_shape: shape of page. (height, width)
        :count: Counter to assign sequential ids.
        :num_table: Counter to assign sequential ids of table.
        :unit_type: the unit of measurements in the table
        :new_words: list of all the words page with your confidence
        :lang: processed document language
    Returns:
        :new_chunk: Chunk with the updated format.

    """
    list_cell = list()
    for cell_idx, cell in enumerate(table['cells']):
        cell['bounding_regions'][0]['polygon'] = convert_polygon(cell['bounding_regions'][0]['polygon'], unit_type)
        list_cell.append(generate_FR_chunk_cell(cell, img_shape, count + cell_idx + 1, num_table, new_words, lang))
    return list_cell



def clean_text(text):
    text = unidecode.unidecode(text)
    return str(text)


def search_for_words_in_paragraph(words, bounding):
    """
    Function search for list words in the area
    Args:
        :words: list of word 
        :bounding: area that must contains a words
    Returns:
        :word_list: return list of words found in the area
    """
    
    word_list = list()
    word_count = 0
    for word in words:
        if is_boxA_in_boxB(word['bounding_box'], bounding):
            word_count = word_count + 1
            word_obj = {
                "xmin": word['bounding_box'][0],
                "ymin": word['bounding_box'][1],
                "xmax": word['bounding_box'][4],
                "ymax": word['bounding_box'][5],
                "text": clean_text(word['content']),
                "word_no": word_count,
            }
            word_list.append(word_obj)
    return word_list


def is_boxA_in_boxB(a: list(), b: list):
    """
    This function checks if the box represented by coordinates in list (or numpy array) a is inside box b
    The order of coordinates in list is: topleft X, topleft Y, topright X, topright Y, bottomright X, bottomright Y, bottomleft X, bottomleft Y.
    a, b: list or numpy array containing x and y coordinates 
    return: boolean
    """
    a = np.array(a)
    b = np.array(b)
    relaxation = 2
    asmaller = sum(b[[0, 1, 3, 6]] - a[[0, 1, 3, 6]] <= [relaxation, relaxation, relaxation, relaxation])
    bsmaller = sum(a[[2, 4, 5, 7]] - b[[2, 4, 5, 7]] <= [relaxation, relaxation, relaxation, relaxation])
    return asmaller + bsmaller == 8


def transform_words(words, type_unit):
    """
    Transform list word value in pixel
    Args:
        :words: list of words
        :type_unit: unit that can transform
    Returns:
        :new_words: return list tht value in pixel
    """
    new_words = list()
    for word in words:
        list_polygon = list()
        coords = convert_polygon(word['polygon'], type_unit)
        for coord in coords:
            list_polygon.append(coord['x'])
            list_polygon.append(coord['y'])
        word['bounding_box'] = list_polygon
        new_words.append(word)
    return new_words


def convert_polygon(polygon, type_unit: str):
    """
    Functions transform polygon in pixel 
    Args:
        :polygon: 
        :type_unit: unit that can transform
    Returns:
        :polygon: return polygon in pixel
    """
    aux = deepcopy(polygon)
    for vertex in aux:
        vertex['x'] = convert_unit_to_pixel(vertex['x'],type_unit)
        vertex['y'] = convert_unit_to_pixel(vertex['y'],type_unit)
    return aux


def convert_inch_to_pixel(unit: int):
    """
    Functions that transform value in inch
    Args:
        :unit: value in pixel to transform 
    Returns:
        :value: return unit in pixel
    """
    
    return round(unit * 72)


def convert_unit_to_pixel(unit: int, type_unit: str):
    """
    Functions transform to pixel to other unit
    Args:
        :unit: value in pixel to transform 
        :type _unit: unit that can transform
    Returns:
        :value: return value in unit 
    """
    if "inch" in type_unit:
        return convert_inch_to_pixel(unit)
    elif "pixel" in type_unit:
        return unit
    else:
        print(f'Warning. Unit dont have model. It\'s a default a pixel')
        return unit
