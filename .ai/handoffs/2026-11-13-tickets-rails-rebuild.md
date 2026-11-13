# Handoff: tickets, rails-rebuild

## Goal
Break `.ai/specs/2026-11-13-rails-rebuild.md` into tracer-bullet GitHub issues with native blocking edges, labelled `ready-for-agent`. Issue #1 untouched.

## Decisions (with why)
- 12 tickets, granularity approved as proposed by the human. Why: each is one context window and ends in a tested, demoable flow.
- Epic issue #4 with all tickets as sub-issues (human chose a parent). Why: one place to track the rebuild.
- No response-time-budget ticket (human decision); it stays an open item in the spec.
- Operator track (#11 onward) is blocked only by catalog data (#6), so it runs parallel to the Visitor track. Administrate spike is GO, so there is no spike gate.
- All tickets labelled `ready-for-agent` (even blocked ones; blockers are native dependencies).

## Artifacts
Epic #4. Tickets (blocked by):
- #5 Skeleton, RSpec, CI, design tokens (none)
- #6 Catalog data, Instance settings, seed (#5)
- #7 Matcher and Prompt builder (#5)
- #8 Consent, Intake, Visit resume (#6)
- #9 Match list, no-match, Exhibit detail (#7, #8)
- #10 Ask more and Copy prompt (#9)
- #11 Operator sign-in, Administrate, Gallery/Interest CRUD (#6)
- #12 Exhibit CRUD with photo and AI note (#11)
- #13 Instance settings editing (#11)
- #14 Visit events and rate limits (#10)
- #15 Visit export CSV (#14, #11)
- #16 Retention job (#14)
Also `.ai/runs/2026-11-13-tickets-rails-rebuild.md`, `.ai/lessons.md`.

## Open questions
- Response-time budget: deliberately no ticket; revisit after #10.
- Deployment automation and backups: issue #1.

## Next session
`/implement` on ticket #5 (only unblocked ticket). After it, #6 and #7 can run in parallel.

## Status
settled
