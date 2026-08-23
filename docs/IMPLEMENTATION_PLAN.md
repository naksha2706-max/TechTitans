# Implementation Plan

Build strictly in order. Do not start a phase until the previous one is
working and manually tested. Mark each phase `[ ]` → `[x]` as completed.

## Phase 1 — Foundation
- [x] React frontend scaffold, FastAPI backend scaffold, Postgres running
- [x] `users` table + JWT auth (register/login)
- [x] Basic layout: opportunity-check form, empty results panel

## Phase 2 — Core scanner (this is the demo-able MVP)
- [x] `POST /api/analyze` implementing every rule in
      `FEATURE_SPECIFICATION.md`
- [x] Results UI: risk score, band (🟢/🟠/🔴), warning list, recommendation
- [x] `checks` table: save every analysis (anonymous or logged-in)
- [x] `GET /api/checks` + simple history page for logged-in users

**Test before moving on:**
- A message with a fee request scores into "high" band
- A clean message with no red flags scores into "low" band
- Missing optional fields (salary, website) doesn't crash the endpoint

## Phase 3 — Reputation & reporting
- [x] `scam_reports` + `contact_reputation` tables
- [x] `POST /api/reports` with hashing per `SECURITY_DESIGN.md`
- [x] `GET /api/reputation` lookup
- [x] Wire `PRIOR_REPORTS` signal into `/api/analyze` per
      `FEATURE_SPECIFICATION.md`
- [ ] (Optional, later in this phase) minimal admin view to mark reports
      reviewed/dismissed

**Test before moving on:**
- Reporting a contact, then checking an opportunity with the same
  contact, surfaces the `PRIOR_REPORTS` warning
- A never-reported contact shows no reputation warning

## Phase 4 — AI/NLP + document analysis (roadmap, not required for demo)
- [ ] Collect labeled data from Phase 2/3 usage (genuine vs. reported
      messages) before attempting to train anything
- [ ] NLP classifier as an additional signal alongside rules, not a
      replacement, until it's proven more accurate
- [ ] OCR pipeline for uploaded offer letters
- [ ] Image embedding + similarity search against reported fake letters
      (needs a seeded dataset — don't build until you have one)

## Phase 5 — Domain intelligence
- [x] WHOIS / domain parsing lookup module (`app/domain_intel.py`)
- [x] SSL certificate validity check
- [x] Feed into `SUSPICIOUS_URL` & `INVALID_SSL` scoring as an additional signal


## Phase 6 — Integrations (roadmap)
- [ ] WhatsApp bot: forward message → same `/api/analyze` call → bot reply
- [ ] Chrome extension: extract visible job page text → same endpoint →
      inline badge

## Phase 7 — Production deployment (roadmap)
- [ ] Move from single-VM/Render hosting to AWS only once real usage
      justifies it (RDS, S3 for uploads, ECS/Lambda, CloudWatch)

---

## General testing notes (apply to every phase)

- Test both directions for every rule: a message that should trigger a
  warning, and a similar-but-clean message that shouldn't (false positive
  check).
- Test missing/malformed input on every endpoint (empty strings, huge
  payloads, wrong types).
- Test auth boundaries: an endpoint requiring auth must reject an invalid/
  missing token; a user must not be able to read another user's `checks`.
- Test rate limiting actually triggers `429` past the configured
  threshold.
