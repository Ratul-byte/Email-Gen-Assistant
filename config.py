# ============================================================
# config.py — Email Generation Assistant
# ============================================================

# --- Model Configuration ---
# Strategy A: Advanced Prompting (Role-Playing + Few-Shot + Chain-of-Thought)
MODEL_A = "llama-3.3-70b-versatile"
STRATEGY_A_NAME = "Llama-3.3-70B | Advanced Prompting"

# Strategy B: Simple / Zero-Shot Prompting (same model, different prompt)
MODEL_B = "llama-3.3-70b-versatile"
STRATEGY_B_NAME = "Llama-3.3-70B | Simple Prompting"

# LLM-as-Judge model for evaluation
JUDGE_MODEL = "llama-3.3-70b-versatile"

# --- Generation Settings ---
GENERATION_TEMPERATURE = 0.7
GENERATION_MAX_TOKENS = 1000

# --- Evaluation Settings ---
JUDGE_TEMPERATURE = 0.1   # Low temperature for consistent scoring
JUDGE_MAX_TOKENS = 400

# --- Rate Limiting ---
SLEEP_BETWEEN_CALLS = 1.2   # seconds between API calls to respect free tier
SLEEP_BETWEEN_SCENARIOS = 2.0  # additional pause between scenarios

# --- Output Files ---
OUTPUT_JSON = "evaluation_results.json"
OUTPUT_CSV = "evaluation_results.csv"
OUTPUT_EMAILS = "generated_emails.json"
