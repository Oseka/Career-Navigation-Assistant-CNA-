# Career Navigation Assistant (CNA)

An intelligent career guidance and development platform that helps Computer Science students explore technology careers through personalised recommendations, skills assessment, and career development guidance.

CNA aims to help students discover suitable technology career paths, understand why those careers may match their interests, identify required skills, and follow structured learning roadmaps.

**Project status:** Planning and documentation phase. Phases 1–2 are complete, with documentation awaiting review. Application development is planned for Phase 3.

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

## Planned Technology Stack

* **Frontend:** React, TypeScript, Tailwind CSS, and Vite
* **Backend:** Python and Flask REST API
* **Database:** MySQL 8
* **Testing:** pytest, Vitest, and Playwright
* **Database migrations:** Alembic
* **Version control:** Git and GitHub

The stack and implementation details will be confirmed as development progresses.

## Planned Repository Structure

```text
backend/     Flask REST API, recommendation engine, migrations, seeds, and tests
frontend/    React application, components, feature modules, and tests
docs/        Project requirements, architecture, methodologies, and planning documents
```

The application structure will be established during the implementation phase.

## Getting Started

The application setup and execution instructions will be added during Phase 3, when the initial application skeleton is implemented.

The planned initial environment tasks include database configuration, database initialisation, and application bootstrap.

## Important Notes

* **Career exploration, not prediction:** CNA is intended to support career exploration. Its assessments are not clinical instruments and do not predict employment outcomes or guarantee career suitability.
* **Transparent recommendations:** The initial recommendation approach is rule-based and deterministic. Machine-learning capabilities should not be claimed unless they are implemented and evaluated.
* **Honest evaluation:** Synthetic evaluation data, when used, will be clearly labelled. Results will not be fabricated or presented as real-world findings.

## Project Goal

CNA aims to make technology career exploration more structured and accessible by connecting students' interests with career information, skill requirements, and practical learning pathways.
