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
        self.post = Post(None, None, None)


class ConstructorUnitTests(PostTestCase):
    """"""


class InitialRenderUnitTests(PostTestCase):
    """"""


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
