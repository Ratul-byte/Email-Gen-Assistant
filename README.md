# Email Generation Assistant
A complete email generation and evaluation pipeline using **Groq's free LLM API**.  
Compares two prompting strategies across 10 scenarios using 3 custom metrics.

---

## Project Structure

```
email_assistant/
├── config.py           # Model names, output file paths, rate-limit settings
├── scenarios.py        # 10 test scenarios + human reference emails
├── prompts.py          # Two prompt templates (Advanced vs Simple)
├── generator.py        # Email generation functions for both strategies
├── evaluator.py        # 3 custom metrics with LLM-as-judge scoring
├── run_evaluation.py   # Main pipeline → outputs CSV, JSON, summary
├── requirements.txt
├── .env.example
└── README.md
```

---

## Quick Setup (5 minutes)

### 1. Get a Free Groq API Key
1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up for free (no credit card required)
3. Navigate to **API Keys** → **Create API Key**
4. Copy the key

### 2. Clone & Install
```bash
git clone <your-repo-url>
cd email_assistant

pip install -r requirements.txt
```

### 3. Configure Your API Key
```bash
cp .env.example .env
# Open .env and paste your Groq API key
```

### 4. Run the Full Evaluation
```bash
python run_evaluation.py
```

The pipeline takes approximately **5–8 minutes** to complete (rate-limit pauses included).

---

## Output Files

| File | Description |
|------|-------------|
| `evaluation_results.json` | Full results including generated emails and all metric scores |
| `evaluation_results.csv` | Score table only — easy to open in Excel/Sheets |
| `generated_emails.json` | All 20 generated emails (10 scenarios × 2 strategies) |
| `evaluation_summary.json` | Per-strategy aggregated averages |
| `summary_report.txt` | Human-readable summary printed during the run |

---

## Prompting Strategies Compared

### Strategy A — Advanced Prompting ✨
Uses three techniques in combination:

1. **Role-Playing**: The system prompt assigns the model an expert persona —  
   *"You are Alexandra Reed, a corporate communications director with 15+ years of experience..."*  
   This anchors tone, vocabulary, and quality expectations before the task begins.

2. **Few-Shot Examples**: Two complete, high-quality email examples are embedded in the user prompt — one for a post-conference follow-up and one for an apology email.  
   These show the model exactly what structure, length, and style are expected.

3. **Chain-of-Thought**: The prompt is structured as explicit steps:  
   - Step 1: Analyse the request (intent, facts, tone)  
   - Step 2: Study the quality examples  
   - Step 3: Write the email  
   This scaffolding forces the model to process all inputs before generating output.

**Full prompt template:** see `prompts.py → ADVANCED_SYSTEM_PROMPT + ADVANCED_USER_TEMPLATE`

### Strategy B — Simple Zero-Shot Prompting
A minimal prompt with no persona, no examples, and no structured steps:
```
System: You are a helpful assistant that writes professional emails.
User: Write a professional email.
      Intent: ...
      Key facts to include: ...
      Tone: ...
```
Used as the **baseline** to quantify the impact of the advanced techniques.

---

## Custom Evaluation Metrics

All three metrics use **Groq's `llama-3.3-70b-versatile`** as the judge model with temperature=0.1 for consistent, reproducible scoring.

---

### Metric 1 — Fact Recall Score (FRS) `0–10`

**Definition:** Measures what proportion of the required key facts are accurately and naturally incorporated into the generated email.

**Logic:**
- The judge receives the list of required facts and the generated email.
- It evaluates each fact individually: *is it present? is it accurate?*
- Score reflects the proportion found: 10 = all facts present and correct; 0 = no facts present.
- Returns structured JSON: `{"score": X, "facts_found": N, "missing_facts": [...], "reasoning": "..."}`

**Why it matters:** An email that sounds great but omits requested facts fails its core purpose.

---

### Metric 2 — Tone Alignment Score (TAS) `0–10`

**Definition:** Measures how precisely the email's language, vocabulary, sentence structure, and emotional register match the requested tone.

**Logic:**
- The judge evaluates four specific dimensions:
  1. Vocabulary register (formal/informal word choices)
  2. Sentence structure (long/complex vs. short/casual)
  3. Emotional warmth (empathy, enthusiasm, detachment)
  4. Opening and closing style
- Score: 10 = perfect tone throughout; 0 = completely wrong tone.
- Returns: `{"score": X, "observed_tone": "...", "deviations": "...", "reasoning": "..."}`

**Why it matters:** Tone mismatches undermine trust — a formal client email written casually feels unprofessional regardless of content.

---

### Metric 3 — Professional Quality Score (PQS) `0–10`

**Definition:** A hybrid metric combining rule-based structural checks and LLM-evaluated linguistic quality.

**Logic:**

| Component | Method | Max Points |
|-----------|--------|-----------|
| Subject line present | `re.search(r"^subject\s*:", ...)` | 1 |
| Greeting present | regex for "Dear/Hi/Hello..." | 1 |
| Non-trivial body | ≥ 5 non-empty lines | 1 |
| Professional closing | regex for "Sincerely/Regards/Best..." | 1 |
| **Structure subtotal** | Rule-based | **4** |
| Grammar & spelling | LLM judge (0–2) | 2 |
| Clarity & readability | LLM judge (0–2) | 2 |
| Conciseness | LLM judge (0–1) | 1 |
| Coherence & flow | LLM judge (0–1) | 1 |
| **Linguistic subtotal** | LLM-as-judge | **6** |
| **TOTAL** | | **10** |

**Why it matters:** Combines objective structure verification (not fakeable by the judge) with subjective linguistic quality, giving a more reliable composite signal than either approach alone.

---

## Metric Definitions Reference (for Report)

```
METRIC 1: Fact Recall Score (FRS)
  Focus    : Fact inclusion and accuracy
  Range    : 0–10
  Method   : LLM-as-judge (structured JSON output, temperature=0.1)
  Rationale: Email must contain all provided key facts to fulfill its purpose

METRIC 2: Tone Alignment Score (TAS)
  Focus    : Tone accuracy across vocabulary, structure, warmth, and closing style
  Range    : 0–10
  Method   : LLM-as-judge (4 sub-dimensions evaluated explicitly)
  Rationale: Tone mismatch damages professional credibility regardless of content quality

METRIC 3: Professional Quality Score (PQS)
  Focus    : Email structure completeness + linguistic fluency
  Range    : 0–10 (structure 0–4 rule-based + linguistic 0–6 LLM-as-judge)
  Method   : Hybrid (regex/string checks + LLM linguistic evaluation)
  Rationale: Hybrid design adds objective anchoring to the subjective quality score
```

---

## Groq Free Tier Notes

- **Rate limit:** 30 requests/minute for `llama-3.3-70b-versatile`
- **Daily limit:** ~14,400 requests
- **Calls per full run:** ~80 total (20 generation + 60 evaluation)
- The pipeline includes automatic 1.2s pauses between calls to stay within limits.
- If you hit a rate limit error, wait 60 seconds and re-run — already-saved results won't be lost (the pipeline processes scenarios sequentially).

---

## Customisation

| Change | Where |
|--------|-------|
| Swap to a different Groq model | `config.py → MODEL_A / MODEL_B` |
| Adjust generation creativity | `config.py → GENERATION_TEMPERATURE` |
| Add more scenarios | `scenarios.py → SCENARIOS list` |
| Modify prompts | `prompts.py` |
| Change output filenames | `config.py → OUTPUT_*` |
