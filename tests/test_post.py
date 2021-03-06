# pylint: disable=W,C,R

from __future__ import print_function

from collections import OrderedDict
from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from wotw_blogger import Post


class PostTestCase(TestCase):

    def setUp(self):
        self.construct_post()
        self.addCleanup(self.wipe_post)

    def wipe_post(self):
        del self.post

    def construct_post(self):
        basename_patcher = patch('wotw_blogger.post.basename')
        self.mock_basename = basename_patcher.start()
        self.post = Post(None, None, None)
        basename_patcher.stop()


class ConstructorUnitTests(PostTestCase):

    def test_assignment(self):
        self.assertIsNone(self.post.post_path)
        self.assertIsNone(self.post.jinja_to_use)
        self.assertIsNone(self.post.build_path)


class InitialRenderUnitTests(PostTestCase):
    BASENAME = 'qqq'

    def setUp(self):
        PostTestCase.setUp(self)
        self.mock_render = MagicMock()
        self.mock_template = MagicMock(
            return_value=MagicMock(
                render=self.mock_render
            )
        )
        self.mock_jinja = MagicMock(
            get_template=self.mock_template
        )
        self.post.jinja_to_use = self.mock_jinja
        self.post.post_basename = self.BASENAME

    def test_render(self):
        self.mock_render.assert_not_called()
        self.mock_template.assert_not_called()
        self.post.initial_render()
        self.mock_template.assert_called_once_with(self.BASENAME)
        self.mock_render.assert_called_once()


class BuildPostTocUnitTests(PostTestCase):
    CONTENT = 'qqq'
    BLOCK_FREE = '### HEADLINE'

    def setUp(self):
        PostTestCase.setUp(self)
        strip_patcher = patch.object(
            Post,
            'strip_code_blocks',
            return_value=self.BLOCK_FREE
        )
        self.mock_strip = strip_patcher.start()
        self.addCleanup(strip_patcher.stop)
        parse_patcher = patch.object(
            Post,
            'parse_headline',
            return_value=['one', 'two']
        )
        self.mock_parse = parse_patcher.start()
        self.addCleanup(parse_patcher.stop)
        create_patcher = patch.object(
            Post,
            'create_new_toc_line'
        )
        self.mock_create = create_patcher.start()
        self.addCleanup(create_patcher.stop)
        swap_patcher = patch.object(
            Post,
            'swap_toc'
        )
        self.mock_swap = swap_patcher.start()
        self.addCleanup(swap_patcher.stop)

    def test_strip(self):
        self.mock_strip.assert_not_called()
        self.post.build_post_toc(self.CONTENT)
        self.mock_strip.assert_called_once_with(self.CONTENT)


class FinalRenderUnitTests(PostTestCase):

    @patch.object(Post, 'initial_render')
    @patch.object(Post, 'build_post_toc')
    @patch.object(Post, 'strip_whitespace')
    def test_result(self, mock_white, mock_build, mock_render):
        mock_render.assert_not_called()
        mock_build.assert_not_called()
        mock_white.assert_not_called()
        self.post.final_render()
        mock_render.assert_called_once()
        mock_build.assert_called_once()
        mock_white.assert_called_once()


class WriteMarkdownUnitTests(PostTestCase):
    CONTENTS = 'buzzard'
    WRITE = MagicMock()

    @patch('wotw_blogger.post.join')
    @patch(
        'wotw_blogger.post.open',
        return_value=MagicMock(
            __enter__=MagicMock(
                return_value=MagicMock(
                    write=WRITE
                )
            )
        )
    )
    def test_writes(self, mock_open, mock_create):
        self.WRITE.assert_not_called()
        mock_create.assert_not_called()
        mock_open.assert_not_called()
        self.post.write_markdown(self.CONTENTS)
        self.WRITE.assert_called_once_with(self.CONTENTS)


class BuildUnitTests(PostTestCase):

    @patch.object(Post, 'final_render')
    @patch.object(Post, 'write_markdown')
    def test_result(self, mock_write, mock_render):
        mock_render.assert_not_called()
        mock_write.assert_not_called()
        self.post.build()
        mock_render.assert_called_once()
        mock_write.assert_called_once()


class StripCodeBlocksUnitTests(PostTestCase):
    INPUT = """
test
```
qqq
```
fin
"""
    RESULT = """
test

fin
"""

    def test_strip(self):
        self.assertEquals(
            self.RESULT,
            Post.strip_code_blocks(self.INPUT)
        )


class ParseHeadlineUnitTests(PostTestCase):
    INPUT = [
        ['1qqq', {}],
        ['2qqq', {'qqq': 0}]
    ]

    RESULT = [
        ['qqq', {'qqq': 0}],
        ['qqq1', {'qqq': 1}]
    ]

    def test_headlines(self):
        for index in range(len(self.INPUT)):
            self.assertEquals(
                self.RESULT[index],
                Post.parse_headline(*self.INPUT[index])
            )


class CreateNewTocLineUnitTests(PostTestCase):
    INPUT = [
        ['#', 'q q q', 'qqq'],
    ]

    RESULT = [
        '  - [q q q](#qqq)\n',
    ]

    def test_headlines(self):
        for index in range(len(self.INPUT)):
            self.assertEquals(
                self.RESULT[index],
                Post.create_new_toc_line(*self.INPUT[index])
            )


class SwapTocUnitTests(PostTestCase):
    INPUT = """
    <!-- wotw_toc -->
"""
    RESULT = 'qqq'

    def test_swap(self):
        self.assertEquals(
            self.RESULT,
            Post.swap_toc('qqq', self.INPUT)
        )


class StripWhitespaceUnitTests(PostTestCase):
    INPUT = """



```


"""
    RESULT = """
```

"""

    def test_clean(self):
        self.assertEquals(
            self.RESULT,
            Post.strip_whitespace(self.INPUT)
        )
