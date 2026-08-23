# Testing Plan

## Phase 2 — Rule engine tests

Each rule in `FEATURE_SPECIFICATION.md` needs a positive and negative
test case (triggers correctly, and doesn't false-positive on clean input).

| Rule | Positive case | Expected | Negative case | Expected |
|---|---|---|---|---|
| `PAYMENT_REQUESTED` | "Pay ₹2,000 registration fee to confirm your seat" | +30, warning present | "No fees required to apply" | no warning |
| `SENSITIVE_INFO_REQUEST` | "Share your Aadhaar number and OTP to proceed" | +20 | "Please attach your resume" | no warning |
| `SUSPICIOUS_URL` | website domain ≠ contact email domain | +20 | both match | no warning |
| `UNREALISTIC_SALARY` | salary = 200000, role unspecified | +15 | salary = 15000 | no warning |
| `URGENT_LANGUAGE` | "Pay within 1 hour or lose your seat" | +10 | "Apply by Friday" | no warning |
| `PERSONAL_EMAIL_DOMAIN` | contact_email = hr@gmail.com | +10 | contact_email = hr@company.com | no warning |
| `NO_COMPANY_INFO` | company_name blank | +10 | company_name filled | no warning |

**End-to-end scoring tests:**
- A message triggering payment + urgency + sensitive-info should land in
  "high" band (≥61)
- A message with only `NO_COMPANY_INFO` triggered should land in "low"
  band (≤30)
- A message with no fields filled beyond required `message_text`, and no
  rules triggered, should score 0 / "low" and not error

## Phase 3 — Reputation & reporting tests

- Submit a report with a phone number → `contact_reputation.report_count`
  increments from 0 to 1
- Submitting a second report with the same (normalized) phone number
  increments to 2, doesn't create a duplicate row
- Running `/api/analyze` with a `contact_email` matching a reported
  contact returns the `PRIOR_REPORTS` warning
- Running `/api/analyze` with a contact that has never been reported
  returns no `PRIOR_REPORTS` warning
- Two different formats of the same phone number (e.g. with/without
  country code) normalize to the same hash

## Security / abuse tests

- Exceeding the rate limit on `/api/analyze` returns `429`
- `message_text` over the length cap is rejected with `422`, not
  truncated silently
- Raw phone/email/UPI never appears in the `scam_reports` or
  `contact_reputation` tables when inspected directly — only hashes
- A user cannot fetch another user's `checks` history via
  `GET /api/checks` (auth boundary test)
- Malformed/missing JWT on an auth-required endpoint returns `401`, not
  a 500 or silent anonymous fallback

## False positive / false negative review (ongoing, not one-off)

- Periodically sample real `checks` results and manually review: did any
  clearly genuine internship get flagged "high risk"? Did any obvious
  scam pattern score "low"? Use findings to adjust rule weights in
  `FEATURE_SPECIFICATION.md` — don't let the scoring table drift from
  what's actually implemented.

## Phase 4+ tests (roadmap, define when that phase starts)

- NLP classifier: accuracy/precision/recall against a held-out labeled
  set, compared against the rule-engine-only baseline before it's allowed
  to influence the score
- OCR: known fake template image → high similarity score; a genuine,
  never-seen-before template → low similarity score
- Malicious file upload (wrong type, oversized, embedded script) is
  rejected before OCR processing runs
