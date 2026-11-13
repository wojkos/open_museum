---
project: "CNK Kompas"
version: 1
status: draft
created: 2026-08-10
context_type: brownfield
kind: test-plan
prd_version: 1
main_focus: recommendation-engine
scope: unit + integration (no property-based, no E2E)
top_risks:
  - weak-personalization-flat-ranking
  - sort-ordering-regressions
  - empty-thin-results-for-real-tag-combos
---

# Test Plan: CNK Kompas — Phased Rollout

> Derived from `context/foundation/prd.md` (v1), the archived slice plans under
> `context/archive/`, and a direct read of the implemented code + existing
> test suite on 2026-08-10. Edit-in-place; each rollout phase opens its own
> `context/changes/<change-id>/` folder as it ships.

## §1 — Load-bearing principles

1. **Cost × signal.** Every test added must answer: *what is the cheapest test
   that gives a real signal for this risk?* The recommendation engine
   (`exhibits/matching.py`) is pure and HTTP-free — its risks are covered by
   fast unit tests, not view or browser tests. Do NOT promote a scorer risk to
   an integration test when a `match_exhibits(...)` call already exercises it.
2. **User concerns are evidence.** The owner explicitly flagged three
   recommendation risks (see §2). They carry the same weight as PRD lines.
3. **Signal, not knowledge.** This plan cites evidence (PRD FRs, code we read,
   existing test names) as *likelihood*. It does not assert where a failure
   lives at line level — that anchor is `/10x-research`'s job per rollout phase.

**Scope decision (owner, 2026-08-10):** unit + integration only. No
property-based/fuzz layer and no browser E2E this rollout — matches the current
suite style (`django.test.TestCase`, `Client`).

## §2 — Risk map (recommendation-focused)

Current suite baseline: **108 tests** across 22 classes. The recommendation
engine is already the best-covered *pure* module (7 `MatchingServiceTests` in
`exhibits/tests.py`). The gaps below are the **edges** of recommendation, not
the core rule.

| # | Risk | Likelihood evidence | Impact | Current coverage | Gap |
|---|---|---|---|---|---|
| R1 | **Weak personalization / flat ranking** — everything scores the same, results become a "generic dump" (violates FR-003 acceptance: "not a generic full catalog dump") | `matching.py` scoring is `overlap (+boosts)`; small integer range means many ties are plausible | High — breaks the core product promise | `test_tag_overlap_is_primary_score` proves overlap drives score for ONE combo | No test asserting a *spread* of scores across a realistic tag set; no guard that top result out-ranks a marginal one for common inputs |
| R2 | **Sort/ordering regressions** — results not correctly `-score, part.sort_order, slug` | `match_exhibits` sort key is explicit and load-bearing (FR-003 "sorted by exhibition part") | High — visitor sees wrong priority | `test_tied_scores_ordered_by_part_sort_order` covers tie→part order | No test for the full 3-level key (score → part → slug fallback); no test that higher score always precedes lower regardless of part |
| R3 | **Empty / thin results for real tag combos** — visitor picks common tags and gets an empty or near-empty list | `match_exhibits` drops score-0 exhibits and returns `[]` for empty tags; Bzzz gating can silently remove a whole gallery | High — visitor "gets nothing", worst-case UX | `test_empty_tags_yield_empty_matches` (empty input only) | No test that *non-empty, realistic* tag selections yield a non-empty list; no lower-bound guard per single-tag selection |
| R4 | **Bzzz gallery gating correctness** (secondary) | `score_exhibit` returns 0 for `bzzz` part unless `kids_under_6` | Medium — safety/appropriateness rule | `test_bzzz_gallery_excluded_without_kids_under_6`, `test_kids_under_6_biases_bzzz` | Well covered; monitor only |
| R5 | **Edge intake normalization** — `normalize_kids_under_6` and empty/None companion feeding the scorer | `visits.py::normalize_kids_under_6`; `intake.py` defaults companion→"alone", budget→"medium" | Medium — malformed input could bias or crash | Tested only *through* the flow (`test_family_missing_kids_normalizes_to_false_in_results`) | No direct unit test of `normalize_kids_under_6`; no scorer test with `companion=""` |
| R6 | **Catalog-empty result path** | `intake.py::_match_context` sets `catalog_empty` flag | Low | none | No test for empty-catalog result state |

## §3 — Rollout phases (status ledger)

Phases are ordered by the owner's stated priority (R1/R2/R3 first). Re-running
`/10x-test-plan` resumes at the first phase not `complete`.

| Phase | Change ID | Covers | Layer | Status |
|---|---|---|---|---|
| T-01 | matching-ranking-spread-tests | R1, R2 | unit | implemented (author-verified; needs local `manage.py test`) |
| T-02 | matching-nonempty-guarantee-tests | R3, R4 | unit | implemented (author-verified; needs local `manage.py test`) |
| T-03 | intake-normalization-and-empty-catalog-tests | R5, R6 | unit + integration | implemented (author-verified; needs local `manage.py test`) |

### T-01: Ranking spread & ordering (R1, R2)

- **Outcome:** the scorer demonstrably *personalizes* (a spread of scores, not a
  flat dump) and the full 3-level sort key is locked.
- **Change ID:** matching-ranking-spread-tests
- **Target:** `exhibits/matching.py` → new tests in `exhibits/tests.py`
  (`MatchingServiceTests` or a new `MatchingRankingTests`).
- **Proposed assertions:**
  - For a realistic multi-tag selection, the result contains **>1 distinct
    score value** (proves ranking is not flat / not a generic dump — R1).
  - The #1 result's score is strictly greater than the last result's score for
    that same selection (R1).
  - Higher score **always** precedes lower score regardless of part
    (`-score` dominates `part.sort_order`) — R2.
  - Full tie (same score, same part) falls back to `slug` ascending — R2.
- **Layer rationale:** pure function; unit tests only.
- **Status:** pending

### T-02: Non-empty guarantee for real tag combos (R3, R4)

- **Outcome:** every *single realistic tag* (from the seed catalog) yields at
  least one recommendation for a default (`alone`, `medium`) visitor, so the
  product never silently returns nothing for a reasonable pick.
- **Change ID:** matching-nonempty-guarantee-tests
- **Target:** `exhibits/matching.py` → `exhibits/tests.py`.
- **Proposed assertions:**
  - Parametrized over every tag slug in the seed catalog: `match_exhibits`
    with that single tag returns a non-empty list for `companion="alone"`
    (R3). *(Bzzz-only tags, if any, are the documented exception — assert they
    return non-empty only with `kids_under_6=True`.)*
  - A "common everyday" multi-tag combo (e.g. `["fizyka", "energia"]`) returns
    ≥ N matches spanning ≥ 2 exhibition parts (R3).
  - Regression guard: a tag that exists ONLY on Bzzz exhibits returns `[]`
    without kids, non-empty with kids (R4 — ties R3 to the gating rule).
- **Layer rationale:** pure function against the seed catalog; unit tests.
- **Status:** pending

### T-03: Intake normalization & empty-catalog path (R5, R6)

- **Outcome:** the normalization helper and the empty-catalog result state are
  covered directly, not only implicitly through the happy-path flow.
- **Change ID:** intake-normalization-and-empty-catalog-tests
- **Target:** `exhibits/visits.py::normalize_kids_under_6`,
  `exhibits/intake.py::_match_context` → `exhibits/tests.py`.
- **Proposed assertions:**
  - `normalize_kids_under_6("family", None) == False`;
    `normalize_kids_under_6("alone", None) is None`;
    non-family values pass through unchanged (R5) — direct unit test.
  - `match_exhibits(companion="", tag_slugs=[...], time_budget="medium")` does
    not raise and does not apply the group boost (R5).
  - Integration: results view with an **empty catalog** renders the
    `catalog_empty` state (no 500) — R6.
- **Layer rationale:** helper = unit; empty-catalog = one thin integration test.
- **Status:** pending

## §4 — Out of scope (explicit non-goals)

- **Property-based / fuzz testing** of `score_exhibit` — owner deferred
  (2026-08-10). Revisit if the scoring rule grows beyond simple overlap+boosts.
- **Browser E2E** of the intake→results→detail→ask-more journey — owner
  deferred. The HTMX flow is already covered by `Client`-level view tests.
- **Ask-more prompt, bilingual, visit-recording, operator-gate** areas — already
  well covered (see §2 baseline); not part of this recommendation-focused rollout.
- No new test runner/config: continue with `uv run python manage.py test`
  (per `AGENTS.md`; no pytest/ruff configured yet).

## §5 — How to run

```bash
uv run python manage.py test                     # full suite
uv run python manage.py test exhibits.tests      # recommendation area
```

## §6 — Cookbook (filled in per phase as it ships)

_Empty until T-01 opens its change folder. Each rollout phase records here the
concrete patterns it established (fixtures, seed-catalog helpers, parametrize
style) so `/10x-tdd` and future phases reuse them._
