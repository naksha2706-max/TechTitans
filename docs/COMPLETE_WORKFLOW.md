# Complete Workflow

## Workflow A — Student checks an opportunity (MVP, Phase 2)

```text
Student receives a message (WhatsApp/email/social media)
        ↓
Opens ScamCheck web app
        ↓
Pastes message text, optionally fills company/salary/website/email
        ↓
POST /api/analyze
        ↓
Rule engine evaluates each rule in FEATURE_SPECIFICATION.md
        ↓
If a contact hash matches an existing scam_reports entry (Phase 3),
add the PRIOR_REPORTS signal
        ↓
Score summed, capped at 100, banded low/medium/high
        ↓
Response: risk_score + warnings[] + recommendation
        ↓
Frontend renders result panel
        ↓
(If logged in) result saved to checks table for history
```

## Workflow B — Student reports a scam (MVP, Phase 3)

```text
Student decides an opportunity was a scam
        ↓
Fills report form: company name, description, contact details
        ↓
POST /api/reports
        ↓
Backend hashes any phone/email/UPI provided
        ↓
scam_reports row created (status = pending)
        ↓
contact_reputation upserted: report_count incremented
        ↓
Future /api/analyze calls referencing the same contact hash
now surface a PRIOR_REPORTS warning
```

## Workflow C — Offer-letter document check (roadmap, Phase 4)

```text
Student uploads offer letter image
        ↓
File validated (type/size) and malware-scanned
        ↓
OCR extracts text
        ↓
Extracted text run through the same entity extraction + rule engine
as Workflow A
        ↓
Image embedding generated
        ↓
Compared via similarity search against known-fake letter embeddings
(scam_documents table)
        ↓
Similarity score folded into the weighted risk engine (AI_ML_DESIGN.md)
        ↓
Combined result returned
```

## Workflow D — WhatsApp bot (roadmap, Phase 6)

```text
Student forwards a suspicious message to the ScamCheck WhatsApp number
        ↓
WhatsApp Business API webhook receives it
        ↓
Bot extracts message text, calls POST /api/analyze
        ↓
Bot replies in-chat with risk band + top 2-3 warnings (kept short
for a chat interface, full detail available via a link to the web app)
```

## Workflow E — Chrome extension (roadmap, Phase 6)

```text
Student opens a job/internship listing page (e.g. on a job board)
        ↓
Extension content script extracts visible text (title, company,
description, salary if shown)
        ↓
Calls POST /api/analyze in the background
        ↓
Extension overlays a badge on the page: 🟢/🟠/🔴 + score
        ↓
Click badge → expands to full warnings list
```

## Workflow F — Admin review (roadmap, Phase 3 later stage)

```text
Admin logs in
        ↓
Views pending scam_reports queue
        ↓
Reviews description + any evidence
        ↓
Marks status: reviewed (confirmed) or dismissed (false report)
        ↓
If dismissed, contact_reputation report_count is decremented/reverted
so a false report doesn't permanently penalize a real contact
        ↓
If confirmed, no change needed — report_count already reflects it
```
