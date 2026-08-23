# Database Design

## MVP tables (Phase 1–2)

### users
```text
id              uuid, primary key
email           text, unique
password_hash   text
created_at      timestamptz
```

### checks
Each time a student runs a risk check, store the input + result so they
can view history.
```text
id              uuid, primary key
user_id         uuid, nullable (anonymous checks allowed)
company_name    text
message_text    text
salary          text, nullable
website         text, nullable
contact_email   text, nullable
risk_score      int
risk_band       text          -- 'low' | 'medium' | 'high'
warnings        jsonb         -- list of triggered warning codes
created_at      timestamptz
```

### scam_reports
```text
id              uuid, primary key
user_id         uuid, nullable
company_name    text
description     text
contact_email_hash  text, nullable
contact_phone_hash  text, nullable
contact_upi_hash    text, nullable
status          text          -- 'pending' | 'reviewed' | 'dismissed'
created_at      timestamptz
```

### contact_reputation
Simple aggregate table, updated whenever a new scam_report references a
hashed contact. Used for the "N other students reported this contact"
signal.
```text
id              uuid, primary key
contact_hash    text, unique  -- hash of email/phone/upi
contact_type    text          -- 'email' | 'phone' | 'upi'
report_count    int, default 0
last_reported_at timestamptz
```

---

## Roadmap tables (add only when the relevant phase starts)

### companies (Phase 3+)
```text
id                    uuid, primary key
name                  text
website               text
email_domain          text
verification_status   text
trust_score           int
```

### scam_documents (Phase 4+, OCR/image similarity)
```text
id              uuid, primary key
image_url       text
embedding       vector       -- requires pgvector extension
report_count    int
created_at      timestamptz
```

### domains (Phase 5+, WHOIS/SSL)
```text
id                   uuid, primary key
domain               text, unique
registration_date    date
ssl_status           text
risk_score           int
```

### message_fingerprints (Phase 4+, NLP)
```text
id                uuid, primary key
fingerprint       text
message_embedding vector
report_count      int
```

## Notes

- All contact hashes use a salted hash (see `SECURITY_DESIGN.md`) — never
  store raw phone/email/UPI in `scam_reports` or `contact_reputation`.
- Don't create the roadmap tables in the initial migration — add them in
  the migration for the phase that needs them, so the schema stays
  understandable and matches what's actually implemented.
