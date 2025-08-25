from django.utils.module_loading import import_string

from yesglot.exceptions import YesGlotException
from yesglot.settings import yesglot_settings
from yesglot.settings import DEFAULT_SYSTEM_PROMPT, DEFAULT_PREAMBLE_TEMPLATE


def get_system_prompt():
    if yesglot_settings.SYSTEM_PROMPT_FUNCTION and yesglot_settings.SYSTEM_PROMPT:
        raise YesGlotException("You can't use system prompt function and system prompt at the same time.")
    elif yesglot_settings.SYSTEM_PROMPT_FUNCTION:
        func = import_string(yesglot_settings.SYSTEM_PROMPT_FUNCTION)
        return func()
    elif yesglot_settings.SYSTEM_PROMPT:
        return yesglot_settings.SYSTEM_PROMPT
    else:
        return DEFAULT_SYSTEM_PROMPT


def get_preamble_template():
    if yesglot_settings.PREAMBLE_TEMPLATE_FUNCTION and yesglot_settings.PREAMBLE_TEMPLATE:
        raise YesGlotException("You can't use system prompt function and system prompt at the same time.")
    elif yesglot_settings.PREAMBLE_TEMPLATE_FUNCTION:
        func = import_string(yesglot_settings.PREAMBLE_TEMPLATE_FUNCTION)
        return func()
    elif yesglot_settings.PREAMBLE_TEMPLATE:
        return yesglot_settings.PREAMBLE_TEMPLATE
    else:
        return DEFAULT_PREAMBLE_TEMPLATE