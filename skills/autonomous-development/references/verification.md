# Verification

Loaded during: deciding what to run to verify a change, deciding whether a milestone or the goal itself is actually done.

## Use what the repository already has

Prefer existing repo commands over inventing new verification: focused unit tests, integration tests, typecheck, lint, build, E2E (Playwright, etc.), runtime smoke tests, database reconciliation scripts, migration validation. These are already trusted by the project — use them instead of building parallel verification.

## The verification ladder: match scope to change

Run the narrowest check that actually covers the change, then widen at milestone/goal boundaries:

| Change | Verify with |
|---|---|
| A function/feature fix | The related unit test(s) |
| A package-level change | That package's typecheck |
| An API change | The relevant integration test |
| Milestone complete | That milestone's full Verification section (see `references/milestone-template.md`) |
| Goal complete | Comprehensive final verification (see `references/completion.md`) |

Do not run the entire build/test suite on every small edit — that's slow and doesn't isolate the signal. Do run the full relevant suite at milestone completion and again at final verification.

## Never bypass verification to manufacture a pass

None of the following are acceptable under any circumstance, regardless of time pressure or a stubborn failure:

- Disabling a test
- Deleting a failing test
- Weakening an assertion to make it pass without fixing the underlying issue
- Suppressing a TypeScript/type error instead of fixing it
- Disabling a lint rule to silence a real finding
- Excluding the feature under test from what gets verified
- Recording a test as passed without having run it
- Treating an external system's result as successful without confirming it actually was

If a test itself turns out to be genuinely wrong (not just inconveniently failing), you may fix it — but only after confirming the test's premise is actually incorrect, and record the reasoning in `LOG.md`. "The test is annoying" is never sufficient justification; "the test asserts behavior that the interview explicitly changed" is.

## No Passive Waiting

Time elapsing is never a valid milestone or completion condition. This applies to both plan-writing and goal-writing.

**Forbidden patterns** — do not write these into a milestone's Done Criteria, a plan's Acceptance Criteria, or a Goal condition:

- "Monitor for 7 days"
- "Wait 24 hours and check"
- "Check status next week"
- "Observe production traffic for a few days"

**Convert to executable validation instead:**

| Instead of | Use |
|---|---|
| "Observe the pipeline for a week" | Replay historical data through it and check results |
| "Wait and see if it holds up under load" | A load test with representative traffic |
| "Monitor for failures over time" | Inject synthetic failure/retry/restart scenarios and verify recovery |
| "See if it handles edge cases in practice" | Representative fixtures covering the edge cases directly |
| "Check if the data stays consistent" | A reconciliation check run against a known dataset |
| "See if alerts fire correctly" | Validate the monitoring rule against a synthetic trigger |

**Example — bad:** "Observe the CDC pipeline in production for 7 days before proceeding to the next milestone."
**Example — good:** "Replay historical fixtures and verify insert/update/delete, duplicate delivery, retry, restart, and schema-drift scenarios all produce correct normalized events."

If genuine long-horizon production observation is still warranted after shipping (it sometimes is — some failure modes really do only show up over days of real traffic), record it explicitly in the plan's **Post-Deployment Follow-up** section (`references/plan-template.md`). It does not block Goal completion unless the user explicitly said it should.
