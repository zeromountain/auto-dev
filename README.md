# auto-dev

A shared Agent Skill — an execution protocol, not a prompt template — for driving a development requirement from raw request to verified, archived completion. Distributed as a plugin that installs identically in Claude Code and Codex.

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

See `skills/autonomous-development/SKILL.md` for the full protocol and `references/` for the detail on each stage.

## Install as a plugin (recommended)

This repository is both a plugin and a marketplace (`auto-dev`), following the same layout as `ponytail` and other multi-host plugins.

**Codex:**

```bash
codex plugin marketplace add zeromountain/auto-dev
codex plugin add auto-dev@auto-dev
```

**Claude Code:**

```text
/plugin marketplace add zeromountain/auto-dev
/plugin install auto-dev@auto-dev
```

Then restart the session. Invoke with `/auto-dev:autonomous-development` (Claude Code) or `$auto-dev:autonomous-development` (Codex) — or just describe a development requirement in plain language, since the skill's `description` frontmatter is written for both hosts to trigger it automatically.

Update with `codex plugin marketplace upgrade auto-dev` / `/plugin marketplace update auto-dev`.

## Install without the plugin system (fallback)

For hosts or setups where installing as a plugin isn't an option, `scripts/install.sh` symlinks the skill directly:

```bash
git clone https://github.com/zeromountain/auto-dev.git
auto-dev/scripts/install.sh /path/to/your/project

# or, if symlinks aren't viable on your filesystem:
auto-dev/scripts/install.sh /path/to/your/project --copy
```

This creates `.claude/skills/autonomous-development` and `.agents/skills/autonomous-development` as symlinks into the cloned repo. Restart Claude Code / Codex in the target project afterward.

## Validate after editing the skill or manifests

```bash
python3 scripts/validate.py       # SKILL.md frontmatter, references, 500-line budget
claude plugin validate . --strict # plugin.json / marketplace.json schema
```

## Repository layout

```
auto-dev/
├── .claude-plugin/
│   ├── marketplace.json    # marketplace catalog (read by both hosts)
│   └── plugin.json         # Claude Code plugin manifest
├── .codex-plugin/
│   └── plugin.json         # Codex plugin manifest
├── skills/
│   └── autonomous-development/
│       ├── SKILL.md
│       └── references/
│           ├── discovery.md
│           ├── planning.md
│           ├── plan-template.md
│           ├── milestone-template.md
│           ├── execution-loop.md
│           ├── verification.md
│           ├── completion.md
│           └── hosts.md
├── scripts/
│   ├── install.sh           # fallback installer (see above)
│   └── validate.py
├── AGENTS.md                # project rules for *this* repo (CLAUDE.md symlinks here)
├── CLAUDE.md -> AGENTS.md
└── README.md                 # this file
```
