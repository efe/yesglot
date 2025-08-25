from unittest import mock
from django.test import SimpleTestCase
from django.test.utils import override_settings

from yesglot.exceptions import YesGlotException
from yesglot.llm import get_system_prompt, get_preamble_template
from yesglot.settings import DEFAULT_SYSTEM_PROMPT, DEFAULT_PREAMBLE_TEMPLATE


def dummy_function():
    return "dummy"


class SystemPromptTests(SimpleTestCase):
    @override_settings(YESGLOT_SYSTEM_PROMPT_FUNCTION="tests.test_prompts.dummy_function", YESGLOT_SYSTEM_PROMPT="literal")
    def test_conflict_raises(self):
        with self.assertRaises(YesGlotException):
            get_system_prompt()

    @override_settings(YESGLOT_SYSTEM_PROMPT_FUNCTION="tests.test_prompts.dummy_function")
    def test_from_function(self):
        self.assertEqual(get_system_prompt(), "dummy")

    @override_settings(YESGLOT_SYSTEM_PROMPT="literal-sp")
    def test_literal(self):
        self.assertEqual(get_system_prompt(), "literal-sp")

    def test_default(self):
        self.assertEqual(get_system_prompt(), DEFAULT_SYSTEM_PROMPT)


class PreambleTemplateTests(SimpleTestCase):
    @override_settings(YESGLOT_PREAMBLE_TEMPLATE_FUNCTION="tests.test_prompts.dummy_function", YESGLOT_PREAMBLE_TEMPLATE="literal")
    def test_conflict_raises(self):
        with self.assertRaises(YesGlotException):
            get_preamble_template()

    @override_settings(YESGLOT_PREAMBLE_TEMPLATE_FUNCTION="tests.test_prompts.dummy_function", YESGLOT_PREAMBLE_TEMPLATE="")
    def test_from_function(self):
        self.assertEqual(get_preamble_template(), "dummy")

    @override_settings(YESGLOT_PREAMBLE_TEMPLATE_FUNCTION="", YESGLOT_PREAMBLE_TEMPLATE="Hi in {language}: ",
                       DEFAULT_PREAMBLE_TEMPLATE="Default {language}: ")
    def test_literal(self):
        self.assertEqual(get_preamble_template(), "Hi in {language}: ")

    @override_settings(YESGLOT_PREAMBLE_TEMPLATE_FUNCTION="", YESGLOT_PREAMBLE_TEMPLATE="",
                       DEFAULT_PREAMBLE_TEMPLATE="Default {language}: ")
    def test_default(self):
        self.assertEqual(get_preamble_template(), DEFAULT_PREAMBLE_TEMPLATE)
