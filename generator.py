# ============================================================
# generator.py — Email Generation (Strategy A & B)
# ============================================================

import os
import time
from groq import Groq
from prompts import (
    ADVANCED_SYSTEM_PROMPT,
    ADVANCED_USER_TEMPLATE,
    SIMPLE_SYSTEM_PROMPT,
    SIMPLE_USER_TEMPLATE,
    format_facts,
)
from config import (
    GENERATION_TEMPERATURE,
    GENERATION_MAX_TOKENS,
    SLEEP_BETWEEN_CALLS,
)

# Initialise Groq client (reads GROQ_API_KEY from environment)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def _call_groq(
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = GENERATION_TEMPERATURE,
    max_tokens: int = GENERATION_MAX_TOKENS,
) -> str:
    """Low-level wrapper around the Groq chat completions API."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


# ── Strategy A ─────────────────────────────────────────────
def generate_advanced(
    intent: str,
    facts: list,
    tone: str,
    model: str,
) -> str:
    """
    Strategy A — Advanced Prompting
    Techniques: Role-Playing persona + Few-Shot examples + Chain-of-Thought steps
    """
    user_prompt = ADVANCED_USER_TEMPLATE.format(
        intent=intent,
        facts_formatted=format_facts(facts),
        tone=tone,
    )
    return _call_groq(model, ADVANCED_SYSTEM_PROMPT, user_prompt)


# ── Strategy B ─────────────────────────────────────────────
def generate_simple(
    intent: str,
    facts: list,
    tone: str,
    model: str,
) -> str:
    """
    Strategy B — Simple / Zero-Shot Prompting
    Minimal instructions, no persona, no examples, no structured steps
    """
    user_prompt = SIMPLE_USER_TEMPLATE.format(
        intent=intent,
        facts_formatted=format_facts(facts),
        tone=tone,
    )
    return _call_groq(model, SIMPLE_SYSTEM_PROMPT, user_prompt)


# ── Convenience wrapper ────────────────────────────────────
def generate_both(
    scenario: dict,
    model_a: str,
    model_b: str,
    verbose: bool = True,
) -> tuple[str, str]:
    """
    Generate an email for the same scenario using both strategies.
    Returns (email_advanced, email_simple).
    Includes retry logic on rate-limit errors.
    """
    intent = scenario["intent"]
    facts = scenario["facts"]
    tone = scenario["tone"]

    if verbose:
        print(f"    [A] Generating with Advanced prompting ({model_a})...")
    email_a = _generate_with_retry(generate_advanced, intent, facts, tone, model_a)
    time.sleep(SLEEP_BETWEEN_CALLS)

    if verbose:
        print(f"    [B] Generating with Simple prompting ({model_b})...")
    email_b = _generate_with_retry(generate_simple, intent, facts, tone, model_b)
    time.sleep(SLEEP_BETWEEN_CALLS)

    return email_a, email_b


def _generate_with_retry(fn, intent, facts, tone, model, retries=3, backoff=5):
    """Retry wrapper with exponential backoff for transient API errors."""
    for attempt in range(retries):
        try:
            return fn(intent, facts, tone, model)
        except Exception as e:
            wait = backoff * (attempt + 1)
            print(f"    ⚠ Error on attempt {attempt+1}: {e}. Retrying in {wait}s...")
            time.sleep(wait)
    return "GENERATION_FAILED"
