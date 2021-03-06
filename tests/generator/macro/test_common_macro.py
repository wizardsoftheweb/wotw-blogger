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


class InstallUnitTests(MacroTestCase):
    PATH = 'qqq'
    MACRO_NAME = 'sally'
    CONTENTS = 'buzzard'
    WRITE = MagicMock()

    @patch.object(
        Macro,
        'create_directory'
    )
    @patch(
        'wotw_blogger.generator.macro.common_macro.open',
        return_value=MagicMock(
            __enter__=MagicMock(
                return_value=MagicMock(
                    write=WRITE
                )
            )
        )
    )
    def test_writes(self, mock_open, mock_create):
        self.macro.macro_name = self.MACRO_NAME
        self.macro.contents = self.CONTENTS
        self.WRITE.assert_not_called()
        mock_create.assert_not_called()
        mock_open.assert_not_called()
        self.macro.install(self.PATH)
        mock_create.assert_called_once_with(self.PATH)
        self.WRITE.assert_called_once_with(self.CONTENTS)
