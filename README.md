# ScamCheck — Internship Scam Detection Platform

A tool that lets students paste or upload a job/internship opportunity
(message, company details, salary, website) and get back a **risk score**
with clear warning indicators and a recommendation — so they can tell a
genuine offer from a scam before they pay money or share personal info.

## Project status

This repo is scoped as an **MVP first, roadmap second**. Do not attempt to
build every feature in `docs/PRD.md` at once — follow the phases in
`docs/IMPLEMENTATION_PLAN.md` in order. Phase 1 is a fully working
rule-based scanner with no AI/ML dependency; everything after that is a
stretch goal layered on top of a working product.

## 🔑 Key Features

| **Feature**                          | **What It Does**                                                                                               | **Impact**                                         |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| 🧠 **AI Scam Detection**             | Analyzes internship messages and identifies suspicious language, payment requests, and scam patterns.          | Detects threats early.                             |
| 🧬 **Scam Fingerprint Database**     | Stores unique fingerprints of reported scams using phone numbers, UPI IDs, emails, URLs, and message patterns. | Recognizes reused scams.                           |
| 🤝 **Crowdsourced Reporting**        | Allows students to report suspicious recruiters, offers, websites, and payment details.                        | Builds collective scam intelligence.               |
| ⭐ **Recruiter & Company Reputation** | Maintains trust/risk profiles based on verified student experiences and previous reports.                      | Helps students make informed decisions.            |
| 💳 **UPI Reputation Check**          | Checks whether payment identifiers have been previously reported for scams.                                    | Prevents fraudulent payments.                      |
| 🔗 **Cross-Platform Correlation**    | Connects the same phone, UPI, email, or recruiter across WhatsApp, Telegram, Instagram, and job platforms.     | Exposes repeated scam campaigns.                   |
| 📄 **Offer Letter Analysis**         | Uses OCR and image analysis to examine uploaded offer letters/certificates.                                    | Detects suspicious documents and reused templates. |
| 🌐 **Website & Domain Intelligence** | Checks domain age, SSL status, and website-related risk signals.                                               | Identifies suspicious recruitment websites.        |
| 📊 **Intelligent Risk Score**        | Combines multiple signals into a 0–100 risk score with reasons.                                                | Provides clear, evidence-based warnings.           |
| 🤖 **WhatsApp Scam Bot**             | Students can forward suspicious messages directly to the bot for analysis.                                     | Makes detection quick and frictionless.            |
| 🌐 **Chrome Extension**              | Scans internship/job listings and displays a risk badge while browsing.                                        | Provides protection at the point of discovery.     |
| 🔄 **Continuous Learning**           | Uses validated reports and new scam patterns to improve future detection.                                      | Makes the system stronger over time.               |


## Structure

```text
internship-scam-detector/
├── AGENTS.md                 ← read this first if you are an AI coding agent
├── README.md                 ← you are here
│
├── docs/
│   ├── PRD.md                 Product requirements (full vision + MVP cut)
│   ├── TRD.md                 Technical stack decisions
│   ├── SYSTEM_ARCHITECTURE.md Component diagram, MVP vs later phases
│   ├── DATABASE_DESIGN.md     Tables/fields for MVP + future phases
│   ├── API_SPECIFICATION.md   Endpoints, request/response, errors
│   ├── FEATURE_SPECIFICATION.md  Exact behavior of every feature
│   ├── SECURITY_DESIGN.md     Hashing, auth, abuse prevention, liability
│   └── IMPLEMENTATION_PLAN.md Build phases in order
│
├── frontend/       React app (student-facing form + results)
├── backend/        FastAPI service (scoring engine, APIs, DB access)
├── ai-service/      Phase 4+: NLP classifier, OCR, embeddings (not MVP)
└── database/       Migrations / seed data
```

## Getting started (Phase 1 MVP)

```bash
# backend
cd backend
python -m venv venv && source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary
uvicorn main:app --reload

# frontend
cd frontend
npm install
npm run dev
```

## For AI coding agents (Antigravity, Claude Code, etc.)

Read `AGENTS.md`, then `docs/PRD.md` (MVP section only), then
`docs/IMPLEMENTATION_PLAN.md`. Do not start on Phase 2+ features until
Phase 1 is fully working and tested.
