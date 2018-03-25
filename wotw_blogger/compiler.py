# pylint: disable=W,C,R

from os import listdir
from os.path import basename

from jinja2 import Environment, FileSystemLoader

from wotw_highlighter import Block

from wotw_blogger import Post


class Compiler(object):

    def __init__(self, post_path, template_path, build_path):
        self.post_path = post_path
        self.template_path = template_path
        self.build_path = build_path

    def build_jinja(self):
        jinja_env = Environment(
            loader=FileSystemLoader([self.post_path, self.template_path])
        )
        jinja_env.globals['highlight_block'] = self.highlight_block
        return jinja_env

    def compile_everything(self):
        jinja_env = self.build_jinja()
        for post_filename in listdir(self.post_path):
            post = Post(post_filename, jinja_env, self.build_path)
            post.build()

    @staticmethod
    def highlight_block(content, **kwargs):
        blob = Block(content, inline_css=True, **kwargs)
        return blob.highlighted_blob

    @staticmethod
    def basename(file_path):
        return basename(file_path)
