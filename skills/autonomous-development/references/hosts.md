# Host adapter: native Goal

This is the **only** file in this skill allowed to contain host-specific instructions. Everything else in this skill must stay host-neutral so it works identically in Claude Code, Codex, or any other Agent-Skills-compatible host. If you find yourself writing "if Claude Code..." anywhere else, move that logic here instead.

## Detecting the host

You generally already know which CLI you're running as (Claude Code vs Codex vs something else). If genuinely unsure, prefer the host-neutral fallback in "No native goal available" below rather than guessing.

## Once the Plan Workspace exists: emit the goal string, don't just describe it

A skill's body cannot execute a slash command itself — setting a native goal is a user/host action. So after `PLAN.md` is validated, output a ready-to-run goal line the user (or the surrounding automation) can fire immediately. Reference the plan by its exact path — never a description of it — so the goal can't drift onto unrelated work.

```
/goal Execute `.plans/active/<plan-id>/PLAN.md` completely: all required
milestones complete, all acceptance criteria satisfied, required verification
passes, no known blocking regression remains.
```

Then **keep working the inner loop regardless of whether the goal was actually set** — the loop (`references/execution-loop.md`) is what makes progress; the native goal is a convenience wrapper that keeps a host auto-continuing between turns. Do not stall waiting for the user to type `/goal`.

## Claude Code specifics

- `/goal` is **session-scoped**. It clears when the session ends or `/clear` runs, and does not survive a process restart.
- The evaluator is a small fast model that reads **only the conversation transcript** — it does not run commands or read files itself. This means: **verification output must actually appear in the transcript**, not just be summarized as "tests passed." Paste or let tool output surface the real pass/fail lines before claiming a milestone or the goal is done.
- Condition length is capped (~4000 chars) — keep the emitted goal string short and reference the plan file path rather than restating the whole plan.
- `/loop` is a **separate, time-based** feature (fires on a wall-clock interval, not a completion condition). Do not use it as the development inner loop. Reserve it for genuinely time-driven polling the harness can't otherwise observe — e.g. waiting on a CI run or an external deployment to finish. The implement→verify→fix cycle in `references/execution-loop.md` is condition-driven and runs within a single turn/session, not via `/loop`.

## Codex specifics

- `/goal` is **thread-scoped and persists across process/terminal restarts** — it survives a crash or resume.
- Completion is **evidence-based**: Codex checks the objective against concrete proof (files changed, commands run, tests passed, generated artifacts) rather than a transcript summary. This lines up naturally with the verification ladder in `references/verification.md` — run the real commands, don't just assert results.
- Supports `/goal pause` / `/goal resume` / `/goal clear` and optional token/wall-clock budgets. If the user gives a turn/time budget, include it in the condition (e.g. "...or stop after 20 turns and report the blocker").

## No native goal available

If the host has no persistent-goal feature (or you can't confirm one), don't block on it. Proceed with the inner loop directly: drive milestones to completion using `references/execution-loop.md` and `references/completion.md`'s final review as your own completion gate — the plan's Acceptance Criteria and Completion Criteria sections already define "done" independent of any host feature.
