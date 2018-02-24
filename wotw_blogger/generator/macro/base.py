# pylint: disable=W,C,R

from errno import EEXIST
from os import makedirs
from os.path import join


class Macro(object):
    macro_name = None
    contents = None

    def install(self, macro_directory):
        self.create_directory(macro_directory)
        with open(join(macro_directory, self.macro_name), 'w') as macro_file:
            macro_file.write(self.contents)

    @staticmethod
    def create_directory(directory_path):
        try:
            makedirs(directory_path)
        except OSError as error:
            if EEXIST != error.errno:
                raise
