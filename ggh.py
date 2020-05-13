from template import GGHAbstract
from accessify import private
from colored import fg, attr
from tools import (
    lookup_in_alphabet,
    generate_basis,
    generate_unimodular_matrix,
    generate_error_vector,
    correct_matrix,
    inverse_matrix,
    multiply_matrices,
    sum_matrices,
    matrix2list
)
import sys
import logging


class GGH(GGHAbstract):
    ''' Class implement GGH algorithm.

        Arguments:
        ----------
            message: message which will be encrypted by Alice and after decrypted by Bob.
            verbose: making output more verbosity. Default value is False
    '''

    def __init__(self, message: list, verbose: bool = False):
        if verbose:
            self.logger = logging.getLogger('GGH')
            self.logger.setLevel(logging.DEBUG)
            h1 = logging.StreamHandler(sys.stdout)
            f1 = logging.Formatter('%(levelname)s: %(message)s')
            h1.setFormatter(f1)
            self.logger.addHandler(h1)

        self.verbose = verbose
        self.message = message

    def algorithm(self):
        ''' Main function which contain all steps of algorithm: generating, encrypting and decrypting. '''

        self.generate()

        if self.verbose:
            self.logger.debug(f"The Alice define message for encrypt: {self.message}")
        else:
            print(f"{fg(2)}The Alice define message for encrypt: {fg(6)}{self.message}{attr('reset')}")

        message = self.convert_message_in_digits(self.message)
        # Message should be have even amount of letters, if not - add space in end
        if len(message) % 2 != 0: message.append(lookup_in_alphabet(' '))

        list_for_encrypt = list()
        list_for_decrypt = list()

        while message:
            first_item = message.pop(0)
            second_item = message.pop(0)
            self.message = [first_item, second_item]
            list_for_encrypt.append(self.encrypt())
            list_for_decrypt.append(self.decrypt())

        
        one_list_for_decrypt = [sublist for item in list_for_decrypt for sublist in item]
        one_list_for_encrypt = [sublist for item in list_for_encrypt for sublist in item]

        message_after_encrypt = "".join([lookup_in_alphabet(item, reverse=True) for item in one_list_for_encrypt]).strip()
        if self.verbose:
            self.logger.debug(f"The Alice encrypted the message using public key and error vector to: {message_after_encrypt} and transmitted it to Bob")
        else:
            print(f"{fg(2)}The Alice encrypted the message to: {fg(6)}{message_after_encrypt}{fg(2)} and transmitted it to Bob{attr('reset')}")

        messafe_after_decrypt = "".join([lookup_in_alphabet(item, reverse=True) for item in one_list_for_decrypt]).strip()
        if self.verbose:
            self.logger.debug(f"The Bob decrypted the message using inverse basis, inverse unimodular matrix and encrypted message: {messafe_after_decrypt}")
        else:
            print(f"{fg(2)}The Bob decrypted the message to: {fg(6)}{messafe_after_decrypt}{attr('reset')}")

    @private
    def convert_message_in_digits(self, message: str) -> list:
        ''' The function rebuild the message into 
        a list with integers that correspond to the letters in the alphabet. 
        '''
        return [lookup_in_alphabet(item) for item in message]

    @private
    def generate(self):
        ''' Function is generating basis, unimodular matrix, error vector and 
        calculate public key, inverse basis, inverse unimodular matrix.
        '''
        self.basis = generate_basis()
        if self.verbose:
            self.logger.debug(f"The Bob generated random basis:\n{self.basis}")
        
        self.inverse_basis = inverse_matrix(self.basis)
        if self.verbose:
            self.logger.debug(f"The Bob calculated inverse basis:\n{self.inverse_basis}")

        self.unimodular_matrix = generate_unimodular_matrix()
        if self.verbose:
            self.logger.debug(f"The Bob generated random unimodular matrix:\n{self.unimodular_matrix}")

        self.inverse_unimodular_matrix = inverse_matrix(self.unimodular_matrix)
        if self.verbose:
            self.logger.debug(f"The Bob calculated inverse basis:\n{self.inverse_unimodular_matrix}")

        self.public_key = multiply_matrices(self.basis, self.unimodular_matrix)
        if self.verbose:
            self.logger.debug(
                f"The Bob calculated pulic key:\n{self.public_key}\nand transmitted it to Alice"
                )

        self.error_vector = generate_error_vector()
        if self.verbose:
            self.logger.debug(f"The Alice generated random error vector:\n{self.error_vector}")

    @private
    def encrypt(self) -> list:
        ''' Function is encrypting message using message, public key and error vector. '''
        self.encrypted_message = sum_matrices(
            multiply_matrices(self.message, self.public_key), self.error_vector
            )
        return matrix2list(self.encrypted_message)

    @private
    def decrypt(self) -> list:
        ''' Function decrypts the encrypted message using,
        inverse basis and inverse unimodular matrix. '''
        self.pre_decrypted_message = correct_matrix(
            multiply_matrices(self.encrypted_message, self.inverse_basis)
            )
        self.decrypted_message = multiply_matrices(
            self.pre_decrypted_message, self.inverse_unimodular_matrix
            )
        return matrix2list(self.decrypted_message)
