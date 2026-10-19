# Career Navigation Assistant (CNA)

An intelligent career guidance and development platform that helps Computer Science students explore technology careers through personalised recommendations, skills assessment, and career development guidance.

CNA aims to help students discover suitable technology career paths, understand why those careers may match their interests, identify required skills, and follow structured learning roadmaps.

**Project status:** Increment I1 (environment and application foundation) is complete: backend and frontend skeletons, database schema, and seed content are implemented and tested. Feature development follows the increment plan in [docs/project-plan.md](docs/project-plan.md).

## What CNA Will Do

* **Assess interests:** Explore interests across nine technology areas: software development, AI/ML, data, cloud computing, cybersecurity, networking, databases, UI/UX, and quality assurance.
* **Recommend careers:** Suggest relevant career paths using a deterministic, rule-based recommendation model with transparent explanations.
* **Analyse skills gaps:** Help students compare their existing and developing skills with the requirements of a chosen career.
* **Provide learning roadmaps:** Offer staged learning recommendations and progress tracking.
* **Support career exploration:** Provide a personal dashboard, career comparisons, and an administrator-managed career catalogue.

## Documentation

The `docs/` directory contains the project's planning and design documentation.

| Document                                                         | Description                                                                          |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [Requirements](docs/requirements.md)                             | Functional and non-functional requirements, including acceptance criteria            |
| [Architecture](docs/architecture.md)                             | System components, API conventions, security, and testing strategy                   |
| [Database Design](docs/database-design.md)                       | Proposed MySQL schema, entity relationships, integrity rules, and migration strategy |
| [Assessment Methodology](docs/assessment-methodology.md)         | Assessment instrument, interest categories, and scoring rules                        |
| [Recommendation Methodology](docs/recommendation-methodology.md) | Weighted scoring model, explanations, and evaluation plan                            |
| [Project Plan](docs/project-plan.md)                             | Development phases, increments, issues, acceptance criteria, and risks               |
| [Decision Log](docs/decisions.md)                                | Architecture and project decision records                                            |

## Technology Stack

* **Frontend:** React 19, TypeScript (strict), Tailwind CSS 4, and Vite
* **Backend:** Python and Flask REST API (SQLAlchemy 2 + Pydantic v2)
* **Database:** MySQL 8
* **Testing:** pytest, Vitest, and Playwright
* **Database migrations:** Alembic (via Flask-Migrate)
* **Version control:** Git and GitHub

## Repository Structure

```text
backend/     Flask REST API, SQLAlchemy models, Alembic migrations, seed content, and pytest tests
frontend/    React application (Vite + TypeScript + Tailwind), feature modules, and Vitest tests
docs/        Project requirements, architecture, methodologies, and planning documents
```

## Getting Started

### Prerequisites

* Python 3.13+
* Node.js 20+ with npm
* MySQL 8.0 running locally (service `MYSQL80` on Windows)
* Git

### 1. Database Bootstrap (once)

Using the MySQL root account, create the schemas and a least-privilege application user:

```sql
CREATE DATABASE cna CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
CREATE DATABASE cna_test CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
CREATE USER 'cna_app'@'localhost' IDENTIFIED BY '<app-password>';
CREATE USER 'cna_app'@'127.0.0.1' IDENTIFIED BY '<app-password>';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, DROP, INDEX, REFERENCES,
      LOCK TABLES, CREATE TEMPORARY TABLES
      ON cna.* TO 'cna_app'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, DROP, INDEX, REFERENCES,
      LOCK TABLES, CREATE TEMPORARY TABLES
      ON cna.* TO 'cna_app'@'127.0.0.1';
GRANT ALL PRIVILEGES ON cna_test.* TO 'cna_app'@'localhost';
GRANT ALL PRIVILEGES ON cna_test.* TO 'cna_app'@'127.0.0.1';
FLUSH PRIVILEGES;
```

`cna` is the development schema. `cna_test` is used automatically by the test suite and is never touched by development data.

### 2. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows   (bash: source .venv/Scripts/activate)
pip install -e . --group dev
copy .env.example .env        # bash: cp .env.example .env
```

Edit `backend/.env`: set `SECRET_KEY` to a long random string, put the MySQL application password into `DATABASE_URL`, and set `ADMIN_EMAIL`/`ADMIN_PASSWORD` (minimum 10 characters) for the bootstrap administrator account.

Apply the schema and seed the reference content (both commands are idempotent and safe to re-run):

```bash
flask db upgrade              # create tables via Alembic migrations
flask seed                    # 77 skills, 9 assessment categories, 27 questions, admin account
flask run                     # API at http://127.0.0.1:5000
```

Verify the API: `curl http://127.0.0.1:5000/api/health` should return `{"status": "ok"}`.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev                   # application at http://localhost:5174
```

The Vite dev server proxies `/api/*` requests to the Flask backend, so run both servers together. Port 5174 is configured explicitly because the Vite default (5173) may already be in use.

### 4. Tests and Checks

```bash
# Backend (runs against the cna_test schema)
cd backend && pytest

# Frontend
cd frontend && npm test
```

Static checks: `ruff check .` in `backend/`; `npm run lint` and `npm run typecheck` in `frontend/`.

### Default Accounts

The seed script creates one administrator account from `ADMIN_EMAIL`/`ADMIN_PASSWORD` in `backend/.env`. Student registration arrives with the authentication increment (I2).

## Important Notes

* **Career exploration, not prediction:** CNA is intended to support career exploration. Its assessments are not clinical instruments and do not predict employment outcomes or guarantee career suitability.
* **Transparent recommendations:** The initial recommendation approach is rule-based and deterministic. Machine-learning capabilities should not be claimed unless they are implemented and evaluated.
* **Honest evaluation:** Synthetic evaluation data, when used, will be clearly labelled. Results will not be fabricated or presented as real-world findings.

## Project Goal

CNA aims to make technology career exploration more structured and accessible by connecting students' interests with career information, skill requirements, and practical learning pathways.
