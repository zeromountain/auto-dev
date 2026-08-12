# Execution loop

Loaded during: running the implement/verify/fix cycle, hitting a repeated failure, considering whether something is a real blocker, updating the plan mid-execution.

Keep Goal and Loop distinct: the **Goal** (native or self-defined, see `references/hosts.md`) is *when* work is done. This **inner loop** is *how* you get there.

## The loop

```
INSPECT   — read the current milestone, relevant code, establish a baseline
IMPLEMENT — make the change
VERIFY    — run the real check (references/verification.md)
EVALUATE  — pass or fail?
```

**PASS →** check the milestone's Done Criteria → if met, mark the milestone complete in `PLAN.md`'s Milestone Index, move to the next milestone (INSPECT again). If Done Criteria aren't actually met yet despite the check passing, that's a sign the check was too narrow — go back to VERIFY with a better check before declaring done.

**FAIL →**

```
ANALYZE ERROR
  → FORM / UPDATE HYPOTHESIS
  → FIX ROOT CAUSE
  → VERIFY AGAIN
```

Fix the root cause, not the symptom the failure message names first — before editing, check what else calls the code you're about to touch, so the fix doesn't just patch the one path the failure happened to surface.

## Anti-loop: change tactic on repeated failure, not on a retry counter

**Do not** use a fixed retry count ("failed 3 times, giving up") as the trigger for anything. Failure count is the wrong signal — it says nothing about whether you're converging.

The real trigger is a **repeated failure signature** — the same error, the same symptom, the same test failing the same way. When that happens:

1. Stop the current tactic. Repeating it again with minor tweaks is not progress.
2. Re-read the actual error/output carefully — don't work from a summary or memory of it.
3. Investigate the related code/config directly.
4. Only if it's actually relevant, check `LOG.md` for whether this was tried before (see `SKILL.md`'s Context loading — don't read the whole file speculatively).
5. Change the hypothesis about what's wrong.
6. Apply a **materially different** intervention — not a variation on the same idea.
7. Verify again.

Conversely, a genuinely new hypothesis with a genuinely different fix can be tried as many times as evidence justifies — this isn't about capping effort, it's about not repeating the same non-working thing.

## Blockers are rare — exhaust alternatives first

Something only qualifies as a real blocker when it is one of:

- Required credentials aren't available
- Required infrastructure access isn't available
- A destructive operation needs explicit user approval
- Business semantics can't be inferred from the repository or the interview and materially affect the outcome
- A significant, unresolved user decision blocks this specific milestone
- An external dependency can't be mocked, simulated, or otherwise worked around

**Before declaring one**, in order:

1. Check repository docs (AGENTS.md/CLAUDE.md, README, comments) — the answer may already be there.
2. Check config/environment — a credential or endpoint may already be configured somewhere non-obvious.
3. Check for existing mocks/fixtures that make the dependency unnecessary for verification purposes.
4. Check for a local/staging alternative to whatever's unavailable.
5. Check whether other milestones in this plan can proceed independently of this blocker — if so, **keep working those** rather than stopping entirely.

Record a real blocker in `PLAN.md`'s Blockers section, and ask the user only the minimum question needed to unblock it — not a general "what should I do?"

## Plan Evolution: what you can change yourself vs. what needs the user

**Autonomous, no confirmation needed** (record it, don't ask):
- Implementation detail decisions within already-agreed scope
- Adding verification beyond what was originally planned
- Splitting an oversized milestone into two (update the Milestone Index)
- Revising a safe/Assumption-category technical decision when evidence contradicts it (update the Assumptions section, note why)
- Recording a newly discovered constraint

**Requires asking the user first:**
- Anything that changes an explicit User Decision recorded in `PLAN.md`
- A change to product scope
- A change to user-visible behavior
- A change to what an Acceptance Criterion actually means
- Introducing destructive behavior not already scoped
- A change to an architecture choice the user explicitly made

## LOG.md discipline (Medium/Large plans)

Record: significant implementation changes, validation failures with their root cause, debugging discoveries, strategy changes, architecture deviations, and milestone-completion evidence.

Do not record: every shell command run, routine successful checks, or narrative that duplicates what `PLAN.md`'s Current Context already states. `PLAN.md` is current-state; `LOG.md` is historical evidence — don't let them converge into the same content.

## Context minimization during execution

Default context stays to: project instructions, active `PLAN.md`, the current milestone file (Large plans), and repository code directly relevant to the current milestone. Do not open unrelated active plans, completed plans, other milestones' spec files, the full `LOG.md`, or another goal's acceptance criteria without a concrete reason. See `SKILL.md`'s Context loading section — the purpose is preventing stale/unrelated requirements from bleeding into the current milestone, not just saving tokens.

## Git safety

- No destructive git operations (force-push, hard reset, history rewrite) without explicit user request.
- Never revert another person's changes you didn't make as part of this work.
- Touch only files relevant to the current milestone even if the working tree has unrelated dirty files — leave those alone unless the user asked about them.
