# database/

Matches `docs/DATABASE_DESIGN.md` exactly. Only the MVP tables (Phase 1-2)
are created: `users`, `checks`, `scam_reports`, `contact_reputation`.

Roadmap tables (`companies`, `scam_documents`, `domains`,
`message_fingerprints`) are intentionally NOT here yet — add them in a new
migration file only when that phase actually starts, per AGENTS.md rule 6.

## Engine: SQLite

This project uses SQLite (a single on-disk `.db` file) instead of Postgres,
so there's no server to install or run — no Docker, no `DATABASE_URL`.
A few things that differ from a Postgres setup because of that:

- **IDs**: no native UUID type, so `id` columns are `TEXT` populated by a
  `DEFAULT` expression that builds a UUID-v4-shaped string out of
  `randomblob()`/`hex()`. It's fine for a hackathon MVP; it isn't a
  cryptographically-audited UUID implementation.
- **Timestamps**: no `TIMESTAMPTZ`, so `created_at` / `last_reported_at`
  are `TEXT` in ISO-8601 UTC (`2026-08-25T15:30:32.026Z`) — sortable as
  plain strings.
- **JSON**: no `JSONB`, so `checks.warnings` is `TEXT` holding a JSON
  string. Use `json.loads()` in Python, or SQLite's `json_extract()` in a
  query.
- **Foreign keys**: SQLite doesn't enforce them unless you turn it on
  *per connection*. Always run `PRAGMA foreign_keys = ON;` right after
  opening a connection, before running any inserts/deletes.

## Run it

```bash
python3 - <<'PY'
import sqlite3
conn = sqlite3.connect("app.db")
conn.executescript(open("migrations/0001_mvp_core.sql").read())
conn.commit()
PY
```

That creates `database/app.db`. From then on, any code (backend, tests,
a quick `sqlite3` shell if you have the CLI installed) just opens that
same file — remember the `PRAGMA foreign_keys = ON;` step above in every
connection.
