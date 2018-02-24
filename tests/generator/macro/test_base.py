# pylint: disable=W,C,R

from __future__ import print_function

from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from wotw_blogger.generator.macro import Macro


class MacroTestCase(TestCase):

    def setUp(self):
        self.construct_macro()
        self.addCleanup(self.wipe_macro)

    def wipe_macro(self):
        del self.macro

    def construct_macro(self):
        self.macro = Macro()


class CreateDirectoryUnitTests(MacroTestCase):
    PATH = 'qqq'

    @patch(
        'wotw_blogger.generator.macro.base.makedirs',
        side_effect=OSError()
    )
    def test_creating_error(self, mock_make):
        mock_make.assert_not_called()
        self.assertRaises(
            OSError,
            Macro.create_directory,
            self.PATH
        )

    @patch(
        'wotw_blogger.generator.macro.base.makedirs',
    )
    def test_creating_existing(self, mock_make):
        error = OSError()
        error.errno = EEXIST
        mock_make.side_effect = error
        mock_make.assert_not_called()
        Macro.create_directory(self.PATH)
        mock_make.assert_called_once_with(self.PATH)

    @patch(
        'wotw_blogger.generator.macro.base.makedirs'
    )
    def test_creating_new(self, mock_make):
        mock_make.assert_not_called()
        Macro.create_directory(self.PATH)
        mock_make.assert_called_once_with(self.PATH)
