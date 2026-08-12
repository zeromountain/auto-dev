# Discovery and interviewing

Loaded during: repository discovery, requirement classification, and deciding what (if anything) to ask the user.

## 1. Investigate before you ask anything

Never open a development request with a batch of questions. Investigate first, in roughly this order, stopping early once you have enough to classify what's actually unresolved:

1. `AGENTS.md`, `CLAUDE.md` (or whatever this host's project-instructions file is)
2. `README` and any `docs/`
3. `package.json` / workspace config / lockfiles (or the language's equivalent) — dependencies already chosen, scripts already defined
4. Project directory structure and existing architecture
5. A similar feature already implemented elsewhere in the codebase — this is usually the single best source of convention
6. DB schema, migrations
7. API conventions (REST/GraphQL/RPC shape, error format, auth pattern)
8. Frontend state management, if relevant
9. Existing tests — what's tested, how, with what runner
10. CI/CD config, lint config, typecheck config, build commands

Anything answerable from what you find here is answered — silently, by using it — not asked.

**Anti-pattern:** the codebase consistently uses Zustand for state, and you ask "Should I use Zustand for state management?" If the repo already tells you, don't ask; use it, and don't call it out as if it were a decision made on the user's behalf that could need reverting — it's just convention-following.

## 2. Classify every open question

After investigating, whatever remains genuinely unresolved falls into exactly one of three buckets. Work through them in order — most requests have nothing left in bucket C.

### A. Repository-resolvable

Answerable from code or docs you have access to. **Investigate further; do not ask.** If your first pass didn't find it, look harder (grep for similar patterns, check a sibling module) before concluding it's not resolvable this way.

### B. Safe implementation decision

All of the following hold:
- Consistent with existing convention (or there's no established convention and the choice is genuinely low-stakes)
- Reversible
- Doesn't materially change product/user-facing behavior
- No material impact on architecture

**Decide it yourself.** If the decision isn't obvious from convention, record it as an **Assumption** in `PLAN.md` (see `references/plan-template.md`) so it's visible and revisable, but don't block on it.

### C. User decision required

Ask when the unresolved point affects any of:

- User experience / user-visible behavior
- Scope (what's in vs. out)
- A business rule
- Permissions or access control
- Security
- Data integrity
- A deletion/retention policy
- Backward compatibility
- An external API contract
- A destructive or irreversible operation
- A significant architecture tradeoff with no clear precedent in the repo
- An irreversible migration

If none of these apply, it isn't category C — recheck A and B.

## 3. Ask the minimum, concretely

When something does land in category C:

- Ask the fewest questions that unblock planning — batch related ones, don't drip them out one at a time.
- Prefer concrete choices over open-ended questions ("Should deleted orders be soft-deleted or hard-deleted?" beats "How should deletion work?").
- State the tradeoff briefly if it's not obvious, then let the user pick.

## 4. Interview termination conditions

Stop asking and move to plan creation once **all** of the following hold:

- The objective is unambiguous
- Scope is clear enough to bound the work
- Every category-C item has been resolved (answered by the user, or genuinely doesn't apply)
- Every architecture constraint that mattered has been resolved
- Acceptance Criteria can now be written concretely
- Everything else can be decided from repository convention as work proceeds (category B)

You do not need every conceivable detail nailed down — only what's needed to start executing correctly and safely.

## 5. After the interview: don't wait for plan approval

Once termination conditions are met, create the Plan Workspace (`references/planning.md`) and **start executing** — do not stop to ask "does this plan look right?" as a matter of course. This is deliberate: the whole point of a verifiable Goal + evidence-driven loop is that correctness is checked by execution and verification, not by a pre-approval ritual.

Exceptions — pause for explicit plan approval before executing:

1. The user explicitly asked to review/approve the plan first.
2. The plan includes a destructive operation (data deletion, irreversible migration, force-push, etc.).
3. A significant architecture decision remains unresolved even after the interview (rare, if termination conditions were actually met).
4. The work carries a meaningful risk of data loss.

Outside those four cases, proceed straight into `references/execution-loop.md`.
