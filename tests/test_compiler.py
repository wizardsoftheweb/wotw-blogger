# pylint: disable=W,C,R

from __future__ import print_function

from collections import OrderedDict
from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from wotw_blogger import Compiler


class CompilerTestCase(TestCase):

    def setUp(self):
        self.construct_compiler()
        self.addCleanup(self.wipe_compiler)

    def wipe_compiler(self):
        del self.compiler

    def construct_compiler(self):
        self.compiler = Compiler(None, None, None)


class ConstructorUnitTests(CompilerTestCase):

    def test_assignment(self):
        self.assertIsNone(self.compiler.post_path)
        self.assertIsNone(self.compiler.template_path)
        self.assertIsNone(self.compiler.build_path)


class BuildJinjaUnitTests(CompilerTestCase):

    @patch('wotw_blogger.compiler.Environment')
    @patch('wotw_blogger.compiler.FileSystemLoader')
    def test_construction(self, mock_file, mock_env):
        mock_env.assert_not_called()
        mock_file.assert_not_called()
        self.compiler.build_jinja()
        mock_env.assert_called_once()
        mock_file.assert_called_once()
