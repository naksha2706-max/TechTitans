# Feature Specification

This file defines exact behavior so the coding agent doesn't have to
guess. Every rule below applies to `POST /api/analyze` in the MVP.

## Rule-based scoring engine (MVP)

Input: `message_text` (required), `salary`, `website`, `contact_email`
(all optional).

Run each check below against the input. Each triggered check adds its
points to a running total, capped at 100. Findings are returned in the
`warnings` array regardless of final band.

| Code | Trigger | Points |
|---|---|---|
| `PAYMENT_REQUESTED` | `message_text` contains payment-related terms combined with a fee context (e.g. "registration fee", "security deposit", "processing fee", "pay ₹", "pay Rs") | +30 |
| `SENSITIVE_INFO_REQUEST` | `message_text` asks for OTP, bank PIN, Aadhaar number, or card details | +20 |
| `SUSPICIOUS_URL` | `website` domain doesn't match `contact_email` domain, or uses a free hosting pattern (e.g. `.tk`, `weebly`, `wixsite` in a claimed "official" company site) | +20 |
| `UNREALISTIC_SALARY` | `salary` present and numeric value is implausible for the stated/inferred role (start with a flat threshold: >₹1,00,000/month for an unspecified/entry role — refine later with role-specific bands) | +15 |
| `URGENT_LANGUAGE` | `message_text` contains urgency phrases ("pay within 1 hour", "limited seats", "immediately", "act now") | +10 |
| `PERSONAL_EMAIL_DOMAIN` | `contact_email` uses a free consumer domain (gmail.com, yahoo.com, outlook.com, etc.) while claiming to represent a company | +10 |
| `NO_COMPANY_INFO` | `company_name` missing/blank, or `website` missing | +10 |

## Scoring & banding

```text
score = sum(triggered rule points), capped at 100

0–30    → risk_band = "low"
31–60   → risk_band = "medium"
61–100  → risk_band = "high"
```

## Recommendation text (fixed strings per band)

- **low**: "This opportunity appears relatively low-risk, but verify the
  company independently before proceeding."
- **medium**: "Some details couldn't be verified. Confirm the recruiter
  and company through an independent channel before applying or sharing
  information."
- **high**: "Multiple high-risk signals were found. Do not pay money or
  share personal/financial information until this opportunity is
  independently verified."

## Copy rules (see AGENTS.md rule 9)

Never render "this is a scam" or "this company is fraudulent." Always
phrase as risk signals: "flagged as high risk," "N students reported this
contact," etc.

## Scam report → reputation flow (MVP)

1. Student submits `POST /api/reports` with optional contact fields.
2. Backend hashes any provided email/phone/UPI (see `SECURITY_DESIGN.md`).
3. Backend upserts `contact_reputation`: increments `report_count` for
   that hash, or creates the row if new.
4. On a future `/api/analyze` or `/api/reputation` call, if a submitted
   contact's hash matches a `contact_reputation` row with
   `report_count >= 1`, add a `PRIOR_REPORTS` warning (+20 points,
   regardless of the fixed rule table above — this is an additive signal
   layered on top of the base rules) with label "N other students
   reported this contact."

## Explicitly deferred (do not implement until their phase)

- NLP-based message classification — Phase 4.
- OCR/offer-letter image analysis — Phase 4.
- WHOIS/SSL domain-age checks — Phase 5.
- Company verification against external registries — Phase 3+.

When one of these phases starts, add its rules to this file in the same
table format before implementation begins.
