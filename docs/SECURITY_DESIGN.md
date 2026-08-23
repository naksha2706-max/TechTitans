# Security Design

## PII handling

- Never store raw phone numbers, emails, or UPI IDs in `scam_reports` or
  `contact_reputation`. Hash with a salted hash (e.g. HMAC-SHA256 with a
  server-side secret pepper stored in an environment variable) before
  writing to the database.
- `checks.contact_email` in the MVP table is stored in plaintext because
  it's tied to a specific analysis request the student made about
  themselves — this is different from `scam_reports`, which stores
  hashed contact info about a *third party* (the recruiter/company) that
  will be looked up by other users. Keep this distinction — do not hash
  fields that only the submitting user will ever see again, and do not
  store plaintext fields that will be matched against future users'
  submissions.
- Normalize phone numbers (E.164) and lowercase/trim emails before
  hashing, so the same contact always hashes to the same value.

## Authentication & authorization

- JWT-based auth. Tokens expire after a reasonable window (e.g. 24h) with
  refresh handled client-side.
- `/api/analyze` and `/api/reports` work without auth (reduce friction),
  but attach `user_id` when a valid token is present.
- `/api/checks` (history) requires a valid token — a user can only read
  their own checks.
- Admin endpoints (roadmap) require a separate `role = admin` check, not
  just "logged in."

## Abuse prevention

- Rate limit `/api/analyze` and `/api/reports` per IP (e.g. 20 requests/
  10 minutes) to prevent scraping or spam reporting.
- Validate and cap `message_text` length (e.g. 5,000 chars) to prevent
  abuse of the scoring engine as a free-text dump.
- When file upload is added (Phase 4 OCR), validate file type/size and
  scan for malware before processing — do not implement upload without
  this.
- Track duplicate/near-duplicate scam reports from the same source to
  reduce brigading of a real company's reputation score.

## False-positive / liability handling

- Every risk output must be phrased as a probability/signal, never a
  factual accusation (see `AGENTS.md` rule 9 and
  `FEATURE_SPECIFICATION.md` copy rules).
- `scam_reports.status` starts as `pending` — reports do not affect
  public-facing company data until reviewed (Phase 3 admin workflow).
  In MVP, `contact_reputation` counts are used only as a scoring signal
  shown to the checking student, not published anywhere else.
- Provide a way (roadmap, Phase 3) for a company/recruiter to dispute a
  report attached to their contact details.

## Secrets

- DB credentials, JWT signing key, and the HMAC pepper for hashing all
  live in environment variables, never committed to the repo. Provide a
  `.env.example` with placeholder keys only.
