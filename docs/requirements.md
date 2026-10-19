# Career Navigation Assistant (CNA) — Requirements Specification

**Status:** Draft v0.1 — 2026-10-14 — awaiting review
**Source:** Project charter provided 2026-10-14

---

## 1. Introduction

### 1.1 Purpose
This document defines the functional and non-functional requirements for CNA, a web-based platform that helps Computer Science (CS) students and recent graduates explore technology careers and plan their professional development through structured assessments, explainable recommendations, skills-gap analysis, and personalised learning roadmaps.

### 1.2 Scope
CNA covers: user accounts and profiles; a career-interest assessment; a curated technology career catalogue; a rule-based, explainable recommendation engine; skills-gap analysis; personalised roadmaps with progress tracking; a personal dashboard; career comparison; and an administrative interface for content management.

### 1.3 Non-goals and disclaimers
- The assessment supports **career exploration only**. It is not a clinical or psychological instrument, and CNA must never claim to predict professional suitability or employment outcomes.
- CNA does not provide job listings, salary data, or live labour-market feeds.
- CNA must not claim to use AI/ML anywhere (UI, docs, report) unless a specific AI/ML component is actually implemented and tested.

### 1.4 Definitions
| Term | Meaning |
|---|---|
| Assessment | Structured questionnaire measuring interest across nine technology categories |
| Attempt | One sitting of the assessment (can be retaken) |
| Category | One of nine technology interest areas (e.g. AI & Machine Learning) |
| Career | A catalogue entry (e.g. Machine Learning Engineer) with requirements and a roadmap |
| Roadmap | Staged learning plan for a career, composed of milestones |
| Milestone | A trackable learning unit within a roadmap stage |
| Skills gap | Difference between a user's recorded skills and a career's required skills |
| Recommendation | A scored, ranked, explained career suggestion produced by the engine |

## 2. Users
- **Primary:** CS students choosing and preparing for technology careers.
- **Secondary:** recent CS graduates; students exploring specialisations; individuals transitioning into technology.
- **Administrators:** maintain careers, skills, assessment content, and learning resources.
- **Supervisors/reviewers:** read documentation and evaluation evidence; they are not application users.

Privacy rule: a student can only ever read their own records. Administrators manage platform content, not student data.

## 3. Functional requirements

Priority: **M** = must (core for evaluation), **S** = should (included unless time forces descoping), **C** = could (nice-to-have).

### Feature A — User authentication and profile
| ID | Pri | Requirement | Acceptance criteria |
|---|---|---|---|
| FR-A1 | M | Register with name, email, password | Email unique (case-insensitive); password ≥ 10 chars; duplicate email → 409 |
| FR-A2 | M | Log in / log out | Invalid credentials → 401 without revealing which field failed; logout invalidates the server-side session |
| FR-A3 | M | Session-based authentication | httpOnly cookie; authenticated routes reject missing/expired sessions with 401 |
| FR-A4 | M | Manage profile | Education level, year of study, graduation year, career aspiration text + aspiration category, learning preference, bio; updates validated and persisted |
| FR-A5 | M | Record skills | Per-skill status `has` / `learning` / `want` plus optional proficiency 1–5; bulk update endpoint |
| FR-A6 | M | Access control | Every API enforces ownership through user-scoped queries; admin APIs require `admin` role server-side |
| FR-A7 | M | Password storage | Strong key-derivation hash (ADR-0004); password never returned by any endpoint |
| FR-A8 | S | Account deletion | Removes the account and all personal records via FK cascade |

### Feature B — Career discovery assessment
| ID | Pri | Requirement | Acceptance criteria |
|---|---|---|---|
| FR-B1 | M | 9 categories × 3 questions; each question has 4 ordered options scored 0–3; all stored in the database | Questions and options editable by admin without code changes |
| FR-B2 | M | Attempt lifecycle: start → answer (autosaved) → complete | Completion requires all active questions answered; an in-progress attempt is resumable |
| FR-B3 | M | Scoring | Per-category raw score and normalized score (0–100) persisted on completion |
| FR-B4 | M | Retakes | A new attempt can be started; recommendations use the latest completed attempt |
| FR-B5 | S | Results view | Category score breakdown with plain-language interpretation |

### Feature C — Technology career catalogue
| ID | Pri | Requirement | Acceptance criteria |
|---|---|---|---|
| FR-C1 | M | At least 16 seeded careers | Each has summary, description, responsibilities, foundational knowledge, related technologies, suggested projects, and references |
| FR-C2 | M | Careers linked to categories (primary/secondary) and skills (core/supporting) | Weights stored in the database and used by the engine |
| FR-C3 | M | Browse, search, filter | Filter by category, search by text; paginated; unpublished careers hidden from students |
| FR-C4 | M | Career detail page | All content and references render; loading, error, and empty states present |
| FR-C5 | S | Save interests | Mark careers `interested` / `following`; list own saved interests |

### Feature D — Recommendation engine
| ID | Pri | Requirement | Acceptance criteria |
|---|---|---|---|
| FR-D1 | M | Weighted rule-based scoring over assessment scores, recorded skills, saved interests, and stated aspiration | Implements the formula in docs/recommendation-methodology.md exactly |
| FR-D2 | M | Deterministic | Identical inputs produce an identical ranked output (unit-tested) |
| FR-D3 | M | Explanations | Factor-level breakdown: matched interests, matched skills, development areas, saved-interest and aspiration notes; no per-user hard-coded text |
| FR-D4 | M | Isolation and testability | Engine is a pure-Python package with no Flask/UI imports, unit-tested independently |
| FR-D5 | M | Ranked list with tiers | strong ≥ 70, moderate 50–69, explore < 50; top 8 returned |
| FR-D6 | M | Refresh on demand | Recomputes from the latest completed attempt; results stored per attempt |
| FR-D7 | M | Honesty | No ML/AI claims in UI or docs unless a component is actually implemented |

### Feature E — Skills-gap analysis
| ID | Pri | Requirement | Acceptance criteria |
|---|---|---|---|
| FR-E1 | M | Compare recorded skills against a career's requirements | Every required skill classified: `have` / `developing` / `planned` / `not_assessed` |
| FR-E2 | M | Unassessed is not a weakness | Not-assessed skills displayed distinctly, never labelled as missing or weak |
| FR-E3 | M | Learning priorities | Core skills ordered before supporting skills |
| FR-E4 | S | Link to roadmap | Gap items reference matching roadmap milestones where they exist |

### Feature F — Personalised roadmaps
| ID | Pri | Requirement | Acceptance criteria |
|---|---|---|---|
| FR-F1 | M | Roadmap per career with stages: foundation → core skills → tools → projects → portfolio → next steps | Stage and milestone structure per database design |
| FR-F2 | M | Milestones carry resources | Resources have verified URLs; project milestones flagged |
| FR-F3 | M | Progress tracking | Per milestone: not started / in progress / completed, with timestamps; persists across sessions |
| FR-F4 | M | Follow a career | Following activates roadmap tracking; roadmap view shows percentage complete |

### Feature G — Personalised dashboard
| ID | Pri | Requirement | Acceptance criteria |
|---|---|---|---|
| FR-G1 | M | Central overview | Profile completeness, assessment status, top recommendations with reasons, followed careers, roadmap progress |
| FR-G2 | M | States | Every widget has loading, error, and empty states |
| FR-G3 | M | Responsive | Usable from 360 px wide to desktop |

### Feature H — Career comparison
| ID | Pri | Requirement | Acceptance criteria |
|---|---|---|---|
| FR-H1 | M | Compare 2–3 careers side by side | Responsibilities, skills, foundational knowledge, learning activities in aligned rows |
| FR-H2 | S | Personal context | Matched-skills count per career for the signed-in user |

### Feature I — Administrative management
| ID | Pri | Requirement | Acceptance criteria |
|---|---|---|---|
| FR-I1 | M | Careers CRUD (categories, skill links, references, publish flag) | Admin-only; validation errors returned in the standard envelope |
| FR-I2 | M | Skills catalogue CRUD | Deactivate rather than delete when a skill is in use |
| FR-I3 | M | Assessment questions/options CRUD with activate/deactivate | Existing responses preserved (FK RESTRICT) |
| FR-I4 | M | Learning resources CRUD | URL format validated; verified flag maintained |
| FR-I5 | M | Roadmap content management | Stages, milestones, and linked resources editable |
| FR-I6 | M | Protection | All admin APIs role-checked server-side; students → 403; admin UI hidden from students |

### Feature J — Optional AI assistant (deferred)
| ID | Pri | Requirement | Acceptance criteria |
|---|---|---|---|
| FR-J1 | C | Conversational career assistant | Only with an approved provider, secure key handling, privacy safeguards, and graceful degradation; the app must remain fully usable without it |

## 4. Non-functional requirements
| ID | Area | Requirement |
|---|---|---|
| NFR-1 | Security | OWASP-aligned: parameterised ORM queries; server-side input validation; authentication and authorisation on every endpoint; secrets via .env only; rate limiting on auth endpoints; strong password hashing; non-revealing error messages |
| NFR-2 | Privacy | Collect only data used by features; strict per-user data isolation; account deletion removes personal data; no third-party analytics |
| NFR-3 | Accessibility | WCAG 2.1 AA target: keyboard navigable, semantic HTML, labelled controls, contrast ≥ 4.5:1, visible focus states |
| NFR-4 | Usability | Consistent component library; clear navigation; readable career content; progress indicators; useful empty and error states |
| NFR-5 | Reliability | Foreign-key constraints and transactions; forward-only migrations; stable JSON error envelope |
| NFR-6 | Maintainability | Modular architecture; typed frontend; linting; maintained decision log; docs updated each phase |
| NFR-7 | Testability | Unit, integration, and E2E layers; core workflows covered; each layer runs with one command |
| NFR-8 | Performance | API p95 < 500 ms on dev hardware; list endpoints paginated (default 20, max 50) |
| NFR-9 | Portability | Runs on the Windows dev machine per documented setup; configuration via environment variables |
| NFR-10 | Determinism | Recommendation output is a pure function of stored inputs and documented weights |

## 5. Data requirements
- Seed content (careers, skills, questions, roadmaps, resources) is authored during development from credible public sources; each career records at least 2 references with valid URLs.
- No runtime web scraping. No fabricated statistics. Evaluation profiles are synthetic and clearly labelled as such.

## 6. Constraints
- Stack fixed by charter: React + TypeScript + Tailwind CSS; Python + Flask REST; MySQL; Git/GitHub; environment-variable configuration; migration tooling (see ADR-0002).
- Dev machine: Windows 10, Python 3.14, Node 24, MySQL 8.0.46 (service `MYSQL80` currently stopped; root password to be reset — project plan issue I1.1).
- Single-instance deployment initially.

## 7. Assumptions
- The latest completed assessment attempt drives recommendations.
- Career and skill content is maintained by administrators, seeded initially by the developer.
- Users run modern browsers.

## 8. Out of scope (v1)
Job listings; live labour-market data; email verification and password-reset email (documented limitation); native mobile apps; multi-language UI; studies involving real user data; ML training on user data.

## 9. Traceability
| Feature | Plan increment | Primary test layers |
|---|---|---|
| A — Auth & profile | I2 | unit, integration, E2E |
| B — Assessment | I3 | unit (scoring), integration |
| C — Catalogue | I4 | integration, seed checks |
| D — Recommendations | I5 | unit (engine), evaluation suite |
| E — Skills gap | I6 | unit, integration |
| H — Comparison | I6 | integration, component |
| F — Roadmaps | I7 | integration, E2E |
| G — Dashboard | I8 | component, E2E |
| I — Admin | I9 | integration, authorisation |
| J — AI assistant | deferred | — |
