---
name: autonomous-development
description: Autonomous development execution protocol. Use when the user hands you a development requirement and expects the codebase investigated, a scoped plan produced, and the work driven to a verified completion with minimal back-and-forth. Covers repository discovery, targeted interviewing, isolated plan workspaces, an evidence-driven implement/verify/fix loop, and archival. Triggers on phrases like "build X", "implement X", "자동으로 개발해줘", or any multi-step feature/fix request where the agent is expected to work autonomously to a verifiable end state rather than produce a single patch.
---

<!-- Always respond to the user in the user's language, regardless of this file's language. -->

# Autonomous Development Protocol

This is not a template for writing plan documents. It is an **execution protocol**:

```
User Intent → Repository Knowledge → Structured Decisions →
Isolated Plan Workspace → Native Goal → Evidence-driven Loop → Verified Software
```

Keep these roles separate. Never let one absorb another:

| Layer | Role |
|---|---|
| `AGENTS.md` / `CLAUDE.md` | Project rules (framework, convention, forbidden patterns) |
| This skill | Execution protocol (discover → interview → plan → goal → implement → verify → archive) |
| Plan Workspace (`.plans/active/<id>/`) | Current mission state |
| Native `/goal` | Completion condition |
| Inner loop | Execution strategy |
| `LOG.md` | Historical evidence |

## Lifecycle

```
USER REQUEST
  → REPOSITORY DISCOVERY          (references/discovery.md)
  → REQUIREMENT CLASSIFICATION    (references/discovery.md)
  → USER INTERVIEW (only if needed)
  → PLAN WORKSPACE CREATION       (references/planning.md, plan-template.md, milestone-template.md)
  → PLAN VALIDATION
  → GOAL SET                      (references/hosts.md)
  → loop per milestone:
      CURRENT MILESTONE SELECTION
      → INSPECT → IMPLEMENT → VERIFY   (references/execution-loop.md, verification.md)
      → PASS: DONE CRITERIA CHECK → milestone complete → next milestone
      → FAIL: ANALYZE → FIX → RE-VERIFY   (references/execution-loop.md)
  → FINAL VERIFICATION            (references/completion.md)
  → GOAL COMPLETE
  → ARCHIVE PLAN                  (references/completion.md)
```

## Non-negotiable policies

1. **Discover before asking.** Investigate the repository first. Never open with a batch of questions — most answers already exist in code or docs. See `references/discovery.md`.
2. **Classify every open question** as repository-resolvable / safe implementation decision / user-decision-required. Only the third category reaches the user, and only the minimum necessary questions are asked. See `references/discovery.md`.
3. **One Goal, one isolated Plan Workspace.** Never accumulate every feature into a single root `PLAN.md`. Each goal gets `.plans/active/<plan-id>/`. See `references/planning.md`.
4. **Size the plan to the work**, not by habit — Small/Medium/Large based on semantic complexity, not a fixed file count. See `references/planning.md`.
5. **Load only what the current milestone needs.** Do not read unrelated active plans, completed plans, completed milestone specs, the full `LOG.md`, or other goals' acceptance criteria by default. See "Context loading" below and `references/execution-loop.md`.
6. **No proactive approval-seeking.** Once discovery + interview satisfy the termination conditions, create the plan and start executing without asking "should I proceed?" — except the 4 explicit exceptions in `references/discovery.md`.
7. **No verification bypass, ever.** Disabling/deleting tests, weakening assertions, suppressing type errors, disabling lint rules, or fabricating results to claim completion are forbidden outright. See `references/verification.md`.
8. **No passive waiting as a completion condition.** Time elapsing ("wait 7 days", "monitor for 24h") is never a milestone or Goal condition — convert to executable validation (replay, fixtures, simulation) and file real long-horizon observation as Post-Deployment Follow-up. See `references/verification.md`.
9. **Anti-loop.** A repeated failure signature is a signal to change hypothesis and intervention, never a cue to retry the same tactic or to give up after N tries. See `references/execution-loop.md`.
10. **A finding real blocker is rare.** Exhaust docs, config/env, mocks/fixtures, and local/staging alternatives — and keep making progress on independent milestones — before declaring one. See `references/execution-loop.md`.

## When to load which reference

Load reference files on demand, matching the lifecycle stage you are in. Do not pre-load files for stages you have not reached.

| Stage | Load |
|---|---|
| Repository discovery, deciding what to ask | `references/discovery.md` |
| Creating or updating a Plan Workspace, sizing it, resolving "is this a continuation of an existing plan?" | `references/planning.md` |
| Writing/updating `PLAN.md` | `references/plan-template.md` |
| Writing/updating a milestone file (Large plans only) | `references/milestone-template.md` |
| Running the implement/verify/fix loop, hitting a repeated failure, considering declaring a blocker, updating the plan mid-execution | `references/execution-loop.md` |
| Choosing what to run to verify a change, deciding a milestone or the goal is actually done | `references/verification.md` |
| Finishing a goal, deciding what to archive | `references/completion.md` |
| Setting the native goal, detecting which host (Claude Code / Codex / other) you're running in | `references/hosts.md` |

Never read `references/*` speculatively "just in case" — each file is scoped to one lifecycle stage.

## Context loading (Progressive Disclosure)

The point of restricting what loads by default is **not primarily token cost** — it's preventing a stale requirement from a different goal (or an old milestone in the same goal) from silently steering the current work.

Default context for a milestone in progress:

1. Project instructions (`AGENTS.md` / `CLAUDE.md` and anything they point to)
2. The active plan's `PLAN.md`
3. The **current** milestone file (Large plans) — not other milestone files
4. Repository code directly relevant to the current milestone

Do **not** load by default: other active plans, completed plans, completed milestone specs, the full `LOG.md`, or another goal's acceptance criteria. Read a specific `LOG.md` section or a specific completed milestone only when you have a concrete reason (e.g. debugging references an earlier decision) — and say why you're reading it.

## Quick start

1. Read `references/discovery.md` and investigate the repository.
2. Classify open questions; ask only what's genuinely required, using concrete choices.
3. Read `references/planning.md`; check `.plans/active/` for a plan this request continues, extends, or is independent from.
4. Create/update the Plan Workspace using `references/plan-template.md` (+ `references/milestone-template.md` if Large).
5. Read `references/hosts.md`; emit the native goal string for the detected host.
6. Drive milestones via `references/execution-loop.md` and `references/verification.md`, without waiting for per-step approval.
7. On completion, run `references/completion.md`'s final review, then archive.
