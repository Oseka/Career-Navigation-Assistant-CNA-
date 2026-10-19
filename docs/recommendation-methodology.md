# CNA — Career Recommendation Methodology

**Status:** Draft v0.1 — 2026-10-14 — awaiting review

---

## 1. Design goals

Per charter Feature D, the engine is an **explainable, deterministic, rule-based weighted-scoring model**:

- Every score is traceable to stored user data and documented weights.
- Identical inputs always produce identical output (unit-tested).
- Explanations are generated from the factors themselves — no per-user hard-coded text, no LLM.
- No ML/AI is used or claimed; introducing ML later would require a new use case, evaluation method, and ADR.

The engine is a pure-Python package (`backend/app/recommendation/`): it receives plain dataclasses and returns results, with no Flask, database, or UI imports, so it is independently testable (FR-D4).

## 2. Inputs

| Input | Source |
|---|---|
| Category interest scores (0–100) | Latest completed assessment attempt (`assessment_category_scores`) |
| Recorded skills | `user_skills` rows: `has` / `learning` / `want` (+ proficiency) |
| Saved career interests | `career_interests` (`interested` / `following`) |
| Stated aspiration | `profiles.aspiration_category_id` (+ free text) |
| Career model | `career_categories` (primary 1.00 / secondary 0.60) and `career_skills` (core / supporting) |

## 3. Factors

For each published career *c* and user *u*:

**F1 — Interest match (weight 0.45)**
```
interest(c) = Σ_cat w(cat,c) × normalized_score(cat,u) / Σ_cat w(cat,c)        → 0–100
```
where w(cat,c) is the career–category weight. A career with categories {ai_ml: 1.00, data_analysis: 0.60} weights AI interest most heavily.

**F2 — Skills match (weight 0.35)**
```
credit(status) = has → 1.0 · learning → 0.4 · want → 0.1 · absent → 0.0
weighted_have(c) = Σ over career_skills: importance_weight × credit(user status)
   where importance_weight: core = 1.0, supporting = 0.5
skills(c) = weighted_have(c) / Σ importance_weight over career_skills × 100     → 0–100
```
Partial credit for `learning`/`want` reflects genuine momentum; absent skills score 0 but are reported as **not assessed**, never as weakness (FR-E2).

**F3 — Explicit interest (weight 0.15)**
```
explicit(c) = 100 if u saved/follows c, else 0
```

**F4 — Aspiration match (weight 0.05)**
```
aspiration(c) = 100 if aspiration_category is primary for c
                60  if it is secondary
                0   otherwise (including no aspiration set)
```

**Total score**
```
total(c) = 0.45×interest + 0.35×skills + 0.15×explicit + 0.05×aspiration       → 0–100
```

Weights are constants in one configuration module (single source of truth); changing them is a documented decision-log update plus updated tests — never an ad-hoc tweak.

## 4. Worked example

User: scores {ai_ml: 85, data_analysis: 70, software_dev: 55, database: 60, …}; skills `has`: Python, SQL, Git; `learning`: Pandas; saved `following`: Machine Learning Engineer; aspiration category `ai_ml`.

Career **Machine Learning Engineer** — categories: ai_ml (1.00), data_analysis (0.60); skills: core = Python, ML frameworks, Statistics & probability, Model evaluation; supporting = SQL, Git, Pandas, Cloud basics.

```
interest   = (1.00×85 + 0.60×70) / 1.60                 = 79.4
skills     = (1.0 + 0.5 + 0.5 + 0.4×0.5) / (4×1.0 + 4×0.5) = 2.2/6.0 = 36.7
             (has Python core; has SQL, Git supporting; learning Pandas)
explicit   = 100    (following)
aspiration = 100    (ai_ml is primary)
total      = 0.45×79.4 + 0.35×36.7 + 0.15×100 + 0.05×100 = 68.6 → tier "moderate"
```

## 5. Explanations

Each stored recommendation carries an `explanation` JSON — a snapshot of the factors:

```json
{
  "factors": [
    {"key": "interest", "label": "Interest alignment", "score": 79.4, "weight": 0.45,
     "contribution": 35.7, "details": ["Strong interest in AI & Machine Learning (85/100)", "Solid interest in Data Analysis (70/100)"]},
    {"key": "skills", "label": "Skills match", "score": 36.7, "weight": 0.35,
     "contribution": 12.8, "details": ["1 of 4 core skills recorded: Python", "2 of 4 supporting skills recorded: SQL, Git"]},
    {"key": "explicit", "label": "Saved interest", "score": 100, "weight": 0.15,
     "contribution": 15.0, "details": ["You are following this career"]},
    {"key": "aspiration", "label": "Stated aspiration", "score": 100, "weight": 0.05,
     "contribution": 5.0, "details": ["Matches your aspiration category: AI & Machine Learning"]}
  ],
  "development_areas": ["ML frameworks — not yet recorded", "Statistics & probability — not yet recorded", "Model evaluation — not yet recorded"],
  "missing_data_notes": ["Record your skills to sharpen this match"]
}
```

Rules: `details` strings are assembled from factor data via templates (same input → same text); `development_areas` lists required core skills with no `has`/`learning` record; notes appear when inputs are sparse (no skills, no aspiration, no saved interests) so the UI never overstates confidence.

## 6. Ranking, tiers, and tie-breaking

- Rank all published careers by `total` descending.
- Tiers: **strong ≥ 70**, **moderate 50–69**, **explore < 50**. Top 8 returned (FR-D5).
- Ties broken deterministically: interest factor, then skills factor, then career title (A–Z).

## 7. Evaluation plan (charter objective 12)

All evaluation uses **synthetic profiles, explicitly labelled as synthetic** — never presented as real student data. No accuracy percentages are claimed beyond what tests show.

1. **Determinism/consistency (unit):** same inputs twice → identical ranking; database round-trip does not change output.
2. **Coverage:** for every published career there exists at least one synthetic profile where it reaches the top 8 (guard against unreachable careers).
3. **Sensitivity:** targeted profiles (e.g. high `security` + security skills → Cybersecurity Analyst top-3) with asserted expected behaviour; each of the 9 categories has at least one such profile.
4. **Explanation quality:** checklist review — every recommendation's explanation names its top factors, matched skills, and development areas without hallucination; reviewed by the developer and (where possible) a qualified reviewer.
5. **Weights sensitivity:** re-running the suite under ±0.05 weight perturbations documents how stable rankings are (a limitation section, not an accuracy claim).

Results, including failures, are recorded honestly in docs/evaluation-results.md (Phase 12–13).

## 8. Limitations and ethics

- Career–category and skill weights are **expert-designed constants**, not learned from data.
- Recommendations reflect self-reported interest and self-reported skill — both can be incomplete or biased.
- No labour-market data (demand, salary, geography) is considered.
- A low score is not a verdict of unsuitability; the UI frames results as "paths worth exploring" and the report must state this.
- The engine advises; the student decides.
