# ============================================================
# run_evaluation.py — Main Evaluation Pipeline
# ============================================================
# Usage:
#   python run_evaluation.py
#
# Outputs:
#   evaluation_results.json   — full results with generated emails
#   evaluation_results.csv    — scores table (no email text)
#   generated_emails.json     — generated emails for inspection
#   summary_report.txt        — printed summary saved to file
# ============================================================

import csv
import json
import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Validate API key early
if not os.environ.get("GROQ_API_KEY"):
    print("ERROR: GROQ_API_KEY not found in environment.")
    print("Copy .env.example to .env and add your key from https://console.groq.com")
    sys.exit(1)

from config import (
    MODEL_A, MODEL_B,
    STRATEGY_A_NAME, STRATEGY_B_NAME,
    OUTPUT_JSON, OUTPUT_CSV, OUTPUT_EMAILS,
    SLEEP_BETWEEN_SCENARIOS,
)
from scenarios import SCENARIOS
from generator import generate_both
from evaluator import evaluate_email


# ──────────────────────────────────────────────────────────────
# Core pipeline
# ──────────────────────────────────────────────────────────────

def run_pipeline() -> list[dict]:
    """Generate and evaluate emails for all scenarios. Returns full result list."""
    results = []

    print("\n" + "=" * 65)
    print("  EMAIL GENERATION ASSISTANT — EVALUATION PIPELINE")
    print("=" * 65)
    print(f"  Strategy A : {STRATEGY_A_NAME}")
    print(f"  Strategy B : {STRATEGY_B_NAME}")
    print(f"  Scenarios  : {len(SCENARIOS)}")
    print(f"  Started at : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65 + "\n")

    for idx, scenario in enumerate(SCENARIOS):
        print(f"[{idx+1:02d}/{len(SCENARIOS)}] Scenario {scenario['id']}: "
              f"{scenario['intent'][:55]}...")

        # ── Generation ────────────────────────────────────────
        email_a, email_b = generate_both(scenario, MODEL_A, MODEL_B)

        # ── Evaluation: Strategy A ─────────────────────────────
        print(f"    Evaluating Strategy A...")
        if email_a == "GENERATION_FAILED":
            scores_a = _failed_scores()
        else:
            scores_a = evaluate_email(scenario, email_a, verbose=False)

        # ── Evaluation: Strategy B ─────────────────────────────
        print(f"    Evaluating Strategy B...")
        if email_b == "GENERATION_FAILED":
            scores_b = _failed_scores()
        else:
            scores_b = evaluate_email(scenario, email_b, verbose=False)

        # ── Store results ──────────────────────────────────────
        base = {
            "scenario_id":  scenario["id"],
            "intent":       scenario["intent"],
            "tone":         scenario["tone"],
        }

        results.append({
            **base,
            "strategy":         STRATEGY_A_NAME,
            "generated_email":  email_a,
            **scores_a,
        })
        results.append({
            **base,
            "strategy":         STRATEGY_B_NAME,
            "generated_email":  email_b,
            **scores_b,
        })

        print(f"    ✓  A: avg={scores_a['average_score']:.2f}  |  "
              f"B: avg={scores_b['average_score']:.2f}\n")

        if idx < len(SCENARIOS) - 1:
            time.sleep(SLEEP_BETWEEN_SCENARIOS)

    return results


def _failed_scores() -> dict:
    """Return zero scores when generation failed."""
    return {
        "fact_recall_score": 0.0,
        "fact_recall_facts_found": 0,
        "fact_recall_reasoning": "Generation failed",
        "tone_alignment_score": 0.0,
        "tone_observed": "",
        "tone_alignment_reasoning": "Generation failed",
        "prof_quality_score": 0.0,
        "prof_quality_structure": 0,
        "prof_quality_linguistic": 0.0,
        "prof_quality_has_subject": False,
        "prof_quality_has_greeting": False,
        "prof_quality_has_closing": False,
        "prof_quality_reasoning": "Generation failed",
        "average_score": 0.0,
    }


# ──────────────────────────────────────────────────────────────
# Output writers
# ──────────────────────────────────────────────────────────────

def save_json(results: list[dict]) -> None:
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"  ✓  {OUTPUT_JSON}")


def save_csv(results: list[dict]) -> None:
    """CSV excludes the full email text (too long for a table)."""
    exclude = {"generated_email"}
    fieldnames = [k for k in results[0].keys() if k not in exclude]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow({k: v for k, v in row.items() if k not in exclude})
    print(f"  ✓  {OUTPUT_CSV}")


def save_emails(results: list[dict]) -> None:
    emails = [
        {
            "scenario_id": r["scenario_id"],
            "strategy":    r["strategy"],
            "intent":      r["intent"],
            "tone":        r["tone"],
            "email":       r["generated_email"],
        }
        for r in results
    ]
    with open(OUTPUT_EMAILS, "w", encoding="utf-8") as f:
        json.dump(emails, f, indent=2, ensure_ascii=False)
    print(f"  ✓  {OUTPUT_EMAILS}")


# ──────────────────────────────────────────────────────────────
# Summary report
# ──────────────────────────────────────────────────────────────

def compute_summary(results: list[dict]) -> dict:
    """Compute per-strategy averages across all 10 scenarios."""
    strategies: dict[str, dict] = {}

    for r in results:
        s = r["strategy"]
        if s not in strategies:
            strategies[s] = {
                "frs": [], "tas": [], "pqs": [], "avg": [],
                "n": 0,
            }
        strategies[s]["frs"].append(r["fact_recall_score"])
        strategies[s]["tas"].append(r["tone_alignment_score"])
        strategies[s]["pqs"].append(r["prof_quality_score"])
        strategies[s]["avg"].append(r["average_score"])
        strategies[s]["n"] += 1

    summary = {}
    for s, v in strategies.items():
        n = v["n"]
        summary[s] = {
            "n_scenarios":                n,
            "avg_fact_recall_score":      round(sum(v["frs"]) / n, 2),
            "avg_tone_alignment_score":   round(sum(v["tas"]) / n, 2),
            "avg_prof_quality_score":     round(sum(v["pqs"]) / n, 2),
            "overall_average_score":      round(sum(v["avg"]) / n, 2),
            "per_scenario_averages":      [round(x, 2) for x in v["avg"]],
        }
    return summary


def print_and_save_summary(summary: dict) -> None:
    lines = []
    lines.append("\n" + "=" * 65)
    lines.append("  EVALUATION SUMMARY")
    lines.append("=" * 65)

    metric_labels = {
        "avg_fact_recall_score":    "Fact Recall Score (FRS)     ",
        "avg_tone_alignment_score": "Tone Alignment Score (TAS)  ",
        "avg_prof_quality_score":   "Professional Quality (PQS)  ",
        "overall_average_score":    "OVERALL AVERAGE             ",
    }

    for strategy, stats in summary.items():
        lines.append(f"\n  ▶ {strategy}  (n={stats['n_scenarios']} scenarios)")
        lines.append("  " + "-" * 50)
        for key, label in metric_labels.items():
            score = stats[key]
            bar = "█" * int(score) + "░" * (10 - int(score))
            lines.append(f"    {label}: {score:>5.2f}/10  [{bar}]")
        lines.append(f"    Per-scenario averages: {stats['per_scenario_averages']}")

    lines.append("\n" + "=" * 65)
    report = "\n".join(lines)
    print(report)

    with open("summary_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  ✓  summary_report.txt\n")


# ──────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────

def main():
    results = run_pipeline()

    print("\nSaving outputs...")
    save_json(results)
    save_csv(results)
    save_emails(results)

    summary = compute_summary(results)
    print_and_save_summary(summary)

    # Persist summary into JSON too
    summary_path = "evaluation_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"  ✓  {summary_path}")

    print("\nAll done! Check your output files for the full results.\n")


if __name__ == "__main__":
    main()
