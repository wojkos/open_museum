# Handoff: grill + spec, rails-rebuild

## Goal
Close remaining gaps from grilling rounds 1–7 and write the spec for the Open Museum Rails rebuild, including `DESIGN.md` and default PL/EN copy.

## Decisions
- Default consent notice approved as drafted (PL/EN, includes the 12-month figure; Instance edits it). Why: neutral default, legal wording stays Instance policy.
- Three test seams: Visitor-flow system spec, domain Matcher spec, Operator and export request specs. Why: fewest seams at the highest level.
- Visit export time rounded to the hour. Why: keeps time-of-day patterns, no id or IP so re-identification risk is low.
- Focus ring uses the Text colour (the prototype's Border colour was too faint for AA).
- The human first chose to wait for the spike, then told the session to proceed autonomously without confirmation. The spec was written with slice 3 (Operator panel) gated on the spike.

## Artifacts
- `.ai/specs/2026-11-13-rails-rebuild.md` (spec, includes default PL/EN copy and slice order)
- `DESIGN.md` (Rails design system)
- `.ai/runs/2026-11-13-grill-rails-rebuild.md` (Round 8 added)
- `.ai/lessons.md`

## Open questions
- Administrate + Mobility + Active Storage spike (sibling 84afb07c) had no handoff when written; if no-go, update ADR 0004/0011 and the spec's slice 3.
- Response-time budget (after slice 1); deployment automation and backups (issue #1).
- The human did not give an explicit "settled" confirmation; they directed the session to finish autonomously.

## Next session
`/to-tickets` on `.ai/specs/2026-11-13-rails-rebuild.md`. Make the Operator-panel ticket blocked by the spike result.

## Status
settled (with the spike gate above)
