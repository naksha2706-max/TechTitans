# API Specification

Base path: `/api`

## MVP endpoints (Phase 1–2)

### POST /api/analyze
Run the rule-based risk check on a submitted opportunity.

**Auth:** optional (works anonymously; if a JWT is provided, the check is
saved to that user's history)

**Request**
```json
{
  "company_name": "ABC Technologies",
  "message_text": "You have been selected. Pay ₹3,000 registration fee...",
  "salary": "40000",
  "website": "https://abc-technologies-example.com",
  "contact_email": "hr@abc-technologies-example.com"
}
```

**Response `200`**
```json
{
  "risk_score": 82,
  "risk_band": "high",
  "warnings": [
    { "code": "PAYMENT_REQUESTED", "label": "Registration fee requested", "points": 30 },
    { "code": "URGENT_LANGUAGE", "label": "Urgent payment language detected", "points": 10 }
  ],
  "recommendation": "Do not pay money or share personal information until this opportunity is verified."
}
```

**Errors**
- `422` — missing required field (`message_text` is required, everything
  else optional)
- `429` — rate limited (see SECURITY_DESIGN.md)

---

### POST /api/reports
Submit a scam report.

**Auth:** optional

**Request**
```json
{
  "company_name": "ABC Technologies",
  "description": "Asked for registration fee before any interview.",
  "contact_email": "hr@abc-technologies-example.com",
  "contact_phone": "+91XXXXXXXXXX"
}
```
Backend hashes `contact_email`/`contact_phone`/`contact_upi` before
storage — never persisted in plaintext.

**Response `201`**
```json
{ "id": "uuid", "status": "pending" }
```

---

### GET /api/reputation?type=phone&value=+91XXXXXXXXXX
Look up report count for a hashed contact. Backend hashes `value` before
querying — client sends plaintext over HTTPS, never a pre-hashed value
(prevents hash-reuse/enumeration issues).

**Response `200`**
```json
{ "report_count": 3, "risk_level": "high" }
```

---

### GET /api/checks (auth required)
Return the logged-in user's past checks.

**Response `200`**
```json
{ "checks": [ { "id": "uuid", "company_name": "...", "risk_score": 82, "created_at": "..." } ] }
```

---

### POST /api/auth/register, POST /api/auth/login
Standard email/password auth, returns a JWT.

---

## Roadmap endpoints (add only when the relevant phase starts)

```text
POST /api/analyze/document      -- Phase 4: OCR + image similarity
GET  /api/company/{id}          -- Phase 3: company verification
GET  /api/domain/{domain}       -- Phase 5: WHOIS/SSL lookup
POST /api/admin/reports/{id}/review   -- Phase 3: admin workflow
```

Every endpoint above must define auth requirements and error cases in
this file before it's implemented — don't let the agent invent the
contract while coding.
