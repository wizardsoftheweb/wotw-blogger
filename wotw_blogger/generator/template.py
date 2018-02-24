# pylint: disable=W,C,R

from errno import EEXIST
from os import makedirs
from os.path import join
from yaml import load as yaml_load


class Template(object):
    files = {}

    def process_file_node(self, key, value, parent=None):
        if not key in self.files:
            self.files[key] = []
        if parent:
            self.files[parent].append(self.parse_include(key))
        if isinstance(value, list):
            for subvalue in value:
                self.walk_node(subvalue, key)
        else:
            self.walk_node(value, key)

    def walk_node(self, node, parent=None):
        if not node:
            return
        for key, value in node.items():
            if 'block' == key:
                self.files[parent].append(self.parse_block(value))
            else:
                self.process_file_node(key, value, parent)

    @staticmethod
    def create_directory(directory_path):
        try:
            makedirs(directory_path)
        except OSError as error:
            if EEXIST == error.errno:
                pass

    def write_files(self, include_directory):
        self.create_directory(include_directory)
        for file_name, contents in self.files.items():
            with open(join(include_directory, file_name), 'w') as template_file:
                if contents:
                    template_file.write('\n\n'.join(contents))
                template_file.write('\n')

    def build(self, yaml_path, include_directory):
        data = self.load_yaml(yaml_path)
        self.walk_node(data)
        self.write_files(include_directory)

    @staticmethod
    def load_yaml(yaml_path):
        with open(yaml_path, 'r') as yaml_file:
            return yaml_load(yaml_file)

    @staticmethod
    def parse_block(title):
        return "{%% block %s %%}{%% endblock %%}" % title

    @staticmethod
    def parse_include(title):
        return "{%% include '%s' %%}" % title
