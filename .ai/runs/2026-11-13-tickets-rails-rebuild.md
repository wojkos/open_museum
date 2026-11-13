# Run: to-tickets rails-rebuild

- Goal: turn the Rails rebuild spec into GitHub issues with blocking edges.
- Spec: `.ai/specs/2026-11-13-rails-rebuild.md`
- Plan: draft 12 vertical slices, quiz the human, publish epic + tickets in dependency order.
- Decisions: breakdown approved as is; epic parent yes; no perf ticket (see handoff).
- Verification: `gh api .../dependencies/blocked_by` for #5–#16 shows the intended edges; epic #4 sub_issues total 12.
- Outcome: epic #4, tickets #5–#16 created, all `ready-for-agent`. Issue #1 not touched.
- Open questions: response-time budget (no ticket).
- Note: gh 2.45 lacks `--blocked-by`/`--parent`; used REST dependency and sub_issues endpoints.
