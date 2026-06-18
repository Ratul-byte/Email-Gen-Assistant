# ============================================================
# evaluator.py — 3 Custom Metrics (LLM-as-Judge)
# ============================================================
#
# METRIC 1: Fact Recall Score (FRS)
#   Logic   : LLM judge checks whether each required key fact is
#             accurately present in the generated email.
#   Range   : 0–10 (10 = all facts present and accurate)
#   Method  : Pure LLM-as-judge
#
# METRIC 2: Tone Alignment Score (TAS)
#   Logic   : LLM judge evaluates how well the email's vocabulary,
#             sentence structure, formality level, and emotional
#             register match the requested tone.
#   Range   : 0–10 (10 = perfect tone match throughout)
#   Method  : Pure LLM-as-judge
#
# METRIC 3: Professional Quality Score (PQS)
#   Logic   : Hybrid approach.
#             Rule-based component (0–4): checks for the presence
#             of structural email elements (subject line, greeting,
#             body with ≥3 lines, professional closing).
#             LLM component (0–6): judges grammar, clarity,
#             conciseness, and coherence.
#   Range   : 0–10 (sum of rule + LLM components)
#   Method  : Rule-based (regex/string) + LLM-as-judge
#
# ============================================================

import json
import os
import re
import time
from groq import Groq
from config import JUDGE_MODEL, JUDGE_TEMPERATURE, JUDGE_MAX_TOKENS, SLEEP_BETWEEN_CALLS

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# ──────────────────────────────────────────────────────────────
# Shared helpers
# ──────────────────────────────────────────────────────────────

def _call_judge(prompt: str) -> str:
    """Call the Groq judge model and return raw text."""
    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=JUDGE_TEMPERATURE,
        max_tokens=JUDGE_MAX_TOKENS,
    )
    return response.choices[0].message.content.strip()


def _parse_json(text: str, fallback_score: float = 5.0) -> dict:
    """
    Extract the first JSON object from the judge's response.
    Falls back to a default dict if parsing fails.
    """
    # Strip markdown code fences if present
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()

    # Try full parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to extract the first {...} block
    match = re.search(r"\{[\s\S]+?\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    # Last resort: extract score with regex
    score_match = re.search(r'"score"\s*:\s*([0-9]+(?:\.[0-9]+)?)', text)
    score = float(score_match.group(1)) if score_match else fallback_score
    return {"score": score, "reasoning": "JSON parse failed — regex fallback used"}


# ──────────────────────────────────────────────────────────────
# METRIC 1: Fact Recall Score
# ──────────────────────────────────────────────────────────────

_FRS_PROMPT = """You are a strict email quality evaluator measuring FACT RECALL.

Your task: determine whether every required key fact listed below is accurately 
and meaningfully present in the generated email.

REQUIRED KEY FACTS ({n_facts} total):
{facts_list}

GENERATED EMAIL:
{email}

SCORING RUBRIC (0–10):
  10   = All {n_facts} facts present and accurately represented
  8–9  = All or nearly all facts present; very minor omission or paraphrase
  5–7  = Roughly half the facts are present
  2–4  = Only one or two facts included
  0–1  = No facts present, or email text is empty/broken

Evaluate each fact individually, then give an overall score.

Return ONLY valid JSON — no preamble, no markdown:
{{"score": <float 0-10>, "facts_found": <int>, "total_facts": {n_facts}, "missing_facts": ["<fact>", ...], "reasoning": "<1-2 sentence summary>"}}"""


def score_fact_recall(facts: list, generated_email: str) -> dict:
    facts_list = "\n".join(f"  {i+1}. {f}" for i, f in enumerate(facts))
    prompt = _FRS_PROMPT.format(
        n_facts=len(facts),
        facts_list=facts_list,
        email=generated_email,
    )
    raw = _call_judge(prompt)
    result = _parse_json(raw, fallback_score=5.0)
    return {
        "metric": "Fact Recall Score",
        "score": float(result.get("score", 5.0)),
        "facts_found": result.get("facts_found", "N/A"),
        "total_facts": len(facts),
        "missing_facts": result.get("missing_facts", []),
        "reasoning": result.get("reasoning", ""),
    }


# ──────────────────────────────────────────────────────────────
# METRIC 2: Tone Alignment Score
# ──────────────────────────────────────────────────────────────

_TAS_PROMPT = """You are a strict email quality evaluator measuring TONE ALIGNMENT.

Your task: assess how precisely the generated email matches the requested tone.

REQUESTED TONE: {tone}

GENERATED EMAIL:
{email}

Evaluate along these four dimensions:
  1. Vocabulary register  — does word choice suit the requested tone?
  2. Sentence structure   — formal (complex/complete) vs. casual (shorter/fragment)?
  3. Emotional warmth     — appropriate level of empathy, enthusiasm, or detachment?
  4. Opening/closing      — do greeting and sign-off reflect the tone?

SCORING RUBRIC (0–10):
  10   = Perfect tone match throughout the entire email
  8–9  = Very good match; trivial deviations only
  5–7  = Partially matches; noticeable tone inconsistencies
  2–4  = Mostly mismatched; tone is clearly off
  0–1  = Completely wrong tone or incoherent text

Return ONLY valid JSON — no preamble, no markdown:
{{"score": <float 0-10>, "observed_tone": "<what tone the email actually conveys>", "deviations": "<any specific mismatches>", "reasoning": "<1-2 sentence summary>"}}"""


def score_tone_alignment(tone: str, generated_email: str) -> dict:
    prompt = _TAS_PROMPT.format(tone=tone, email=generated_email)
    raw = _call_judge(prompt)
    result = _parse_json(raw, fallback_score=5.0)
    return {
        "metric": "Tone Alignment Score",
        "score": float(result.get("score", 5.0)),
        "observed_tone": result.get("observed_tone", ""),
        "deviations": result.get("deviations", ""),
        "reasoning": result.get("reasoning", ""),
    }


# ──────────────────────────────────────────────────────────────
# METRIC 3: Professional Quality Score (Hybrid)
# ──────────────────────────────────────────────────────────────

_PQS_LLM_PROMPT = """You are a strict email quality evaluator measuring LINGUISTIC QUALITY.

Your task: score the grammar, clarity, conciseness, and coherence of the email below.

GENERATED EMAIL:
{email}

Score on these sub-dimensions (allocate points as shown):
  Grammar & spelling  (0–2): 2 = error-free, 1 = minor errors, 0 = frequent errors
  Clarity             (0–2): 2 = crystal clear, 1 = occasionally unclear, 0 = confusing
  Conciseness         (0–1): 1 = no padding/filler, 0 = repetitive or bloated
  Coherence & flow    (0–1): 1 = paragraphs connect logically, 0 = disjointed

TOTAL possible: 6 points.

Return ONLY valid JSON — no preamble, no markdown:
{{"linguistic_score": <float 0-6>, "grammar_note": "<any grammar issues>", "clarity_note": "<clarity observation>", "reasoning": "<1-2 sentence overall assessment>"}}"""


def _rule_based_structure(email: str) -> dict:
    """
    Rule-based sub-score (0–4) for structural email elements.
    +1 for each: subject line, greeting, non-trivial body, closing phrase
    """
    lower = email.lower()

    has_subject = bool(re.search(r"^subject\s*:", lower, re.MULTILINE))
    has_greeting = bool(re.search(
        r"\b(dear|hi\s+\w|hello\s+\w|good\s+(morning|afternoon|evening))\b",
        lower
    ))
    has_body = len([ln for ln in email.split("\n") if ln.strip()]) >= 5
    has_closing = bool(re.search(
        r"\b(sincerely|regards|best\s+regards|warm\s+regards|yours\s+(sincerely|truly|faithfully)|"
        r"kind\s+regards|respectfully|thank\s+you,)\b",
        lower
    ))

    structure_score = sum([has_subject, has_greeting, has_body, has_closing])

    return {
        "structure_score": structure_score,
        "has_subject_line": has_subject,
        "has_greeting": has_greeting,
        "has_body": has_body,
        "has_closing": has_closing,
    }


def score_professional_quality(generated_email: str) -> dict:
    """
    Metric 3 — Professional Quality Score (hybrid)
    Structure component (rule-based, 0–4) + Linguistic component (LLM, 0–6) = Total (0–10)
    """
    structure = _rule_based_structure(generated_email)

    prompt = _PQS_LLM_PROMPT.format(email=generated_email)
    raw = _call_judge(prompt)
    llm_result = _parse_json(raw, fallback_score=4.0)

    linguistic_score = min(6.0, float(llm_result.get("linguistic_score", 4.0)))
    total = round(structure["structure_score"] + linguistic_score, 2)

    return {
        "metric": "Professional Quality Score",
        "score": total,
        "structure_score": structure["structure_score"],
        "linguistic_score": linguistic_score,
        "has_subject_line": structure["has_subject_line"],
        "has_greeting": structure["has_greeting"],
        "has_closing": structure["has_closing"],
        "grammar_note": llm_result.get("grammar_note", ""),
        "reasoning": llm_result.get("reasoning", ""),
    }


# ──────────────────────────────────────────────────────────────
# Combined evaluation entry point
# ──────────────────────────────────────────────────────────────

def evaluate_email(scenario: dict, generated_email: str, verbose: bool = True) -> dict:
    """
    Run all three metrics on a generated email and return a flat result dict.
    Pauses between judge calls to respect Groq rate limits.
    """
    if verbose:
        print("       → Scoring Fact Recall...")
    frs = score_fact_recall(scenario["facts"], generated_email)
    time.sleep(SLEEP_BETWEEN_CALLS)

    if verbose:
        print("       → Scoring Tone Alignment...")
    tas = score_tone_alignment(scenario["tone"], generated_email)
    time.sleep(SLEEP_BETWEEN_CALLS)

    if verbose:
        print("       → Scoring Professional Quality...")
    pqs = score_professional_quality(generated_email)
    time.sleep(SLEEP_BETWEEN_CALLS)

    avg = round((frs["score"] + tas["score"] + pqs["score"]) / 3, 2)

    return {
        # Metric scores
        "fact_recall_score":          frs["score"],
        "fact_recall_facts_found":    frs.get("facts_found", "N/A"),
        "fact_recall_reasoning":      frs.get("reasoning", ""),
        "tone_alignment_score":       tas["score"],
        "tone_observed":              tas.get("observed_tone", ""),
        "tone_alignment_reasoning":   tas.get("reasoning", ""),
        "prof_quality_score":         pqs["score"],
        "prof_quality_structure":     pqs["structure_score"],
        "prof_quality_linguistic":    pqs["linguistic_score"],
        "prof_quality_has_subject":   pqs["has_subject_line"],
        "prof_quality_has_greeting":  pqs["has_greeting"],
        "prof_quality_has_closing":   pqs["has_closing"],
        "prof_quality_reasoning":     pqs.get("reasoning", ""),
        # Aggregate
        "average_score":              avg,
    }
