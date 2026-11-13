# AGENTS.md

Instructions for AI coding agents working in this repository (Open Museum). `CLAUDE.md` imports this file; edit rules here only.

## Project metadata: `.ai/`

All AI-related artifacts live in `.ai/`. Use them; do not invent other locations. Exception: the engineering-skills configuration (issue tracker, domain docs) lives in `docs/agents/` and is referenced from the `## Agent skills` section below.

```
.ai/
├── specs/              # SDD specifications: YYYY-MM-DD-slug.md
│   ├── implemented/    # specs fully implemented (moved here when done)
│   └── archive/        # abandoned or superseded specs
├── runs/               # logs of autonomous AI runs: YYYY-MM-DD-slug.md
├── lessons.md          # index of lessons learned (one line each)
└── lessons/            # lesson details: YYYY-MM-DD-slug.md
```

Naming: `YYYY-MM-DD-slug.md`, lowercase kebab-case slug, date = creation date (today's date from the environment, never guessed).

### Rules

1. **Specs first.** Non-trivial features start from a spec in `.ai/specs/`. If none exists, write one (or ask) before implementing. Follow the spec; if it is wrong or incomplete, update the spec rather than silently diverging. When fully implemented, move it to `specs/implemented/`; move dead specs to `specs/archive/`.
2. **Log every autonomous run.** Each autonomous run creates `.ai/runs/YYYY-MM-DD-slug.md` recording goal, spec used, plan, key decisions, verification results, outcome and open questions. Update it as you work, not only at the end.
3. **Read lessons before work.** Read `.ai/lessons.md` at the start of a task and apply what is relevant.
4. **Record lessons.** After fixing a bug, after any user correction, or on any finding worth remembering long term: add a one-line entry to `.ai/lessons.md` (newest first), with a detail file in `.ai/lessons/` if it needs more. Write it as a rule that prevents the mistake from recurring. Promote repo-wide durable rules into this file.

## Working principles

- **Plan complex tasks.** For anything multi-step or ambiguous, plan before coding: state the approach, affected files and how you will verify. Keep the plan in the spec or run log. If the work goes sideways, stop and re-plan rather than pushing on.
- **Verify every change.** Run the project's tests, linters and build (or the real app) before declaring done, and report actual output. Never claim success unverified; if something cannot be verified, say so.
- **Fix bugs autonomously.** Given a bug or failing CI, reproduce, find the root cause, fix and verify without waiting for step-by-step direction. Add a regression test where practical.
- **Be specific, resolve ambiguity.** Ask only when a decision is truly the user's; otherwise pick a sensible default and note it in the run log.
- **Prefer elegant fixes.** If a fix turns out to be a workaround, redo it properly with what you now know instead of stacking patches.
- **Keep context clean.** Delegate research and independent subtasks to subagents. Use separate git worktrees for parallel work on disjoint areas.
- **Repeat work becomes a skill.** If a procedure is done repeatedly, propose a committed skill or command for it.

## Agent skills

### Issue tracker

GitHub Issues for `wojkos/open_museum`, via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` and `docs/adr/` at the repo root (created lazily). See `docs/agents/domain.md`.
