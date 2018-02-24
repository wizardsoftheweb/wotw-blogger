# pylint: disable=W,C,R

from __future__ import print_function

from unittest import TestCase

from mock import MagicMock, patch

from wotw_blogger.generator import Template


class TemplateTestCase(TestCase):

    def setUp(self):
        self.construct_template()
        self.addCleanup(self.wipe_template)

    def wipe_template(self):
        del self.template

    def construct_template(self):
        self.template = Template()


class WalkNodeUnitTests(TemplateTestCase):
    """"""


class WriteFilesUnitTests(TemplateTestCase):
    """"""


class BuildUnitTests(TemplateTestCase):
    """"""


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
