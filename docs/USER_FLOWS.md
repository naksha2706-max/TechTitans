# User Flows

## Student — check an opportunity (MVP)

```text
Landing page
   ↓
"Check an opportunity" (no login required)
   ↓
Form: paste message text (required) + optional fields
   (company name, salary, website, contact email)
   ↓
Tap "Check Now"
   ↓
Loading state
   ↓
Results screen:
   - Risk score (large, color-coded: 🟢/🟠/🔴)
   - Warning list (each with a plain-language label)
   - Recommendation text
   - "Was this helpful?" / "Report this as a scam" CTA
   ↓
(optional) Prompted to sign up to save this to history
```

## Student — sign up / log in (MVP)

```text
"Sign up" or "Log in" from nav
   ↓
Email + password form
   ↓
Submit
   ↓
JWT stored client-side
   ↓
Redirect to dashboard (shows past checks if any)
```

## Student — view history (MVP, requires login)

```text
Dashboard
   ↓
List of past checks: company name, date, risk band
   ↓
Tap a past check
   ↓
Full result view (same layout as the original results screen)
```

## Student — report a scam (MVP, Phase 3)

```text
From a results screen (after checking an opportunity), or standalone
   ↓
"Report this as a scam" form:
   - Company name
   - Description (what happened)
   - Contact details (phone/email/UPI) — optional but encouraged
   ↓
Submit
   ↓
Confirmation: "Thanks — this helps warn other students."
   (no promise of investigation timeline or outcome — see
   SECURITY_DESIGN.md on liability)
```

## Admin — review reports (roadmap, Phase 3 later stage)

```text
Admin login (role = admin required)
   ↓
Dashboard: pending reports queue, sorted by date
   ↓
Open a report
   ↓
Review description + any evidence + existing report_count for that
contact
   ↓
Decision: Mark reviewed (confirmed) / Mark dismissed (false report)
   ↓
If dismissed: contact_reputation report_count reverted for that report
   ↓
Return to queue
```

## Admin — monitor activity (roadmap, Phase 3+)

```text
Admin dashboard
   ↓
Summary stats: checks run (7-day), reports submitted, top-reported
contacts, band distribution (% low/medium/high)
   ↓
(Not built until there's enough usage data for these numbers to be
meaningful — don't build this screen with mock/zero data)
```
