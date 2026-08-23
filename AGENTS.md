# Agent Rules — Internship Scam Detection Platform

You are an AI coding agent working on this repository. Follow these rules
before writing or changing any code.

## Before doing anything

1. Read `docs/PRD.md` — pay attention to the "MVP scope" section. The
   "Full vision" section is a roadmap, NOT something to build now.
2. Read `docs/TRD.md` for the approved tech stack. Do not introduce a new
   framework, database, or language without asking the user first.
3. Read `docs/SYSTEM_ARCHITECTURE.md` and `docs/DATABASE_DESIGN.md` before
   creating or modifying any backend module or table.
4. Read `docs/IMPLEMENTATION_PLAN.md` and confirm which phase is currently
   active. Do not build features from a later phase.

## Hard rules

5. Do not invent features that aren't in `docs/FEATURE_SPECIFICATION.md`.
   If a feature is ambiguous, stop and ask rather than guessing.
6. Do not change the database schema without updating
   `docs/DATABASE_DESIGN.md` in the same change.
7. Never store phone numbers, UPI IDs, or emails in plaintext — hash them
   per `docs/SECURITY_DESIGN.md` before persisting.
8. Every API endpoint that reads/writes user data must have authentication
   and authorization checks. See `docs/API_SPECIFICATION.md`.
9. Risk scores are a probability/heuristic signal, not legal proof of
   fraud. Never render UI copy or API responses that assert a company or
   person "is a scammer" — always phrase it as "flagged as high risk" or
   similar. This is a liability requirement, not a style preference.
10. Do not mark any company/recruiter as fraudulent based on a single
    signal (e.g. one report, one keyword match). Risk scores must combine
    multiple signals per `docs/AI_ML_DESIGN.md` / `docs/FEATURE_SPECIFICATION.md`.
11. Write a test for every backend feature you add (see testing notes in
    `docs/IMPLEMENTATION_PLAN.md`).
12. Keep frontend, backend, and ai-service modules independent — the
    backend must run and serve Phase 1 features with ai-service absent.
13. Keep all secrets (DB credentials, API keys) in environment variables,
    never hard-coded.
14. When you finish a phase, update `docs/IMPLEMENTATION_PLAN.md` to mark
    it complete before starting the next one.

## When in doubt

Stop and ask the user rather than assuming. A wrong assumption here means
either shipping a false "this is a scam" accusation about a real company,
or leaking a student's personal data — both are worse than a pause to ask.
