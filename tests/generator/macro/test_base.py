# pylint: disable=W,C,R

from __future__ import print_function

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
