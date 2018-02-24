# pylint: disable=W,C,R

from __future__ import print_function

from collections import OrderedDict
from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from wotw_blogger.generator import Template


class TemplateTestCase(TestCase):

    def setUp(self):
        self.construct_template()
        self.addCleanup(self.wipe_template)

    def wipe_template(self):
        del self.template

    def construct_template(self):
        self.template = Template()


class ProcessFileNodeUnitTests(TemplateTestCase):
    """"""


class WalkNodeUnitTests(TemplateTestCase):

    def setUp(self):
        TemplateTestCase.setUp(self)
        block_patcher = patch.object(
            Template,
            'parse_block'
        )
        self.mock_block = block_patcher.start()
        self.addCleanup(block_patcher.stop)
        process_patcher = patch.object(
            Template,
            'process_file_node'
        )
        self.mock_process = process_patcher.start()
        self.addCleanup(process_patcher.stop)

    def test_no_node(self):
        self.mock_block.assert_not_called()
        self.mock_process.assert_not_called()
        self.template.walk_node(None)
        self.mock_block.assert_not_called()
        self.mock_process.assert_not_called()

    def test_block_node(self):
        self.template.files = {'zzz': []}
        self.mock_block.assert_not_called()
        self.mock_process.assert_not_called()
        self.template.walk_node({'block': 'qqq'}, 'zzz')
        self.mock_block.assert_called_once_with('qqq')
        self.mock_process.assert_not_called()

    def test_file_node(self):
        self.mock_block.assert_not_called()
        self.mock_process.assert_not_called()
        self.template.walk_node({'filename': None})
        self.mock_block.assert_not_called()
        self.mock_process.assert_called_once_with('filename', None, None)


class CreateDirectoryUnitTests(TemplateTestCase):
    PATH = 'qqq'

    @patch(
        'wotw_blogger.generator.template.makedirs',
        side_effect=OSError()
    )
    def test_creating_error(self, mock_make):
        mock_make.assert_not_called()
        self.assertRaises(
            OSError,
            Template.create_directory,
            self.PATH
        )

    @patch(
        'wotw_blogger.generator.template.makedirs',
    )
    def test_creating_existing(self, mock_make):
        error = OSError()
        error.errno = EEXIST
        mock_make.side_effect = error
        mock_make.assert_not_called()
        Template.create_directory(self.PATH)
        mock_make.assert_called_once_with(self.PATH)

    @patch(
        'wotw_blogger.generator.template.makedirs'
    )
    def test_creating_new(self, mock_make):
        mock_make.assert_not_called()
        Template.create_directory(self.PATH)
        mock_make.assert_called_once_with(self.PATH)


class WriteFilesUnitTests(TemplateTestCase):
    PATH = 'qqq'
    FILES = OrderedDict()
    FILES['one'] = ['a', 'b', 'c']
    WRITE = MagicMock()

    @patch.object(
        Template,
        'create_directory'
    )
    @patch(
        'wotw_blogger.generator.template.open',
        return_value=MagicMock(
            __enter__=MagicMock(
                return_value=MagicMock(
                    write=WRITE
                )
            )
        )
    )
    def test_writes(self, mock_open, mock_create):
        self.template.files = self.FILES
        self.WRITE.assert_not_called()
        mock_create.assert_not_called()
        mock_open.assert_not_called()
        self.template.write_files(self.PATH)
        mock_create.assert_called_once_with(self.PATH)
        self.WRITE.assert_has_calls([
            call('a\n\nb\n\nc'),
            call('\n')
        ])


class BuildUnitTests(TemplateTestCase):
    YAML_PATH = 'qqq'
    INCLUDE_DIRECTORY = 'zzz'
    DATA = MagicMock()

    @patch.object(
        Template,
        'load_yaml',
        return_value=DATA
    )
    @patch.object(
        Template,
        'walk_node'
    )
    @patch.object(
        Template,
        'write_files'
    )
    def test_construction(self, mock_files, mock_node, mock_load):
        mock_load.assert_not_called()
        mock_node.assert_not_called()
        mock_files.assert_not_called()
        self.template.build(self.YAML_PATH, self.INCLUDE_DIRECTORY)
        mock_load.assert_called_once_with(self.YAML_PATH)
        mock_node.assert_called_once_with(self.DATA)
        mock_files.assert_called_once_with(self.INCLUDE_DIRECTORY)


class LoadYamlUnitTests(TemplateTestCase):
    PATH = 'qqq'
    YAML_FILE = MagicMock()

    @patch(
        'wotw_blogger.generator.template.open',
        return_value=MagicMock(
            __enter__=MagicMock(
                return_value=YAML_FILE
            )
        )
    )
    @patch('wotw_blogger.generator.template.yaml_load')
    def test_call(self, mock_load, mock_open):
        mock_load.assert_not_called()
        Template.load_yaml(self.PATH)
        mock_load.assert_called_once_with(self.YAML_FILE)


class ParseBlockUnitTests(TemplateTestCase):
    INPUT = 'qqq'
    RESULT = "{% block qqq %}{% endblock %}"

    def test_result(self):
        self.assertEquals(
            self.RESULT,
            Template.parse_block(self.INPUT)
        )


class ParseIncludeUnitTests(TemplateTestCase):
    INPUT = 'qqq'
    RESULT = "{% include 'qqq' %}"

    def test_result(self):
        self.assertEquals(
            self.RESULT,
            Template.parse_include(self.INPUT)
        )
