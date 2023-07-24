import logging

import numpy as np


def check_arrays_have_same_shape(list_of_arrays: list) -> bool:
    '''Check if all arrays in provided list have the same length.'''
    if check_arrays_are_ndarrays(list_of_arrays):
        shape_to_check_against = list_of_arrays[0].shape

        list_of_shapes = [array.shape for array in list_of_arrays if array.shape != shape_to_check_against]
        if len(list_of_shapes) == 0:
            logging.debug("All input arrays are the same length")
            return True
    
        logging.error("Arrays are not all of same length")
        return False

def check_arrays_are_ndarrays(list_of_potential_arrays: list) -> bool:
    '''Check if all arrays in provided list are of the type np.ndarray, to catch errors before calling .shape'''
    for array in list_of_potential_arrays:
        if not isinstance(array, np.ndarray):
            logging.error(f"{array} must be of type np.ndarray")
            return False
    
    logging.debug("All arrays are np.ndarray type")
    return True


def pad_array(array):
    '''Duplicates the first item of an array to preserve array size while differentiating.'''
    padded_array = array.copy()

    return np.insert(padded_array,0,array[0])