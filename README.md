# Career Navigation Assistant (CNA)

An intelligent career guidance and development platform for Computer Science students: discover suitable technology careers, understand *why* they match, see the skills they require, and follow a personalised roadmap to prepare for them.

**Status:** Phase 1–2 complete (planning) — documents awaiting review. No application code yet.

## What CNA will do
- **Assess** interests across nine technology areas (software, AI/ML, data, cloud, security, networking, databases, UI/UX, QA)
- **Recommend** career paths with transparent, factor-level explanations (rule-based, deterministic — no ML claims)
- **Analyse** skills gaps against a chosen career (having / developing / planned / not-assessed)
- **Guide** with staged learning roadmaps and progress tracking
- **Serve** a personal dashboard, career comparison, and an admin-managed career catalogue

## Documentation
| Document | Contents |
|---|---|
| [docs/requirements.md](docs/requirements.md) | Functional + non-functional requirements with acceptance criteria |
| [docs/architecture.md](docs/architecture.md) | System components, API conventions, security, testing strategy |
| [docs/database-design.md](docs/database-design.md) | MySQL schema: 22 tables, ERD, integrity rules, migration/seed strategy |
| [docs/assessment-methodology.md](docs/assessment-methodology.md) | Assessment instrument, categories, scoring rules |
| [docs/recommendation-methodology.md](docs/recommendation-methodology.md) | Weighted scoring model, explanations, evaluation plan |
| [docs/project-plan.md](docs/project-plan.md) | Phases → increments → issues with acceptance criteria and risks |
| [docs/decisions.md](docs/decisions.md) | ADR-style decision log |

## Technology
React + TypeScript + Tailwind CSS (frontend) · Python + Flask REST (backend) · MySQL 8 (database) · pytest / Vitest / Playwright (testing) · Alembic migrations · Git.

## Repository layout (planned)
```
backend/    Flask REST API, recommendation engine, migrations, seeds, tests
frontend/   React SPA (Vite), component kit, feature modules, tests
docs/       Project documentation (authoritative for the report)
```

## Getting started
Setup and run instructions will be added in Phase 3 (increment I1) once the application skeleton exists. The MySQL root-password reset and database bootstrap are the first planned environment tasks.

## Important notes
- The assessment and recommendations support career **exploration only** — they are not clinical instruments and predict neither suitability nor employment outcomes.
- Synthetic evaluation data is always labelled synthetic; no fabricated results are reported.
