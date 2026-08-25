# ai-service/

Standalone microservice, called by `backend/` over HTTP. Keeps scoring logic
swappable without redeploying the main API.

## Run locally

```bash
cd ai-service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8100
```

Test it:

```bash
curl -X POST http://localhost:8100/score \
  -H "Content-Type: application/json" \
  -d '{"message": "Congratulations! Pay Rs 499 registration fee to confirm your work from home job. Hurry, limited seats!", "company_name": ""}'
```

## What's implemented (Phase 1-2)

`app/rules/scorer.py` — pure rule-based scoring, no ML, fully explainable.
Weights live in `app/rules/config.py`. **Align these with
`docs/FEATURE_SPECIFICATION.md` exactly** — that doc is the spec, this file
is the implementation, they must not drift apart.

## What's deliberately NOT implemented yet

- `app/llm/llm_scorer.py` — Phase 3 stub. Few-shot LLM scoring as a
  secondary opinion alongside the rule engine, not a replacement. Disabled
  by default (`AI_SERVICE_LLM_ENABLED=false`). Raises `NotImplementedError`
  if you try to call it before wiring in a real LLM client — this is
  intentional, so nobody accidentally ships fake confidence scores.
- A trained classifier (Phase 4). **Precondition before building this:**
  `training_examples` (see `database/migrations/0003_ai_ml_future.sql`)
  needs a meaningful number of real, non-synthetic rows sourced from actual
  `reports` submissions — not just the ~10 synthetic seed rows. There's no
  hard number that makes a classifier suddenly valid, but low hundreds of
  real labeled examples, roughly balanced between scam/legit, is a
  reasonable floor. Below that, a trained model is just overfitting to
  noise while looking more sophisticated than the rule engine it's supposed
  to improve on.
- Image similarity / fake letterhead matching. Same precondition problem,
  worse — you need actual fake letters to compare against, which you won't
  have until reports start including screenshots. OCR-then-run-through-
  the-existing-rule-engine is the honest interim version (extract text,
  reuse `scorer.py`, no new model needed).

## Why rules first, not a model

The scorer is a pure function (`score_message`) with no network or DB calls
inside it — every input it needs (domain age, reputation hit) is computed
elsewhere and passed in. That makes it trivial to unit test and to swap
later: the LLM/classifier layers can be added as *additional* fields on the
response without touching this function.
