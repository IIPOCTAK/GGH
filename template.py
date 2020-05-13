from abc import ABC, abstractmethod


class GGHAbstract(ABC):
    ''' Class template for GGH algorithm.

        Required functions:
        -------------------
            algorithm
            generate
            encrypt
            decrypt
    '''

    @abstractmethod
    def algorithm(self):
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def encrypt(self):
        return None

    @abstractmethod
    def decrypt(self):
        return None
