-- 0003_ai_ml_future.sql
-- DO NOT APPLY THIS YET.
--
-- This is Phase 4+ schema (per AI_ML_DESIGN.md). It exists now only so the
-- shape is documented and Antigravity doesn't invent its own version later.
-- Apply only once training_examples has meaningfully organic growth from
-- real `reports` rows (see ai-service/README.md for the exact precondition).

-- ---------------------------------------------------------------------
-- training_examples
-- The labeled dataset your rule-based scorer currently has no substitute
-- for. Populated two ways: (1) synthetic seed rows you write by hand now,
-- (2) a trigger/job that copies `reports` + `opportunity_checks` into this
-- table whenever a report is filed, using report_type as the label.
-- ---------------------------------------------------------------------
CREATE TABLE training_examples (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_text    TEXT NOT NULL,
    label           TEXT NOT NULL CHECK (label IN ('scam', 'legit', 'unclear')),
    source          TEXT NOT NULL CHECK (source IN ('synthetic', 'user_report', 'manual_review')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------
-- fake_letter_embeddings
-- Only useful once you have a nontrivial number of known fake offer
-- letters to compare against. Do not build the matching feature before
-- this table has real rows — an empty comparison set is a no-op feature
-- that just adds latency and a false sense of coverage.
-- ---------------------------------------------------------------------
CREATE TABLE fake_letter_embeddings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_report_id UUID REFERENCES reports(id) ON DELETE SET NULL,
    image_hash      TEXT NOT NULL,      -- perceptual hash, cheap first pass
    embedding       VECTOR(512),        -- requires pgvector extension; swap
                                         -- for BYTEA + external vector DB if
                                         -- pgvector isn't available
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
