import json
import logging

import tiktoken
from litellm import completion, completion_cost, get_max_tokens

from yesglot.settings import API_KEY, LLM_MODEL, PER_ITEM_OUTPUT, SAFETY_MARGIN

logging.getLogger("LiteLLM").setLevel(logging.ERROR)

SYSTEM_PROMPT = (
    "You are a professional translator. Translate into the target language.\n"
    "- Keep placeholders like {name} / {{handlebars}} unchanged.\n"
    "- Keep URLs and emails unchanged.\n"
    "- Return ONLY a JSON array of strings in the same order."
)
PREAMBLE_TEMPLATE = "Translate these items into {language}. Return ONLY a JSON array:\n"


def get_encoder(model):
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        return tiktoken.get_encoding("cl100k_base")


def count_tokens(text, enc):
    return len(enc.encode(text))


def make_batches(items, target_language, model):
    """Split items into token-safe batches."""
    encoder = get_encoder(model)

    # Precompute stable token costs
    system_tokens = count_tokens(SYSTEM_PROMPT, encoder)
    user_preamble = PREAMBLE_TEMPLATE.format(language=target_language)
    preamble_tokens = count_tokens(user_preamble, encoder)

    batches = []
    current = []

    for item in items:
        candidate = current + [item]

        # Variable part: JSON array of items
        items_json = json.dumps(candidate, ensure_ascii=False)
        items_tokens = count_tokens(items_json, encoder)

        # Estimated output tokens
        est_output_tokens = PER_ITEM_OUTPUT * len(candidate)

        # Total estimated tokens
        total_tokens = system_tokens + preamble_tokens + items_tokens + est_output_tokens

        max_context_tokens = get_max_tokens(LLM_MODEL)
        if current and total_tokens >= (max_context_tokens - SAFETY_MARGIN):
            batches.append(current)
            current = [item]
        else:
            current = candidate

    if current:
        batches.append(current)

    return batches


def translate_batch(batch, target_language, model):
    user_prompt = PREAMBLE_TEMPLATE.format(language=target_language) + json.dumps(batch, ensure_ascii=False)
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
        api_key=API_KEY,
    )
    cost = completion_cost(completion_response=response)

    content = response["choices"][0]["message"]["content"].strip()
    return json.loads(content), cost


def translate_items(items, target_language, model=LLM_MODEL):
    results = []
    total_cost = 0
    for batch in make_batches(items, target_language, model):
        translations, cost = translate_batch(batch, target_language, model)

        results.extend(translations)
        total_cost += cost

    return dict(zip(items, results)), total_cost
