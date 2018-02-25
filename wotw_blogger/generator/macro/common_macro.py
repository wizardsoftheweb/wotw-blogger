# pylint: disable=W,C,R

from errno import EEXIST
from os import makedirs
from os.path import join

from wotw_blogger.generator import Generator


class Macro(Generator):
    macro_name = None
    contents = None

    def install(self, macro_directory):
        self.create_directory(macro_directory)
        with open(join(macro_directory, self.macro_name), 'w') as macro_file:
            macro_file.write(self.contents)
