# PLAN.md format

Loaded during: writing or updating a plan's `PLAN.md`.

`PLAN.md` holds **durable state and the goal contract** only. It is not a history log — see `references/planning.md` for the PLAN.md/LOG.md split, and don't let debugging narrative creep in here.

## Required sections

```markdown
# <plan-id>

## Metadata
- Created: <date>
- Size: Small | Medium | Large
- Status: active | blocked | complete

## Objective
One or two sentences: what this goal achieves and why.

## Current Context
What's true about the repository/system right now that's relevant to this
goal. Update as execution reveals more — this is *current*, not historical.

## User Decisions
Decisions the user explicitly made during interviewing (category C from
references/discovery.md). Quote or closely paraphrase them. These cannot be
silently changed during execution — see "Plan Evolution" in
references/execution-loop.md.

## Assumptions
Safe implementation decisions (category B) made autonomously, with brief
rationale. Revisable if evidence contradicts them, but visible so the user
can correct any that were wrong.

## Scope
What this goal includes.

## Out of Scope
What it explicitly does not include — especially anything a reasonable
reader might otherwise assume was included.

## Architecture Decisions
Any non-trivial technical choices and why, especially where they deviate
from existing repo convention (and why that deviation was justified).

## Milestone Index
- [ ] M01 — <short name>
- [ ] M02 — <short name>
...
(Small/Medium plans: milestones described inline here.
Large plans: one line per milestone, detail lives in milestones/M0N-*.md —
see references/milestone-template.md.)

## Current Milestone
Which milestone is active right now. This is the pointer execution resumes
from.

## Acceptance Criteria
Concrete, checkable conditions for the *goal* as a whole (not per-milestone
— those live in each milestone's Done Criteria). Should be specific enough
that "is this met?" doesn't require judgment calls.

## Verification Strategy
Which existing repo commands/suites this goal's changes will be checked
with (unit, integration, typecheck, lint, build, E2E, etc.) — see
references/verification.md for how to choose these.

## Blockers
Currently active blockers only (see references/execution-loop.md for what
qualifies). Empty when nothing is blocked. Resolved blockers move to
LOG.md, not deleted silently.

## Post-Deployment Follow-up
Any genuinely time-based, real-world observation this goal requires after
shipping (e.g. real production monitoring) that could NOT be converted to
executable validation. Does not block Goal completion. Empty if not
applicable — most goals won't need this section populated.

## Completion Criteria
The explicit, evidence-based conditions under which this goal is DONE. See
references/completion.md for the Final Review this must satisfy.
```

## Notes

- Keep this scannable. If a section is empty, say so briefly rather than omitting it — an empty `Blockers` section is meaningful signal, a missing one is ambiguous.
- For Large plans, this file is the execution controller: milestone *detail* lives in `milestones/`, but the Milestone Index, Current Milestone, and top-level Acceptance/Completion Criteria stay here so resuming work never requires reading every milestone file.
