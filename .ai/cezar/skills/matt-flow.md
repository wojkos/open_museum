---
name: matt-flow
description: Orchestrator for the gap-filling half of the ask-matt flow. Inspect repo state, then keep up to 4 human-interactive cezar sessions running in waves (grill, spec, tickets, triage, prototype, wayfinder), advance each topic to its next phase, merge settled branches. Implementation is NOT done here: it runs as separate matt-implement tasks.
---

# matt-flow orchestrator (gap filling)

You run inside the `matt-flow` workflow. Before you, the `launch_impl` node already filled the implementation slots (`.ai/cezar/scripts/matt-implement-launch.py` -> one `matt-implement` task per issue, off `main`). After you, the workflow commits your branch and opens a draft PR. So:

- You do NOT grill, write specs, implement, push or open PRs yourself.
- Your job: find the gaps that stop work from becoming `ready-for-agent` tickets, open sessions that close them, and keep going until no gap can be advanced without the human.

Routing comes from `.claude/skills/ask-matt/SKILL.md` and `PHASE-BOUNDARIES.md` (read first). Also read `.ai/lessons.md`, `GLOSSARY.md`, `docs/agents/*`. The user's task text (idea, topic or empty) is input; empty = work from the backlog.

## 1. Survey (read-only)

- `.ai/specs/*.md` (active); `implemented/`, `archive/` are done.
- `.ai/handoffs/*.md`: newest handoff per topic wins; read `Status` and `Next session`.
- `gh issue list --state open --json number,title,labels,createdAt`: group by `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `in-progress`.
- Open PRs (`gh pr list`) and `.ai/runs/` for in-flight work.
- Implementation state: run `python3 .ai/cezar/scripts/matt-implement-launch.py --dry-run` (read-only) to see active, stuck and waiting issues. Report it; never implement.

## 2. Find gaps (one session per topic)

First match wins:

| State found | Session | Skill |
|---|---|---|
| New idea in user text, or fuzzy topic, no spec | **grill** | `/grill-with-docs`, then `/to-spec` in the same session once settled |
| Spec with open questions / handoff `needs-more-grilling` | **grill** (resume) | `/grill-with-docs` seeded with spec + handoff |
| Spec settled, no tickets reference it | **tickets** | `/to-tickets` (native GitHub `blocked_by` edges, label `ready-for-agent`) |
| Open question needing a runnable answer | **prototype** | `/prototype` |
| Issues `needs-triage` / `needs-info` (not from `/to-tickets`) | **triage** | `/triage` |
| Issue labelled `in-progress` reported STUCK by the launcher | **triage** | `/triage` on that issue: clarify, split or re-label; remove `in-progress` only when it is ready again |
| Ticket graph has no frontier but open tickets (all blocked by something not ticketed) | **tickets** | `/to-tickets` for the missing blocker |
| Huge foggy effort | **wayfinder** | `/wayfinder` |

Never two sessions on the same topic. Priority when capacity is short: tickets > spec > grill > triage > prototype.

## 3. Dispatch in waves

cezar allows 4 children **in flight**, not 4 in total. Keep the slots full:

1. Commit your branch clean first (children fork your committed tip).
2. Dispatch up to 4 gap sessions (always `node "$CEZ_BIN" task create ...`, no `--budget`):

```
node "$CEZ_BIN" task create "<objective>" --title "<phase>: <topic>" \
  --scope ".ai/specs/<slug>*, .ai/handoffs/*-<slug>.md, GLOSSARY.md, docs/adr/" \
  --success "<done>" --evidence "<handoff path>" --model <model>
```

   Models: `opus` for grill / spec / prototype / wayfinder (judgement), `sonnet` for tickets / triage.
3. End the turn with `CEZ:MONITORING`.
4. On each report: validate (handoff on the branch with all sections; spec/issues it names exist), `git merge --no-ff <branch>`, then **re-survey and refill**:
   - handoff `settled` after grill/spec -> dispatch **tickets** for that spec now (same run, no new `/matt-flow` needed);
   - tickets created -> nothing more here: the new `ready-for-agent` issues are picked up by the implementation slots (the next `matt-implement` refill or `matt-flow` run);
   - `needs-more-grilling` -> leave it for the human, list it;
   - free slot + remaining gap -> dispatch it.
5. Stop dispatching when no gap is left that can move without a human answer.

Every objective must contain:

1. Which skill on what (spec path, issue numbers, idea text); read `.claude/skills/ask-matt/SKILL.md`.
2. "This session is INTERACTIVE: ask the human (CEZ:ASK for concrete choices); do not auto-answer. Do not end until the human confirms the phase is settled."
3. Keep the phase in one unbroken context; do not compact mid-phase.
4. **Handoff (mandatory):** `.ai/handoffs/YYYY-MM-DD-<phase>-<slug>.md` (date from the environment) with `Goal`, `Decisions` (with why), `Artifacts`, `Open questions`, `Next session` (exact skill + input), `Status` (`settled` | `needs-more-grilling`). Log the run in `.ai/runs/`, add lessons, report via `cez task report`.
5. Specs at `.ai/specs/YYYY-MM-DD-slug.md`. Do not push or open PRs: the parent's workflow opens one PR for the run.

If a handoff is missing, message the child via `$CEZ_TREE_DIR/inbox/<id8>/`.

## 4. Close

Never merge into `main`, never push. Write `.ai/runs/YYYY-MM-DD-matt-flow.md` (append `-2`, `-3` if it exists) and commit it. Final message (it becomes the PR summary): table of sessions (phase, topic, status, handoff), implementation slots (active / launched / stuck issues from the launcher), topics waiting on the human, and the next step. Finish with `CEZ:DONE` only when all children settled and are merged; the workflow then commits and opens the draft PR.
