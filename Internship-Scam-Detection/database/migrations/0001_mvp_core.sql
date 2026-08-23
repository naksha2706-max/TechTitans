-- 0001_mvp_core.sql
-- Matches docs/DATABASE_DESIGN.md "MVP tables (Phase 1-2)" exactly.
-- Do NOT add the roadmap tables (companies, scam_documents, domains,
-- message_fingerprints) here — those come in later migrations, one per
-- phase, per AGENTS.md rule 6.

CREATE EXTENSION IF NOT EXISTS pgcrypto; -- for gen_random_uuid()

-- ---------------------------------------------------------------------
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           TEXT UNIQUE NOT NULL,
    password_hash   TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------
-- checks: one row per POST /api/analyze call
CREATE TABLE checks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id) ON DELETE SET NULL, -- nullable: anonymous checks allowed
    company_name    TEXT,
    message_text    TEXT NOT NULL,
    salary          TEXT,
    website         TEXT,
    contact_email   TEXT,
    risk_score      INTEGER NOT NULL,
    risk_band       TEXT NOT NULL CHECK (risk_band IN ('low', 'medium', 'high')),
    warnings        JSONB NOT NULL DEFAULT '[]', -- list of {code, points, label}
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_checks_user ON checks(user_id);

-- ---------------------------------------------------------------------
-- scam_reports: POST /api/reports
CREATE TABLE scam_reports (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID REFERENCES users(id) ON DELETE SET NULL,
    company_name        TEXT,
    description         TEXT,
    contact_email_hash  TEXT, -- salted hash — see SECURITY_DESIGN.md, never raw
    contact_phone_hash  TEXT,
    contact_upi_hash    TEXT,
    status              TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'dismissed')),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------
-- contact_reputation: aggregate, updated whenever a scam_report references
-- a hashed contact. Powers the PRIOR_REPORTS warning (+20 points).
CREATE TABLE contact_reputation (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_hash        TEXT UNIQUE NOT NULL,
    contact_type        TEXT NOT NULL CHECK (contact_type IN ('email', 'phone', 'upi')),
    report_count        INTEGER NOT NULL DEFAULT 0,
    last_reported_at    TIMESTAMPTZ
);

CREATE INDEX idx_contact_reputation_hash ON contact_reputation(contact_hash);
