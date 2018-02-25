# pylint: disable=W,C,R

from __future__ import print_function

from collections import OrderedDict
from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from wotw_blogger.generator import Generator


class GeneratorTestCase(TestCase):

    def setUp(self):
        self.construct_generator()
        self.addCleanup(self.wipe_generator)

    def wipe_generator(self):
        del self.generator

    def construct_generator(self):
        self.generator = Generator()


class CreateDirectoryUnitTests(GeneratorTestCase):
    PATH = 'qqq'

    @patch(
        'wotw_blogger.generator.common_generator.makedirs',
        side_effect=OSError()
    )
    def test_creating_error(self, mock_make):
        mock_make.assert_not_called()
        self.assertRaises(
            OSError,
            Generator.create_directory,
            self.PATH
        )

    @patch(
        'wotw_blogger.generator.common_generator.makedirs',
    )
    def test_creating_existing(self, mock_make):
        error = OSError()
        error.errno = EEXIST
        mock_make.side_effect = error
        mock_make.assert_not_called()
        Generator.create_directory(self.PATH)
        mock_make.assert_called_once_with(self.PATH)

    @patch(
        'wotw_blogger.generator.common_generator.makedirs'
    )
    def test_creating_new(self, mock_make):
        mock_make.assert_not_called()
        Generator.create_directory(self.PATH)
        mock_make.assert_called_once_with(self.PATH)
