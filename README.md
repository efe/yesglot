# yesglot

A Django app that autofills missing translations in `.po` files using an LLM, while respecting [ICU](https://unicode-org.github.io/icu/)/format placeholders and source references.

## Why yesglot?

- 🧠 LLM-powered: works with [100+ LLM models](https://models.litellm.ai/) through LiteLLM’s unified API
- 🔒 Placeholder-safe: keeps {name}, {{handlebars}}, URLs, and emails intact
- 📦 Django-native: one management command: python manage.py translatemessages
- 🧮 Cost-aware: prints per-file and total cost (via LiteLLM)
- 🧱 Token-safe batching: automatically splits work to avoid context overflows

## Requirements

- Python 3.10+ (recommended)
- Django

## Installation

```python
pip install yesglot
```

In settings.py:

```python
INSTALLED_APPS = [
    # ...
    "yesglot",
]
```

## Configuration

Set the model from [100+ LLM models](https://models.litellm.ai/) and API key in your Django settings:

```python
YESGLOT_LLM_MODEL = "openai/gpt-4o-mini"
YESGLOT_API_KEY = "sk-..."
```

Optional parameters,

- `YESGLOT_SAFETY_MARGIN`: 1000 (default)
- `YESGLOT_PER_ITEM_OUTPUT`: 100 (default)

## Usage

A typical workflow with Django translations:

1. Extract messages into .po files (creates entries with empty msgstr):

```
python manage.py makemessages -all
```

2. Autofill missing translations with *yesglot*:

```
python manage.py translatemessages
```

Example output:

```
▶ Translation run started.
Using translation model: openai/gpt-4o-mini

• Language: French [fr]
  - Scanning: locale/fr/LC_MESSAGES/django.po
    Missing entries: 12. Translating…
    Filled 12 entries in 3.21s • Cost: $0.0123

============================================================
Done in 3.76s • Files: 1 • Missing found: 12 • Filled: 12 • Total cost: $0.0123
```

3. Compile translations into .mo files (so Django can use them at runtime):

```
python manage.py compilemessages
```

# License

Mozilla Public License Version 2.0

![Yesglot Logo](assets/logo.png)
