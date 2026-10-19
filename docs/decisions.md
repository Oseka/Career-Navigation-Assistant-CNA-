# CNA — Decision Log (ADR-style)

Decisions are recorded as work progresses (charter section 13). Format: context → decision → consequences. Statuses: **Accepted** / Proposed / Superseded.

---

## ADR-0001 — Repository layout: single repo, `backend/` + `frontend/`
**Date:** 2026-10-14 · **Status:** Accepted
A single repository keeps the Flask API and React SPA versioned together, which suits a solo final-year project and unified history. Both toolchains live side by side with their own lock files. *Consequences:* any future CI must run both test suites.

## ADR-0002 — Data layer: MySQL 8 + SQLAlchemy 2 + Flask-Migrate (Alembic) + PyMySQL
**Date:** 2026-10-14 · **Status:** Accepted
The charter mandates MySQL and asks for a Python-compatible access/migration approach without incompatible or unnecessary ORMs. SQLAlchemy is the standard Flask companion; Flask-Migrate wraps Alembic for migrations; PyMySQL is pure-Python (no C build issues on Windows). *Consequences:* database URL pattern `mysql+pymysql://...`; migrations are forward-only Alembic revisions.

## ADR-0003 — Authentication: server-side sessions (httpOnly cookies) over JWT
**Date:** 2026-10-14 · **Status:** Accepted (user-confirmed)
Sessions are stored server-side (Flask-Session, SQLAlchemy backend); the cookie carries only an opaque ID, flagged HttpOnly + SameSite=Lax (+ Secure in production). Logout deletes the session record = immediate revocation; no token-theft-via-XSS window; simple to test. CSRF on mutations is handled by requiring the `X-CSRF-Protection` custom header (cross-site forms cannot set it). *Consequences:* the SPA is served same-origin in dev (Vite proxy) and production (Flask serves the build); a future cross-origin deployment would need CSRF-token upgrade and cookie domain review.

## ADR-0004 — Password hashing: Werkzeug scrypt
**Date:** 2026-10-14 · **Status:** Accepted
`werkzeug.security.generate_password_hash(method="scrypt")` — memory-hard, OWASP-acceptable, and already a Flask dependency (no extra package). *Consequences:* upgrade path to argon2id exists if requirements change; hashes carry their parameters, so verification stays forward-compatible.

## ADR-0005 — Request validation: Pydantic v2 schemas at the API boundary
**Date:** 2026-10-14 · **Status:** Accepted
One validation library for all request/response shapes; validation errors map to the standard envelope (`VALIDATION_ERROR`, 400). *Consequences:* schemas are the contract documentation source for docs/api-spec.md.

## ADR-0006 — Frontend stack: Vite + React + TypeScript (strict) + Tailwind CSS v4
**Date:** 2026-10-14 · **Status:** Accepted
Vite is the current standard (CRA deprecated); Tailwind v4 for utility styling with a small reusable component kit (charter section 9); TanStack Query for server state (caching, invalidation, loading/error states); react-hook-form + zod for forms mirroring server validation. *Consequences:* a handful of well-known dependencies, each with a concrete job.

## ADR-0007 — Testing stack
**Date:** 2026-10-14 · **Status:** Accepted
pytest (unit + integration against a real `cna_test` MySQL schema), Vitest + React Testing Library (components), Playwright (E2E golden paths), ruff + ESLint + tsc (static). *Consequences:* each layer runs with one command; integration tests require MySQL locally, which the machine already has.

## ADR-0008 — Recommendation engine: deterministic rule-based weighted scoring; no ML claims
**Date:** 2026-10-14 · **Status:** Accepted
The charter requires an explainable model first and forbids AI/ML claims without an implemented, tested component. The engine is a pure-Python package (no Flask imports) with documented factors/weights and an evaluation suite using labelled synthetic profiles. *Consequences:* introducing ML later requires a new ADR + evaluation method (charter Feature D).

## ADR-0009 — AI assistant (Feature J): deferred
**Date:** 2026-10-14 · **Status:** Accepted
Not in the initial build. Re-entry gate: approved provider, secure key management, privacy review, graceful degradation — documented in a new ADR before any integration work.

## ADR-0010 — Time and IDs
**Date:** 2026-10-14 · **Status:** Accepted
All datetimes stored and served in UTC, ISO 8601 in the API; entity IDs are database-assigned integers (no UUIDs needed for a single-instance system). *Implementation note (I1.4):* every pooled connection sets `time_zone = '+00:00'` via the PyMySQL `init_command`, so `CURRENT_TIMESTAMP` defaults write UTC.

## ADR-0011 — Dropped legacy `cna` schema left by the previous project
**Date:** 2026-10-19 · **Status:** Accepted (user-confirmed: back up, then drop)
During I1.4 the first Alembic autogeneration revealed that the dev `cna` schema still contained nine tables from the previous, deleted CNA application (`users`, `mentors`, `community_posts`, etc.), because `CREATE DATABASE IF NOT EXISTS` had silently preserved it during the I1.1 bootstrap. The charter requires treating CNA as a brand-new project that must not depend on previous artifacts, and the legacy schema would have corrupted the new migrations. *Decision:* dump all nine tables to `C:\Users\HP\Documents\cna_old_schema_backup_2026-10-19.sql` (outside the repository), then drop and recreate `cna` empty before generating migration 0001. *Consequences:* the new schema starts clean and matches docs/database-design.md exactly; the old data remains recoverable only from the backup file.

## ADR-0012 — Seeds are insert-only by natural key
**Date:** 2026-10-19 · **Status:** Accepted
Seed scripts (`flask seed`, `flask seed-skills`, `flask seed-assessment`, `flask seed-admin`) insert missing rows by natural key (skill name; category key; category+question order) and never modify existing rows, so administrator edits survive re-runs. The single documented exception is `seed-admin`, which is a bootstrap command: it always resets the admin password and role from `ADMIN_EMAIL`/`ADMIN_PASSWORD`. Content corrections during development are made by dropping the disposable dev schema and re-seeding, not by seed updates.

