# Plan Workspaces

Loaded during: creating or updating a Plan Workspace, deciding how to size it, deciding whether this request continues an existing plan.

## Never accumulate into one root PLAN.md

Every development Goal gets its own isolated workspace. Do not add "just one more feature" to an existing plan's scope unless it's genuinely the same goal (see "Existing active plans" below) — that's how a single PLAN.md ends up mixing unrelated, stale requirements.

## Layout

```
.plans/
├── INDEX.md
├── active/
│   └── <plan-id>/
└── completed/
    └── <plan-id>/
```

### `plan-id`

Short, stable, kebab-case, describing *what*, not *that-it's-a-task*.

Good: `order-cdc`, `customer-sync`, `refresh-token`, `admin-order-filter`
Bad: `task`, `feature`, `new-feature`, `plan-1`

## Sizing: Small / Medium / Large

Judge by **semantic complexity**, not a file-count rule of thumb. Ask: how much execution history will actually be worth preserving, and how many genuinely independent, separately-verifiable chunks does this decompose into?

### Small

```
<plan-id>/
└── PLAN.md
```

Use when: 3 or fewer milestones, small blast radius, little debugging history expected. Most bug fixes and small features land here.

### Medium

```
<plan-id>/
├── PLAN.md
└── LOG.md
```

Use when: multiple components affected, repeated validate/fix cycles are likely, and a history of what was tried is worth keeping separate from current state.

### Large

```
<plan-id>/
├── PLAN.md
├── LOG.md
└── milestones/
    ├── M01-xxx.md
    ├── M02-xxx.md
    └── ...
```

Use when any of: more than ~5 substantial milestones, multiple applications/services involved, multiple databases, several external systems, an architecture change, infrastructure work, a migration, CDC/ETL/data-pipeline work, large-scale refactoring, or work you expect to genuinely span many iterative sessions.

In a Large plan, `PLAN.md` becomes the execution controller — current state, current milestone, index — and the detailed requirements for each milestone move to `milestones/M0N-<name>.md` (see `references/milestone-template.md`). Don't let `PLAN.md` re-absorb that detail as the plan grows; split a milestone file out as soon as a milestone's spec starts crowding `PLAN.md`.

If a plan starts Small or Medium and later grows past its bucket's triggers, upgrade it (move detail into `LOG.md` or `milestones/`) rather than letting the original file balloon — this is a safe, autonomous **Plan Evolution** move (see `references/execution-loop.md`), not a decision that needs the user.

## Existing active plans: continuation, extension, or new?

Before creating a plan, check `.plans/active/`. If something is already there, determine which of these the current request is:

1. **Continuation** of an existing plan's goal (e.g. picking up an unfinished milestone, or the user is asking for the next step of the same feature) → use the existing plan, don't create a new one.
2. **Scope extension of the same goal** (a closely related requirement that's still fundamentally the same objective) → update the existing `PLAN.md`'s Scope and Milestone Index; still one plan.
3. **An independent goal** (different objective, even if it touches overlapping code) → create a new plan.

Determine this from the repository and the active plan's `PLAN.md` — read its Objective and Scope sections, compare against the new request. Ask the user only when it's genuinely undecidable from that (rare); don't ask reflexively.

## INDEX.md: a registry, not a summary

`.plans/INDEX.md` stays lightweight — one row per plan, nothing else. Never put implementation detail here.

```markdown
# Development Plans

## Active

| Plan | Goal | Status | Current Milestone |
|---|---|---|---|

## Completed

| Plan | Goal | Completed |
|---|---|---|
```

Update it when a plan is created, when its current milestone changes, and on archival (`references/completion.md`).

## PLAN.md vs LOG.md: current state vs. history

- **PLAN.md** — durable state and the goal contract. What's true *now*. See `references/plan-template.md` for its exact sections.
- **LOG.md** — what happened. Append-only, but selective: significant implementation changes, validation failures with root cause, debugging discoveries, strategy changes, architecture deviations, and milestone-completion evidence. Not a transcript of every shell command run.

Don't let debugging history accumulate inside `PLAN.md`; that's exactly what `LOG.md` is for. See `references/execution-loop.md` for what belongs in each during execution, and the "Context loading" section of `SKILL.md` for why unrelated/old plan content should stay unloaded by default.
