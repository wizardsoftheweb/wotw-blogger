# pylint: disable=W,C,R

from errno import EEXIST
from os import makedirs


class Generator(object):

    @staticmethod
    def create_directory(directory_path):
        try:
            makedirs(directory_path)
        except OSError as error:
            if EEXIST != error.errno:
                raise
