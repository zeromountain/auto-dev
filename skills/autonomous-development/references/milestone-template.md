# Milestone format

Loaded during: writing or updating a milestone file (Large plans only — Small/Medium plans describe milestones inline in `PLAN.md`'s Milestone Index).

Path: `.plans/active/<plan-id>/milestones/M0N-<short-name>.md`

## Milestones must be independently verifiable

A milestone should produce **observable progress**, not just cover a technical layer. Prefer decomposing by what can be demonstrated to work over decomposing by architecture tier.

**Bad milestone:** "CDC work"
**Good milestone:** "Insert/update/delete events from SQL Server are captured and transformed into normalized events, verified against an integration fixture"

The bad version can't be checked as done or not-done without more specification. The good version has a built-in verification target.

## Required sections

```markdown
# M0N — <short name>

## Objective
What this milestone achieves, in one or two sentences, framed as an
observable outcome.

## Dependencies
Which other milestones (if any) must be complete first. None if this can
start immediately.

## Requirements
The specific, concrete requirements this milestone must satisfy.

## Expected Affected Areas
Files, modules, services, or systems this milestone is expected to touch.
Not exhaustive — a guide for what "related code" means when loading
context (see SKILL.md's Context loading section), and a sanity check
against scope creep.

## Constraints
Anything that must hold throughout this milestone's work — e.g. "must not
change the public API of X," "must not touch migration files."

## Verification
The specific check(s) that prove this milestone works — real commands,
real fixtures, real scenarios. Not "will be tested" — name the actual
verification (see references/verification.md).

## Done Criteria
The explicit condition(s) under which this milestone is complete. Should
be checkable without ambiguity — this is what execution-loop.md's
"DONE CRITERIA check" evaluates against.
```

## Notes

- Keep each milestone file focused on itself. Don't read *other* milestone files while working the current one unless there's a concrete dependency reason (see SKILL.md's Context loading section).
- If, mid-execution, a milestone turns out to be oversized (its Requirements keep growing), split it into two — this is autonomous Plan Evolution (see `references/execution-loop.md`), update the Milestone Index in `PLAN.md` accordingly.
