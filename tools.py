import numpy as np
import string
import json


class NotValidValue(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


def lookup_in_alphabet(char: str, reverse: bool = False) -> object:
    ''' Function generate alphabet, looking here for char and return digit for it,
        if reverse is True then function looking here for digit and returns char.
    '''
    if reverse:
        alphabet = dict(enumerate(string.ascii_letters + string.digits + string.punctuation + ' '))
    else:
        alphabet = {v:k for k,v in dict(enumerate(string.ascii_letters + string.digits + string.punctuation + ' ')).items()}
    return alphabet[char] if not reverse else alphabet[char % len(alphabet)]


def inverse_matrix(matrix: 'Matrix') -> 'Matrix':
    ''' Function is calculating and returns invert matrix. '''
    return np.linalg.inv(matrix)


def determinant_of_matrix(matrix: 'Matrix') -> int:
    ''' Function is calculating and returns determinant of matrix. '''
    # np.linalg.det returns float number for integer matrix,
    # therefore needs round value and convert in int, because float again
    return int(round(np.linalg.det(matrix)))


def sum_matrices(matrix_A: 'Matrix', matrix_B: 'Matrix') -> 'Matrix':
    ''' Function sums two matrices and return resulted matrix. '''
    return matrix_A + matrix_B


def multiply_matrices(matrix_A: 'Matrix', matrix_B: 'Matrix') -> 'Matrix':
    ''' Function multiplies two matrices and return resulted matrix. '''
    return matrix_A * matrix_B


def matrix2list(matrix: 'Matrix') -> list:
    ''' This function convert a matrix into list with same values '''
    # Double loop because it looks like: [[],[]].
    # correct_matrix needs for convert each value in matrix to int
    return [ j for i in correct_matrix(matrix).tolist() for j in i ]


def correct_matrix(matrix: 'Matrix') -> 'Matrix':
    ''' This function round each value in matrix and returns matrix with edited values. '''
    return np.matrix([int(round(j)) for i in matrix.tolist() for j in i ])


def get_matrix_from_cache(path_to_file: str = '/tmp/matrix_cache.json') -> list:
    ''' Function fetches all unimodular matrices from cache file. '''
    with open(path_to_file) as file:
        return json.load(file)


def add_matrix_in_cache(added_list: list, path_to_file: str = '/tmp/matrix_cache.json') -> None:
    ''' Function add new unimodular matrix in cache file. '''
    current_info_in_cache = get_matrix_from_cache()
    current_info_in_cache.append(added_list)
    with open(path_to_file, mode='w') as file:
        json.dump(current_info_in_cache, file)


def is_valid_ranges(start: int, start_range: list, end: int, end_range: list) -> bool:
    ''' Function validate start and end, them should be integer and be in given range. '''
    if not isinstance(start, int) or not isinstance(end, int):
        return False
    elif start not in start_range:
        return False
    elif end not in end_range:
        return False
    else:
        return True


def generate_basis(start: int = 20, end: int = 301) -> 'Matrix':
    ''' Function generating a basis and returns it. 

        Arguments:
        ----------
            start: start value in range for generating. Default is 20.
            end:   end value in range for generating. Default is 301.
    '''
    if not is_valid_ranges(start=start,
                           start_range=range(20, 101),
                           end=end,
                           end_range=range(200, 501)):
        raise NotValidValue(
            f"Argument should be integer values, start range should be [20, 100], end - [200, 500]"
        )

    rand_int_for_basis = np.random.randint(start, high=end)

    basis = [
        [
            rand_int_for_basis,
            0
        ],
        [
            0,
            rand_int_for_basis
        ]
    ]

    return np.matrix(basis)


def generate_unimodular_matrix(start: int = 20, end: int = 301) -> 'Matrix':
    ''' Function generating an unimodular matrix and returns it.
        Unimodular matrix - is matrix which determinant is equals 1 or -1.

        Arguments:
        ----------
            start: start value in range for generating. Default is 20.
            end:   end value in range for generating. Default is 301.
    '''
    if not is_valid_ranges(start=start,
                           start_range=range(20, 101),
                           end=end,
                           end_range=range(200, 501)):
        raise NotValidValue(
            f"Argument should be integer values, start range should be [20, 100], end - [200, 500]"
        )

    unimodular_matrix = np.random.randint(start, high=end, size=(2,2))

    iteration = 0
    while iteration <= 9999:
        unimodular_matrix = np.random.randint(start, high=end, size=(2,2))
        
        if determinant_of_matrix(unimodular_matrix) == 1:
            add_matrix_in_cache(unimodular_matrix.tolist())
            return np.matrix(unimodular_matrix)
        
        iteration += 1

    else:
        unimodular_matrix = get_matrix_from_cache()[np.random.randint(len(unimodular_matrix))]
        return np.matrix(unimodular_matrix)


def generate_error_vector(start: int = -10, end: int = 11) -> 'Matrix':
    ''' This function generating an error vector and returns it. '''
    if not is_valid_ranges(start=start,
                           start_range=[-10],
                           end=end,
                           end_range=[11]):
        raise NotValidValue(
            f"Argument should be integer values, start range should be [-10], end - [11]"
        )
    error_vector = np.random.randint(start, high=end, size=(1,2))
    return np.matrix(error_vector)



