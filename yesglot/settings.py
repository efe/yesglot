from django.conf import settings as django_settings

LLM_MODEL = django_settings.YESGLOT_LLM_MODEL
API_KEY = django_settings.YESGLOT_API_KEY

# cushion to avoid hitting the hard limit
SAFETY_MARGIN = getattr(django_settings, "YESGLOT_SAFETY_MARGIN", 1000)

# rough estimate of tokens per translated item
PER_ITEM_OUTPUT = getattr(django_settings, "YESGLOT_PER_ITEM_OUTPUT", 100)
