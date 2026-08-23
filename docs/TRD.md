# TRD — Technical Requirements

## Guiding rule

Ship Phase 1 (MVP) on the simplest possible stack that will actually run
end-to-end for a demo. Don't add a service (Redis, S3, Cognito, vector DB,
etc.) until the phase that needs it is actually starting.

## MVP stack (Phase 1–2)

| Layer | Choice | Why |
|---|---|---|
| Frontend | React (Vite) | Fast to scaffold, matches team familiarity |
| Backend | Python + FastAPI | Simple, async, good for later ML integration |
| Database | PostgreSQL | Relational data (users, reports, companies) fits well |
| Auth | JWT (simple email/password) | No need for a managed auth service yet |
| Hosting (demo) | Render / Railway / a single VM | One-click deploy, avoids AWS setup overhead during MVP |

## Roadmap stack (add only when the relevant phase starts)

| Phase | Addition | Purpose |
|---|---|---|
| Phase 3 (reputation) | Redis (optional) | Fast repeated lookups if volume justifies it |
| Phase 4 (NLP) | scikit-learn → later Transformers | Message classifier, trained on collected reports |
| Phase 4 (OCR) | Tesseract / cloud OCR API | Offer-letter text extraction |
| Phase 4 (image similarity) | A pretrained vision model + a vector index (e.g. pgvector or FAISS) | Fake-template matching |
| Phase 5 (domain intel) | `python-whois`, SSL check library | Domain age / cert validity |
| Phase 6 (integrations) | WhatsApp Business API, Chrome extension (Manifest V3) | Alternate entry points |
| Phase 7 (deployment) | AWS: RDS, S3, ECS/Lambda, CloudWatch | Only once the product needs production-grade scale |

## Explicit stack decisions NOT to make yet

- Do not provision AWS Cognito, ECS, or Lambda for MVP — this adds IAM/
  networking complexity with no benefit until Phase 7.
- Do not add a vector database until Phase 4 actually needs image
  similarity search — Postgres alone is enough until then.
- Do not add Redis until there's a measured latency problem — premature
  caching adds a moving part with no payoff in early phases.
