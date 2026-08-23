# System Architecture

## MVP architecture (Phase 1–2)

```text
                     STUDENT (browser)
                          │
                          ▼
                     React Frontend
                          │
                          ▼
                   FastAPI Backend
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        Rule Engine   Report Store  Basic Auth
              │           │
              └─────┬─────┘
                    ▼
              PostgreSQL
```

- Student submits opportunity details via the frontend form.
- Backend runs the rule-based scoring engine (see
  `FEATURE_SPECIFICATION.md`) synchronously and returns a risk score +
  warnings in the same request — no async/queue needed at this scale.
- Scam reports are written to Postgres and read back for a simple
  report-count lookup on phone/email/UPI hash.

## Full architecture (roadmap — do not build until relevant phase)

```text
                       STUDENT
                          │
            ┌─────────────┼─────────────┐
            │             │             │
            ▼             ▼             ▼
        Web App      WhatsApp Bot   Chrome Extension
            │             │             │
            └─────────────┼─────────────┘
                          ▼
                    Backend API
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
   Message Engine    Document Engine   Reputation Engine
   (rules + NLP)      (OCR + image      (phone/UPI/email
                        similarity)       report counts)
         │                │                │
         └────────────────┼────────────────┘
                          ▼
                     Risk Engine
                    (weighted combination
                     of all signal scores)
                          │
                          ▼
                    Risk Score + Warnings
                          │
                          ▼
                   Report / Feedback Loop
                          │
                          ▼
                Scam Fingerprint Database
```

Add the Message Engine's NLP branch, Document Engine, and their storage
only when Phase 4 starts — building them earlier means designing against
data you don't have yet (no labeled messages, no fake-letter corpus).
