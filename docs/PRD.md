# PRD — ScamCheck (Internship Scam Detection Platform)

## Problem

Students receive internship/job offers via WhatsApp, Telegram, Instagram,
email, LinkedIn, and job boards. Many are scams: fake companies, fake
recruiters, registration-fee demands, fake offer letters, and UPI payment
requests. Students have no fast way to check whether an offer is genuine.

## Goal

Let a student paste or enter an opportunity's details and receive a risk
score, plain-language warning indicators, and a recommendation — in under
a minute, with no signup friction for the core check.

## Users

**Student** — pastes/enters an opportunity, sees risk score + warnings,
can optionally report a scam.

**Admin** (Phase 3+, not MVP) — reviews reports, manages the reputation
database, resolves disputed/false reports.

---

## MVP scope (build this first — Phase 1–2)

1. Web form: student enters company name, message text, salary, website,
   contact email/phone.
2. Rule-based risk scoring (see `FEATURE_SPECIFICATION.md` for exact
   rules): payment requested, unrealistic salary, urgent language,
   personal/free-email domain, missing company info, sensitive-info
   requests.
3. Risk score (0–100) + Low/Medium/High banding with specific warning
   indicators shown to the student.
4. Student can submit a scam report (stores phone/email/UPI hash +
   description) which feeds a simple report-count reputation lookup for
   future checks against the same contact details.
5. Basic auth (optional account) so a student can view their past checks.

**Explicitly out of scope for MVP:** OCR/offer-letter image analysis,
image-similarity fake-template detection, WHOIS/domain-age lookups,
NLP/ML classifier, WhatsApp bot, Chrome extension, admin dashboard, AWS
deployment. These are documented below as the longer-term roadmap so the
architecture doesn't need to be redesigned later, but none of them block
a working, demo-able Phase 1 product.

---

## Full vision (roadmap — Phase 3 onward, build only after MVP works)

- **Reputation engine**: phone/UPI/email report-count based risk lookup,
  shared across all future checks.
- **NLP classifier**: replace/augment rule-based scoring with a trained
  model once enough labeled message data exists (from scam reports
  collected in MVP).
- **Offer-letter OCR + image similarity**: detect reused fake letter
  templates.
- **Domain intelligence**: WHOIS age, SSL status for a linked website.
- **WhatsApp bot**: forward a suspicious message directly instead of
  copy-pasting into the web app.
- **Chrome extension**: inline risk badge on job listing pages.
- **Admin review workflow**: verify/dispute reports, manage the
  reputation database.
- **Verified Recruiter badge**: opt-in program for legitimate companies.

Each roadmap item should get its own short spec added to
`FEATURE_SPECIFICATION.md` when its phase starts — don't design it in
detail before then, since requirements will shift based on what real
data MVP usage produces.

---

## Non-goals

- This is not a legal determination of fraud. Every score/label must be
  phrased as a risk signal, not a fact (see `AGENTS.md` rule 9).
- Not a general spam/phishing filter — scope is internship/job offers
  specifically.
- Not attempting real-time cross-platform tracking of scammers (no API
  exists for this) — "cross-platform correlation" in the roadmap means
  matching the same contact details across separate *user reports*, not
  live monitoring of WhatsApp/Instagram/Telegram.
