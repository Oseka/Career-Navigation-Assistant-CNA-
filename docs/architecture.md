# CNA — System Architecture and Design

**Status:** Draft v0.1 — 2026-10-14 — awaiting review

---

## 1. Architecture overview

```mermaid
flowchart LR
    subgraph Client["Browser"]
        SPA["React SPA<br/>(Vite + TypeScript + Tailwind)"]
    end
    subgraph Backend["Flask REST API"]
        API["API layer<br/>(Blueprints + Pydantic validation)"]
        SVC["Services<br/>(business logic)"]
        REC["Recommendation engine<br/>(pure Python package)"]
        ORM["SQLAlchemy 2 ORM<br/>+ Alembic migrations"]
    end
    DB[("MySQL 8")]

    SPA -- "HTTPS /api/* (JSON, session cookie)" --> API
    API --> SVC
    SVC --> REC
    SVC --> ORM
    REC --> ORM
    ORM --> DB
```

The system has five components, matching the charter (section 8):

| Component | Responsibility | Runs in |
|---|---|---|
| Frontend | Pages, forms, assessment flow, career discovery, comparison, dashboard, progress display | Browser (React SPA) |
| Backend | Auth, validation, REST endpoints, profiles, career data, application workflows | Flask (Python) |
| Recommendation service | Assessment scoring, career matching, ranking, explanations | Pure-Python package inside the backend, no Flask imports |
| Data layer | Users, profiles, skills, careers, assessments, recommendations, roadmaps, progress | MySQL 8 via SQLAlchemy |
| External integration layer | Reserved for the optional AI assistant (Feature J, deferred) | — |

Key rule: **business logic lives in services and the recommendation package, never in blueprints or React components**, so each part can be tested independently (charter section 8).

## 2. Backend design

```
backend/
├── app/
│   ├── __init__.py          # application factory
│   ├── config.py            # environment-driven configuration
│   ├── extensions.py        # db (SQLAlchemy), migrate, session, limiter
│   ├── models/              # SQLAlchemy models, one module per domain
│   │   ├── user.py          # User, Profile, UserSkill
│   │   ├── assessment.py    # Category, Question, QuestionOption, Attempt, Response, CategoryScore
│   │   ├── career.py        # Career, CareerCategory, CareerSkill, CareerReference
│   │   ├── roadmap.py       # Roadmap, RoadmapStage, RoadmapMilestone, LearningResource, ...
│   │   └── recommendation.py
│   ├── schemas/             # Pydantic request/response schemas per resource
│   ├── api/                 # blueprints: auth, profile, assessment, careers,
│   │                        # recommendations, skills_gap, roadmaps, admin, health
│   ├── services/            # business logic per domain (no HTTP concepts)
│   ├── recommendation/      # THE ENGINE — pure Python, zero Flask imports
│   │   ├── scoring.py       # factor calculations
│   │   ├── explanations.py  # explanation assembly
│   │   ├── engine.py        # orchestration: inputs → ranked recommendations
│   │   └── types.py         # plain dataclasses for engine inputs/outputs
│   └── seed/                # idempotent seed scripts (skills, careers, questions, roadmaps)
├── migrations/              # Alembic (via Flask-Migrate)
├── tests/                   # pytest: unit, integration, evaluation suite
├── .env.example
├── pyproject.toml           # dependencies + ruff/pytest config
└── wsgi.py
```

Layering rules:
- **Blueprints** parse/validate requests (Pydantic), call services, and return JSON. No business logic.
- **Services** implement workflows (e.g. `complete_attempt`, `record_skills`, `refresh_recommendations`) against models. No HTTP.
- **Models** declare tables, relationships, and constraints only.
- **Recommendation package** receives plain data (dataclasses loaded by a service) and returns scored results — independently unit-testable, swappable, and portable (charter Feature D).
- Central Flask error handlers convert exceptions and validation errors into the standard error envelope.

## 3. Frontend design

| Choice | Decision |
|---|---|
| Build tool | Vite (fast, current standard; CRA is deprecated) |
| Language | TypeScript (strict mode) |
| Styling | Tailwind CSS v4 with a small reusable UI kit |
| Routing | React Router |
| Server state | TanStack Query (caching, loading/error states, invalidation) |
| Forms | react-hook-form + zod (client-side mirrors server validation) |
| Auth state | Auth context hydrated from `GET /api/auth/me` |
| Linting | ESLint (+ jsx-a11y), type-check via `tsc` |

```
frontend/
├── src/
│   ├── api/            # typed fetch client + endpoint functions
│   ├── components/     # reusable UI: Button, Card, Badge, Input, Select, Progress,
│   │                   # Alert, EmptyState, Skeleton, Modal, Table
│   ├── features/       # feature modules: auth, profile, assessment, careers,
│   │                   # recommendations, roadmap, dashboard, compare, admin
│   ├── hooks/          # shared React hooks
│   ├── routes/         # route definitions + RequireAuth / RequireAdmin guards
│   ├── types/          # API types mirrored from schemas
│   └── App.tsx
├── index.html
├── package.json
└── vite.config.ts      # dev proxy: /api → http://127.0.0.1:5000
```

Pages/routes (student first, per charter section 5):
`/` landing · `/register` · `/login` · `/dashboard` · `/assessment` (+ `/assessment/results`) · `/careers` (+ `/careers/:slug`, `/careers/compare`) · `/recommendations` · `/roadmap/:careerSlug` · `/profile` (+ skills) · `/admin/*` (careers, skills, questions, resources, roadmaps).

## 4. API conventions

- Base path `/api`; JSON only; timestamps ISO 8601 UTC.
- **Auth:** session cookie `cna_session` (httpOnly, SameSite=Lax; see section 5). The SPA sends `credentials: 'include'`-equivalent same-origin requests.
- **Error envelope:**
  ```json
  { "error": { "code": "VALIDATION_ERROR", "message": "...", "details": ["..."] } }
  ```
  Codes: `VALIDATION_ERROR` (400), `UNAUTHENTICATED` (401), `FORBIDDEN` (403), `NOT_FOUND` (404), `CONFLICT` (409), `RATE_LIMITED` (429), `INTERNAL` (500).
- **Pagination:** `?page=1&per_page=20` (max 50) → `{ "items": [...], "page": 1, "per_page": 20, "total": 123, "total_pages": 7 }`.
- **CSRF protection:** every mutating request (POST/PUT/PATCH/DELETE) must carry the custom header `X-CSRF-Protection: 1`. Cross-site forms cannot set custom headers without a CORS preflight the API never grants, and SameSite=Lax blocks cross-site sends. Enforced in a Flask `before_request` hook and unit-tested.

### Endpoint catalogue (authoritative detail to be finalised per increment in docs/api-spec.md)
| Group | Endpoints |
|---|---|
| Health | `GET /api/health` |
| Auth | `POST /api/auth/register` · `POST /api/auth/login` · `POST /api/auth/logout` · `GET /api/auth/me` |
| Profile | `GET/PUT /api/profile/me` · `GET/PUT /api/profile/me/skills` |
| Assessment | `GET /api/assessment/questions` · `POST /api/assessment/attempts` · `GET /api/assessment/attempts/active` · `PUT /api/assessment/attempts/{id}/responses` · `POST /api/assessment/attempts/{id}/complete` · `GET /api/assessment/attempts/{id}/results` · `GET /api/assessment/me/latest` |
| Careers | `GET /api/careers` · `GET /api/careers/{slug}` · `GET /api/careers/{id}/skills` · `GET /api/careers/compare?ids=…` · `GET/POST/PUT /api/careers/{id}/interest` · `GET /api/careers/me/interests` |
| Recommendations | `GET /api/recommendations/me` · `POST /api/recommendations/me/refresh` |
| Skills gap | `GET /api/skills-gap?career_id=…` |
| Roadmaps | `GET /api/roadmaps/careers/{career_id}` · `GET /api/roadmaps/me` · `PUT /api/roadmap-progress/me/milestones/{id}` |
| Admin | CRUD under `/api/admin/...` for careers (+categories/skills/references), skills, questions/options, resources, roadmap content; `GET /api/admin/overview` |

## 5. Session and security architecture

Per ADR-0003 (user-confirmed 2026-10-14): **server-side sessions**.

- Flask-Session with the SQLAlchemy backend: session records in the database; cookie holds only an opaque session ID. Flags: `HttpOnly`, `SameSite=Lax`, `Secure` in production. Lifetime: 7 days sliding, refreshed on activity; logout deletes the record — immediate revocation.
- **Password hashing:** Werkzeug `generate_password_hash(method="scrypt")` (ADR-0004).
- **Rate limiting:** Flask-Limiter — login/register 5 per minute per IP; assessment writes 60 per hour per user.
- **Authorisation:** every user-scoped query filters by the session's user id (ownership built into the service layer); admin endpoints guarded by a role decorator checked server-side.
- **Input validation:** Pydantic schemas at the API boundary; SQLAlchemy parameterisation for all queries (no raw SQL string building).
- **Secrets:** `.env` only (git-ignored); committed `.env.example` documents variables.
- **Headers:** `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`; CSP added when the built SPA is served (Phase 13).
- Users' private records (profiles, skills, responses, recommendations, progress) are returned only to the owning session.

## 6. Configuration and environments

| Variable | Purpose |
|---|---|
| `FLASK_ENV` | `development` / `testing` / `production` |
| `SECRET_KEY` | Session signing key |
| `DATABASE_URL` | e.g. `mysql+pymysql://cna_app:***@127.0.0.1:3306/cna?charset=utf8mb4` |
| `SESSION_LIFETIME_MINUTES` | Session expiry |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | Credentials used once by the seed script to create the first admin (never a committed default) |
| `RATELIMIT_*` | Limiter settings |

`testing` config points at a separate `cna_test` schema created/dropped by the test suite.

## 7. Testing architecture

| Layer | Tool | Covers |
|---|---|---|
| Engine unit tests | pytest | Scoring math, explanations, ranking, determinism (pure functions, no DB) |
| Backend integration tests | pytest + Flask test client + real `cna_test` MySQL schema | Auth, ownership, assessment workflow, CRUD, validation, error codes |
| Evaluation suite | pytest (labelled subset) | Synthetic profile → expected ranking; consistency, coverage, sensitivity (docs/recommendation-methodology.md) |
| Frontend unit tests | Vitest + React Testing Library | Components, forms, hooks, states (loading/error/empty) |
| E2E | Playwright | Golden paths: register → assess → recommendations → roadmap → progress; admin CRUD |
| Static | ruff (backend), ESLint + tsc (frontend) | Lint/type hygiene |

## 8. Environments and serving strategy

- **Development:** Vite dev server (`localhost:5173`) proxies `/api` to Flask (`127.0.0.1:5000`) — one origin for the browser, so cookies work with no CORS ceremony.
- **Production target (Phase 13):** `npm run build` → Flask serves `frontend/dist` as static root with an SPA fallback route; serve via waitress (Windows-friendly) or gunicorn behind nginx; still single-origin, so sessions keep working unchanged.
- AI assistant (Feature J) is deferred; the external integration layer will only be introduced with an ADR covering provider, key management, privacy, and degradation.

## 9. Key flows

- **Register/login:** validate → hash password → create user + empty profile → issue server session; cookie returned.
- **Assessment:** start attempt → autosave each response → on complete, compute and persist category scores (service), then optionally trigger a recommendation refresh.
- **Recommendation refresh:** load latest completed attempt scores + user skills + interests + aspiration into engine input dataclasses → engine computes per-career factors, total, tier, explanations → replace stored recommendations for that attempt in one transaction.
- **Skills gap:** load career skill links + user skills → classify each required skill (`have`/`developing`/`planned`/`not_assessed`) → order core → supporting → attach roadmap milestone links where mapped.
- **Roadmap progress:** upsert per-milestone status with timestamps; dashboard reads aggregates.
