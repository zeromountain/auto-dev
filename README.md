# autonomous-development

A shared Agent Skill — an execution protocol, not a prompt template — for driving a development requirement from raw request to verified, archived completion. Works identically in Claude Code and Codex (and any other host implementing the [Agent Skills](https://agentskills.io) open standard).

```
User Intent → Repository Knowledge → Structured Decisions →
Isolated Plan Workspace → Native Goal → Evidence-driven Loop → Verified Software
```

## What it does

1. **Investigates the repository first** — reads `AGENTS.md`/`CLAUDE.md`, README, configs, existing patterns — before asking the user anything.
2. **Classifies every open question** into repository-resolvable / safe-to-decide / needs-the-user, and only asks the last kind, with concrete choices.
3. **Creates an isolated Plan Workspace** per goal (`.plans/active/<plan-id>/`) instead of piling every feature into one root `PLAN.md`, sized Small/Medium/Large by actual complexity.
4. **Drives an implement → verify → fix loop** to each milestone's Done Criteria, with an anti-loop rule (change hypothesis on repeated failure, never blind retry) and a hard ban on faking verification.
5. **Refuses time-based completion conditions** ("wait a week and check") — converts them to executable validation, or files them separately as Post-Deployment Follow-up.
6. **Finishes with a real review** (all criteria checked, full diff reviewed, verification actually run) and archives the plan to `.plans/completed/`.

See `agent-skills/autonomous-development/SKILL.md` for the full protocol and `references/` for the detail on each stage.

## Install into a project

```bash
# from this repo
agent-skills/install.sh /path/to/your/project

# or, if you cloned this repo next to your project and want to keep it that way:
agent-skills/install.sh /path/to/your/project --copy   # only if symlinks aren't viable there
```

This creates:

```
your-project/
├── .claude/skills/autonomous-development -> (symlink to this repo)
└── .agents/skills/autonomous-development  -> (symlink to this repo)
```

Restart Claude Code / Codex in the target project afterward so it picks up the new skill directory.

## Invoke it

- Claude Code: `/autonomous-development <your requirement>`
- Codex: `$autonomous-development <your requirement>`

Or just describe a development requirement in plain language — the skill's `description` frontmatter is written so both hosts trigger it automatically.

## Validate after editing the skill

```bash
python3 agent-skills/validate.py
```

Checks frontmatter against the [Agent Skills spec](https://agentskills.io/specification) (name/description constraints, only spec-defined fields), the 500-line `SKILL.md` budget, and that every path referenced under `references/` actually exists.

## Repository layout

```
auto-dev/
├── AGENTS.md               # project rules for *this* repo (CLAUDE.md symlinks here)
├── CLAUDE.md -> AGENTS.md
├── README.md                # this file
└── agent-skills/
    ├── install.sh
    ├── validate.py
    └── autonomous-development/
        ├── SKILL.md
        └── references/
            ├── discovery.md
            ├── planning.md
            ├── plan-template.md
            ├── milestone-template.md
            ├── execution-loop.md
            ├── verification.md
            ├── completion.md
            └── hosts.md
```
