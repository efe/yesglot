from django.conf import settings as django_settings


# Default values
DEFAULT_SYSTEM_PROMPT = (
    "You are a professional translator. Translate into the target language.\n"
    "- Keep placeholders like {name} / {{handlebars}} unchanged.\n"
    "- Keep URLs and emails unchanged.\n"
    "- Return ONLY a JSON array of strings in the same order."
)
DEFAULT_PREAMBLE_TEMPLATE = "Translate these items into {language}. Return ONLY a JSON array:\n"


class YesglotSettings:
    """Lazy loading of settings so override_settings works in tests"""

    @property
    def LLM_MODEL(self):
        return django_settings.YESGLOT_LLM_MODEL

    @property
    def API_KEY(self):
        return django_settings.YESGLOT_API_KEY

    @property
    def LLM_MODEL_TEMPERATURE(self):
        # Lower temperature makes outputs more predictable and factual, while higher temperature
        # increases randomness for more diverse and creative results.
        # https://www.youtube.com/shorts/XsLK3tPy9SI
        return getattr(django_settings, "YESGLOT_LLM_MODEL_TEMPERATURE", 0)

    @property
    def SYSTEM_PROMPT_FUNCTION(self):
        return getattr(django_settings, 'YESGLOT_SYSTEM_PROMPT_FUNCTION', None)

    @property
    def SYSTEM_PROMPT(self):
        return getattr(django_settings, 'YESGLOT_SYSTEM_PROMPT', None)

    @property
    def PREAMBLE_TEMPLATE_FUNCTION(self):
        return getattr(django_settings, 'YESGLOT_PREAMBLE_TEMPLATE_FUNCTION', None)

    @property
    def PREAMBLE_TEMPLATE(self):
        return getattr(django_settings, 'YESGLOT_PREAMBLE_TEMPLATE', None)

    @property
    def SAFETY_MARGIN(self):
        # cushion to avoid hitting the hard limit
        return getattr(django_settings, "YESGLOT_SAFETY_MARGIN", 1000)

    @property
    def PER_ITEM_OUTPUT(self):
        # rough estimate of tokens per translated item
        return getattr(django_settings, "YESGLOT_PER_ITEM_OUTPUT", 100)


yesglot_settings = YesglotSettings()
