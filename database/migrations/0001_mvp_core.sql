-- 0001_mvp_core.sql (SQLite)
-- Matches docs/DATABASE_DESIGN.md "MVP tables (Phase 1-2)" exactly.
-- Do NOT add the roadmap tables (companies, scam_documents, domains,
-- message_fingerprints) here — those come in later migrations, one per
-- phase, per AGENTS.md rule 6.
--
-- SQLite has no native UUID or TIMESTAMPTZ type, so:
--   * ids are TEXT, generated with a hex-of-random-bytes expression
--     (formatted to look like a UUID v4 string; not cryptographically
--     validated as v4, just id-shaped and collision-resistant enough
--     for a hackathon MVP).
--   * timestamps are TEXT in ISO-8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`),
--     comparable and sortable as plain strings.
--   * JSONB becomes TEXT holding a JSON string; use json_extract() in
--     queries, or just json.loads() it in the app layer.
--
-- Run this with foreign keys turned on:
--   sqlite3 app.db "PRAGMA foreign_keys = ON;" -init migrations/0001_mvp_core.sql

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
CREATE TABLE users (
    id              TEXT PRIMARY KEY DEFAULT (
                        lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' ||
                        substr(lower(hex(randomblob(2))), 2) || '-' ||
                        substr('89ab', 1 + (abs(random()) % 4), 1) ||
                        substr(lower(hex(randomblob(2))), 2) || '-' ||
                        lower(hex(randomblob(6)))
                    ),
    email           TEXT UNIQUE NOT NULL,
    password_hash   TEXT NOT NULL,
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- ---------------------------------------------------------------------
-- checks: one row per POST /api/analyze call
CREATE TABLE checks (
    id              TEXT PRIMARY KEY DEFAULT (
                        lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' ||
                        substr(lower(hex(randomblob(2))), 2) || '-' ||
                        substr('89ab', 1 + (abs(random()) % 4), 1) ||
                        substr(lower(hex(randomblob(2))), 2) || '-' ||
                        lower(hex(randomblob(6)))
                    ),
    user_id         TEXT REFERENCES users(id) ON DELETE SET NULL, -- nullable: anonymous checks allowed
    company_name    TEXT,
    message_text    TEXT NOT NULL,
    salary          TEXT,
    website         TEXT,
    contact_email   TEXT,
    risk_score      INTEGER NOT NULL,
    risk_band       TEXT NOT NULL CHECK (risk_band IN ('low', 'medium', 'high')),
    warnings        TEXT NOT NULL DEFAULT '[]', -- JSON string: list of {code, points, label}
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE INDEX idx_checks_user ON checks(user_id);

-- ---------------------------------------------------------------------
-- scam_reports: POST /api/reports
CREATE TABLE scam_reports (
    id                  TEXT PRIMARY KEY DEFAULT (
                            lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' ||
                            substr(lower(hex(randomblob(2))), 2) || '-' ||
                            substr('89ab', 1 + (abs(random()) % 4), 1) ||
                            substr(lower(hex(randomblob(2))), 2) || '-' ||
                            lower(hex(randomblob(6)))
                        ),
    user_id             TEXT REFERENCES users(id) ON DELETE SET NULL,
    company_name        TEXT,
    description         TEXT,
    contact_email_hash  TEXT, -- salted hash — see SECURITY_DESIGN.md, never raw
    contact_phone_hash  TEXT,
    contact_upi_hash    TEXT,
    status              TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'dismissed')),
    created_at          TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- ---------------------------------------------------------------------
-- contact_reputation: aggregate, updated whenever a scam_report references
-- a hashed contact. Powers the PRIOR_REPORTS warning (+20 points).
CREATE TABLE contact_reputation (
    id                  TEXT PRIMARY KEY DEFAULT (
                            lower(hex(randomblob(4))) || '-' || lower(hex(randomblob(2))) || '-4' ||
                            substr(lower(hex(randomblob(2))), 2) || '-' ||
                            substr('89ab', 1 + (abs(random()) % 4), 1) ||
                            substr(lower(hex(randomblob(2))), 2) || '-' ||
                            lower(hex(randomblob(6)))
                        ),
    contact_hash        TEXT UNIQUE NOT NULL,
    contact_type        TEXT NOT NULL CHECK (contact_type IN ('email', 'phone', 'upi')),
    report_count        INTEGER NOT NULL DEFAULT 0,
    last_reported_at    TEXT
);

CREATE INDEX idx_contact_reputation_hash ON contact_reputation(contact_hash);
