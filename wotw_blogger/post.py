# pylint: disable=W,C,R

from os.path import basename, join, splitext
from re import (
    compile as re_compile,
    finditer,
    MULTILINE,
    sub
)


class Post(object):

    PATTERNS = {
        'CODE_BLOCKS': re_compile(r"```[\s\S]*?```"),
        'HEADER_LINES': re_compile(
            r"^##(?P<depth>#*)\s*(?P<headline>.*)$",
            MULTILINE
        ),
        'TOC_MARKER': re_compile(
            r"[^\n]*<!--\s*?wotw_toc\s*?-->[^\n]*"
        ),
        'WHITESPACE': [
            [
                re_compile(r"\n\n+"),
                r"\n\n"
            ],
            [
                re_compile(r"\n\n```\n\n"),
                r"\n```\n\n"
            ]
        ]
    }

    def __init__(self, post_path, jinja_to_use, build_path):
        self.post_path = post_path
        self.post_basename = basename(post_path)
        self.jinja_to_use = jinja_to_use
        self.build_path = build_path

    def initial_render(self):
        template = self.jinja_to_use.get_template(self.post_basename)
        content = template.render(
            current_tag=splitext(self.post_basename)[0].replace('.md', '')
        )
        return content.strip().encode('utf-8')

    def build_post_toc(self, content):
        block_free = self.strip_code_blocks(content)
        used_headlines = dict()
        generated_toc = ''
        for header_line_match in finditer(
                self.PATTERNS['HEADER_LINES'],
                block_free
        ):
            cleaned_headline, used_headlines = self.parse_headline(
                header_line_match.group('headline'),
                used_headlines
            )
            generated_toc += self.create_new_toc_line(
                header_line_match.group('depth'),
                header_line_match.group('headline'),
                cleaned_headline
            )
        return self.swap_toc(content, generated_toc)

    def final_render(self):
        initial = self.initial_render()
        with_toc = self.build_post_toc(initial)
        final = self.strip_whitespace(with_toc)
        return final

    def write_markdown(self, contents):
        output_filename = join(
            self.build_path,
            self.post_basename.replace('.j2', '')
        )
        with open(output_filename, 'w+') as built_file:
            built_file.write(contents)

    def build(self):
        contents = self.final_render()
        self.write_markdown(contents)

    @staticmethod
    def strip_code_blocks(content):
        return sub(Post.PATTERNS['CODE_BLOCKS'], '', content, 0)

    @staticmethod
    def parse_headline(headline, used_headlines):
        cleaned_headline = sub('[^a-z]', '', headline.lower())
        if cleaned_headline in used_headlines:
            used_headlines[cleaned_headline] += 1
            cleaned_headline += str(used_headlines[cleaned_headline])
        else:
            used_headlines[cleaned_headline] = 0
        return [cleaned_headline, used_headlines]

    @staticmethod
    def create_new_toc_line(depth_string, headline, cleaned_headline):
        return "%s- [%s](#%s)\n" % (
            sub('#', '  ', depth_string, 0),
            headline,
            cleaned_headline
        )

    @staticmethod
    def swap_toc(content, new):
        return sub(Post.PATTERNS['TOC_MARKER'], new, content)

    @staticmethod
    def strip_whitespace(contents):
        for entry in Post.PATTERNS['WHITESPACE']:
            contents = sub(entry[0], entry[1], contents, 0)
        return contents
