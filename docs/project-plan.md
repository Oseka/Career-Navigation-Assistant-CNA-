# CNA — Phased Implementation Plan

**Status:** Draft v0.1 — 2026-10-14 — awaiting review

---

## 1. Working agreements

- **Small, reviewed increments.** Each increment ends with working, tested software plus updated docs. No large unreviewed code drops (charter section 15).
- **Definition of done (per issue):** code + tests (appropriate layer) + docs updated + verified locally + changes reviewed by the project owner.
- **Honesty:** no feature is marked complete before it is verified; no test result is reported that was not executed; synthetic data is labelled synthetic.
- **Just-in-time detail:** I1–I3 are broken into concrete issues below; I4–I12 are defined at feature level and broken into issues at the start of each increment.
- Docs and the decision log are updated as part of the increment that changes them.

## 2. Increment map (charter phases → increments)

| Increment | Charter phase | Scope | Depends on |
|---|---|---|---|
| I0 | 1–2 | Requirements, architecture, DB design, methodologies, plan (this document set) | — |
| I1 | 3 | Environment & foundation (MySQL reset, backend + frontend skeletons, migrations infra, seed framework) | I0 |
| I2 | 4 | Authentication, profile, skills self-service | I1 |
| I3 | 5 | Assessment module | I1 (content), I2 (auth) |
| I4 | 6 | Career catalogue + skills data + seed content | I1 |
| I5 | 7 | Recommendation engine + evaluation suite | I3, I4 |
| I6 | 8 | Skills-gap analysis + career comparison | I4 (I5 for personal context) |
| I7 | 9 | Roadmaps + progress tracking | I4, I2 |
| I8 | 10 | Dashboard | I2–I7 |
| I9 | 11 | Administrative interface | I2, I4 |
| I10 | 12 | Testing expansion, security review, accessibility pass, refinement | I2–I9 |
| I11 | 13 | Documentation finalisation, deployment preparation | I10 |
| I12 | 14 | Evaluation evidence + final-year report materials | I11 |

## 3. Detailed issues — I1: Environment & foundation

| Issue | Objective | Acceptance criteria | Verification |
|---|---|---|---|
| I1.1 | **Reset MySQL root password; create `cna` schema + least-privilege `cna_app` user** (user confirmed root password is lost) | `mysql -u cna_app -p … -e "SELECT 1"` succeeds against `cna`; credentials exist only in `backend/.env` (git-ignored); MYSQL80 service starts | Manual + `backend/.env` present, never committed |
| I1.2 | Backend skeleton: venv, Flask app factory, env config, `GET /api/health`, Flask-Migrate initialised, pytest smoke test | `flask run` boots; `pytest` passes; health endpoint returns JSON | `pytest`, curl health |
| I1.3 | Frontend skeleton: Vite + React + TS + Tailwind, router, app shell, typed API client, Vite `/api` proxy, Vitest smoke test | `npm run dev` renders shell; proxy reaches `/api/health`; `npm run test` passes | `npm run test`, browser check |
| I1.4 | Seed framework + first seeds: skills catalogue, assessment categories/questions, admin user from env | Seeds idempotent (re-run safe); counts logged; admin login works | Run seeds twice, compare counts |
| I1.5 | README setup instructions (both apps, DB, seeds, tests) | A cold start following the README reaches a running app | Fresh-clone simulation |

## 4. Detailed issues — I2: Authentication, profile, skills

| Issue | Objective | Acceptance criteria | Verification |
|---|---|---|---|
| I2.1 | `users`/`profiles`/`user_skills` models + Alembic migration | Migration runs clean; schema matches database-design.md | `flask db upgrade`; introspection |
| I2.2 | Register/login/logout/me endpoints; Flask-Session; CSRF header check; rate limiting | FR-A1–A3 acceptance criteria met; 401/403/409/429 behaviours correct | Integration tests |
| I2.3 | Profile + skills self-service APIs (Pydantic validated) | FR-A4–A5 met; ownership enforced (user A cannot read/write user B) | Integration tests incl. negative cases |
| I2.4 | Frontend auth pages, route guards, profile & skills UI | Register→login→profile flow usable; guards redirect; states present | Component tests + Playwright happy path |
| I2.5 | Docs updated: api-spec (auth/profile), setup additions | Docs match implementation | Review |

## 5. Detailed issues — I3: Assessment module

| Issue | Objective | Acceptance criteria | Verification |
|---|---|---|---|
| I3.1 | Assessment models + migration (categories/questions/options/attempts/responses/scores) | Schema matches design; FK rules as documented | Migration + introspection |
| I3.2 | Final question set authored (27 questions, 9 categories) and seeded | Every category ≥ 3 active questions; options scored 0–3 | Seed check + review |
| I3.3 | Assessment APIs: questions, start/active, autosave responses, complete, results, latest | FR-B1–B4 met; single in-progress attempt; completion validates completeness | Integration tests |
| I3.4 | Scoring service implementing assessment-methodology.md | Formulas exact; deactivated questions excluded | Unit tests |
| I3.5 | Assessment UI: category-grouped flow, progress, autosave, resumable, results screen | FR-B5 met; usable keyboard-only; autosave survives reload | Component tests + Playwright |

## 6. Feature-level scope — I4 through I12

- **I4 — Catalogue:** career/category/skill/reference models + migration; 16 careers seeded with ≥ 2 credible references each and category/skill weights; public APIs (list/filter/search/paginate, detail, compare data); browse + detail pages with states.
- **I5 — Recommendation engine:** engine package (scoring, explanations, ranking); refresh endpoint + storage; recommendations page with explanation cards; full evaluation suite from recommendation-methodology.md §7 passing.
- **I6 — Skills gap + comparison:** gap service/API (classification + priorities + roadmap links); comparison API (2–3 careers, personal context); gap panel + compare page.
- **I7 — Roadmaps:** roadmap/stage/milestone/resource models + migration; roadmaps seeded for all careers; follow + progress APIs; roadmap UI with progress tracking and percentage complete.
- **I8 — Dashboard:** aggregate endpoint(s); widgets per FR-G1 with loading/error/empty states; responsive layout check.
- **I9 — Admin:** admin APIs with role guard (FR-I1–I5); admin UI sections; authorisation test matrix (student→403 everywhere, anonymous→401).
- **I10 — Hardening:** expanded E2E (register→assess→recommend→roadmap→progress; admin CRUD); OWASP checklist pass; accessibility audit (keyboard, contrast, labels, focus); pagination + performance sanity; bug fixes.
- **I11 — Docs & deployment:** api-spec.md complete; testing report with real results; known limitations; production build served by Flask (single origin), verified end-to-end.
- **I12 — Evaluation & report:** evaluation-results.md from the I5/I10 suites (synthetic, labelled); screenshots; report outline mapping requirements → implementation → evidence.

## 7. Risk register

| # | Risk | Mitigation |
|---|---|---|
| R1 | Windows/MySQL environment friction (root password already lost) | I1.1 is the first issue; reset procedure documented; fallback = reinstall MySQL 8 |
| R2 | Seed content volume (16 careers × full roadmaps is heavy) | Careers first (I4), roadmaps staged (I7); content authored from cited public sources; can descope to 10–12 careers if needed (documented) |
| R3 | Recommendation validity questioned in evaluation | Methodology + weights + evaluation plan documented up front; limitations stated honestly |
| R4 | Security added too late | Security built in from I2 (sessions, CSRF, rate limits, ownership); I10 is review, not retrofit |
| R5 | Scope creep (AI assistant, extras) | Feature J explicitly deferred behind an ADR gate; priorities M/S/C enforced at increment planning |
| R6 | Time pressure near report deadline | Each increment delivers usable value independently; descope order: Could → Should items, never Must |

## 8. Change control

Changes to requirements, methodology (weights, formulas, tiers), or the data model are made by updating the relevant document **first**, then implementing — keeping docs authoritative for the report.
