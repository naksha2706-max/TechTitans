# AI/ML Design

## Status: Roadmap (Phase 4) — do not build until Phase 1–3 are working

The MVP scoring engine is entirely rule-based (see
`FEATURE_SPECIFICATION.md`). No ML model is required to ship a working
demo. This document defines the AI components for later phases so the
architecture doesn't need to be redesigned when that work starts — but
none of it should be implemented before Phase 4 begins, and Phase 4
should not begin before Phase 2/3 have produced real usage data.

## Why AI is deferred, not skipped

A classifier is only as good as its training data. Before Phase 1–3 run
in production, there is no labeled dataset of genuine vs. scam messages
to train on. Building the model first means training on synthetic or
guessed examples, which won't generalize. The correct order is:
collect real `checks` and `scam_reports` data first (Phase 2–3) → then
train (Phase 4).

## Component 1 — Message classifier (NLP)

**Input:** `message_text`
**Output:** suspicious probability (0–1), used as an *additional* signal
alongside the rule engine — not a replacement, until it's measurably more
accurate than rules on held-out data.

**Approach:**
- Start simple: TF-IDF + Logistic Regression on labeled messages from
  `scam_reports` (label = reported) vs. `checks` with low risk_score and
  no follow-up report (label = likely genuine). This labeling is noisy —
  treat early model output with caution and keep the rule engine as the
  primary signal until accuracy is validated.
- Only move to a pretrained transformer model if the simple baseline
  shows the approach has value and more data is available.

## Component 2 — Entity extraction

**Input:** `message_text`
**Output:** structured fields — phone, email, UPI ID, company name, URL

Used to auto-fill the analyze form when a student pastes a raw forwarded
message instead of filling fields individually. Can start as regex-based
extraction (phone/email/UPI patterns, URL regex) before any ML is
involved — this doesn't need to wait for Phase 4 and could move into
Phase 2 if it simplifies the UI.

## Component 3 — OCR (offer-letter text extraction)

**Input:** uploaded offer-letter image
**Output:** extracted text, then run through the same entity extraction
and rule engine as a pasted message

**Approach:** Tesseract for MVP-of-this-feature; only move to a cloud OCR
API if accuracy on real uploaded documents is insufficient.

## Component 4 — Image embedding + similarity search

**Input:** offer-letter image
**Output:** a vector embedding, compared against previously reported fake
templates via cosine similarity

**Important constraint:** this component has near-zero value until a
seeded dataset of known-fake letter images exists (from Phase 3 reports
with evidence uploads). Do not implement before that dataset exists —
there will be nothing to match against.

## Component 5 — Risk engine (combining signals)

Once Phase 4/5 components exist, the final score becomes a weighted
combination instead of the pure rule-sum used in MVP:

```text
Rule-based signals        40%
NLP classifier            20%
Document similarity       15%
Domain intelligence       15%
Reputation (reports)      10%
```

These weights are a starting point, not fixed — tune them against
labeled outcomes once enough data exists, and document any change here.

## Explicit rule (see AGENTS.md rule 10)

No single AI/ML signal should be allowed to push a score into "high risk"
alone if every rule-based signal is clean. Combine signals; don't let one
noisy model override everything else.
