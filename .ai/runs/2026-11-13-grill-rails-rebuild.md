# Run: grill Open Museum Rails rebuild
- Goal: grill-with-docs on rebuilding the visitor app on Rails; output GLOSSARY.md + ADRs. No code, no /to-spec.
- Input: docs/source/cnk_kompas/*, AGENTS.md, .ai/lessons.md, docs/agents/*.
- Plan: ask frontier round (Q1-Q8), record answers.
- Decisions: user told the run to proceed autonomously, so all recommended answers to Q1-Q8 were adopted (generic core; full Rails replacement; glossary terms; matching = score>0, score desc, Gallery order, slug, as a pure Ruby object; en default + PL; anonymous minimal Visit data; single Operator via Rails auth; Ask more via configurable link + copy fallback).
- Outcome: GLOSSARY.md and ADRs 0001-0006 written.
- Open questions: consent/retention/data sharing per Instance; Gallery-grouped vs flat display in the spec; open-source licence; photo storage (assumed Active Storage later).
