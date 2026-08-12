# Completion and archival

Loaded during: finishing a goal, deciding what to archive.

## Final Review — before declaring the Goal complete

Writing code is not completion. Run through all of these before considering the goal done:

1. Every required milestone in `PLAN.md`'s Milestone Index is marked complete.
2. Every item in `PLAN.md`'s Acceptance Criteria is individually confirmed, not assumed.
3. Comprehensive final verification actually runs (the full relevant suite, not just the last milestone's narrow check) — see `references/verification.md`.
4. The full diff for this goal is reviewed end to end, not just the most recent change.
5. Check for regressions — did anything that worked before stop working?
6. Any migration or destructive change introduced by this work is specifically re-examined.
7. No unaddressed warnings or errors from build/typecheck/lint remain.
8. Any new TODO/FIXME introduced by this work that represents genuinely blocking follow-up is either resolved or explicitly called out — don't let it silently ride along as unfinished work disguised as done.
9. No known blocking issue remains open.

If any of these fail, that's a FAIL in the inner loop (`references/execution-loop.md`) — go fix it, don't declare completion with caveats.

## Archive

Once the Final Review passes:

1. Move `.plans/active/<plan-id>/` to `.plans/completed/<plan-id>/`.
2. Update `.plans/INDEX.md` — move the row from Active to Completed with the completion date.
3. Update `PLAN.md`'s Metadata `Status` to `complete` before or during the move.

A completed plan is **not** loaded by default in future work (see `SKILL.md`'s Context loading section) — only pull it back in when a new goal has a direct dependency on it or genuinely needs its architecture history.
