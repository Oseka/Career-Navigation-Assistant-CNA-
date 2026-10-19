# CNA — Assessment Design and Scoring Methodology

**Status:** Draft v0.1 — 2026-10-14 — awaiting review

---

## 1. Purpose and disclaimer

The assessment measures a student's **interest** across nine technology areas to support career *exploration*. It is a self-report instrument designed by the development team; it is **not** a validated psychological instrument, does not measure ability, and must not be presented as predicting professional suitability or outcomes. This disclaimer appears in the assessment UI and the report.

## 2. Categories

| Key | Category | Focus of statements |
|---|---|---|
| `software_dev` | Software & Application Development | Building programs, solving problems with code, shipping features |
| `ai_ml` | Artificial Intelligence & Machine Learning | Models, training/evaluating ML, applied intelligence |
| `data_analysis` | Data Analysis & Data Science | Working with datasets, finding patterns, statistics, visualisation |
| `cloud` | Cloud Computing & Infrastructure | Cloud platforms, provisioning, scalable infrastructure |
| `security` | Cybersecurity | Protecting systems, threats and vulnerabilities, ethical hacking |
| `networking` | Networking & Systems | Networks, servers, operating systems, connectivity |
| `database` | Database Management | Designing schemas, querying, managing data stores |
| `uiux` | UI & UX Design | Interfaces, usability, design systems, user research |
| `qa` | Software Testing & Quality Assurance | Breaking things systematically, test design, quality gates |

## 3. Instrument format

- **27 questions**: 3 per category, mixed presentation order (order stored in `question_order`).
- Each question is a first-person **interest statement** with a **4-point agreement scale** (forced choice — no neutral midpoint):
  | Option | Score |
  |---|---|
  | Strongly agree | 3 |
  | Agree | 2 |
  | Disagree | 1 |
  | Strongly disagree | 0 |
- Every question loads on **exactly one category** (no cross-category questions — keeps the scoring model transparent and testable).
- All questions and options live in the database (FR-B1); administrators can edit wording or activate/deactivate questions without code changes.

### Example questions (final wording authored in increment I3)

1. `software_dev` — "I enjoy designing and writing programs that solve everyday problems."
2. `ai_ml` — "I find it exciting to train and evaluate models that learn from data."
3. `qa` — "I like systematically trying to break software to find defects before users do."

## 4. Scoring rules

For a completed attempt, per category *c*:

```
raw_score(c)        = Σ option score over that category's active questions   (range 0–9)
normalized_score(c) = raw_score(c) / (3 × number_of_active_questions(c)) × 100
```

- Scores are computed by the assessment service on completion and persisted in `assessment_category_scores` (raw + normalized).
- Deactivated questions are excluded from both numerator and denominator — historical scores stay interpretable.
- Only whole-option responses count; there are no partial answers.

## 5. Attempt lifecycle

1. `POST /api/assessment/attempts` → new `in_progress` attempt (a user may hold at most one).
2. Responses autosave as answered (`UNIQUE (attempt_id, question_id)` upsert), so the attempt is resumable.
3. `POST .../complete` → service verifies **every active question is answered**, then computes and persists category scores in one transaction and sets `completed_at`.
4. Retake → new attempt. **The latest completed attempt drives recommendations.** Older attempts and their scores are retained for the user's history.

Estimated completion time: 10–15 minutes.

## 6. Content maintenance policy (admin)

- Editing question/option **wording** affects future attempts only; existing responses reference immutable rows (FK RESTRICT).
- Changing an option's **score_value** likewise affects future attempts; a documented limitation (§8).
- Deactivation (`is_active = 0`) hides a question from the instrument while preserving history.

## 7. Interpretation in the product

- Category scores feed the recommendation engine's interest factor (docs/recommendation-methodology.md).
- The results screen shows each category's normalized score with a short plain-language description, and a reminder that scores reflect self-reported interest, not skill.

## 8. Limitations

- Self-report; responses can be influenced by mood or self-image.
- Statement pool and category weights are designed, not statistically validated.
- No norming against a population sample; scores are meaningful within one user's profile, not across users.
- The instrument is short (27 items) by design — acceptable for exploration, a limitation to state in the report.
