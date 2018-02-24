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
    """"""


class ParseBlockUnitTests(TemplateTestCase):
    """"""


class ParseIncludeUnitTests(TemplateTestCase):
    """"""
