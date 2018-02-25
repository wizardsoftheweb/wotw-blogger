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
        self.mock_jinja = MagicMock(
            return_value=MagicMock(
                render=self.mock_render
            )
        )
        self.post.jinja_to_use = self.mock_jinja
        self.post.post_basename = self.BASENAME

    def test_render(self):
        self.mock_render.assert_not_called()
        self.mock_jinja.assert_not_called()
        self.post.initial_render()
        self.mock_jinja.assert_called_once_with(self.BASENAME)
        self.mock_render.assert_called_once()


class BuildPostTocUnitTests(PostTestCase):
    """"""


class FinalRenderUnitTests(PostTestCase):
    """"""


class WriteMarkdownUnitTests(PostTestCase):
    """"""


class StripCodeBlocksUnitTests(PostTestCase):
    """"""


class ParseHeadlineUnitTests(PostTestCase):
    """"""


class CreateNewTocLineUnitTests(PostTestCase):
    """"""


class SwapTocUnitTests(PostTestCase):
    """"""


class StripWhitespaceUnitTests(PostTestCase):
    """"""
