# database/

Matches `docs/DATABASE_DESIGN.md` exactly. Only the MVP tables (Phase 1-2)
are created: `users`, `checks`, `scam_reports`, `contact_reputation`.

Roadmap tables (`companies`, `scam_documents`, `domains`,
`message_fingerprints`) are intentionally NOT here yet — add them in a new
migration file only when that phase actually starts, per AGENTS.md rule 6.

## Run it

```bash
psql "$DATABASE_URL" -f migrations/0001_mvp_core.sql
```

See the main README / step-by-step guide for how to get `$DATABASE_URL`
running via Docker.
