# auto-dev

This repository holds a single shared Agent Skill, published for reuse across projects.

## What lives here

- `agent-skills/autonomous-development/` — the skill source (`SKILL.md` + `references/`). This is the only content that matters; everything else supports distributing it.
- `agent-skills/install.sh` — symlinks (or copies) the skill into a target project's `.claude/skills/` and `.agents/skills/`.
- `agent-skills/validate.py` — validates frontmatter and internal references against the Agent Skills spec (stdlib only, no dependencies).

## Conventions for changes in this repo

- Keep `SKILL.md` host-neutral. Any Claude Code- or Codex-specific behavior belongs in `agent-skills/autonomous-development/references/hosts.md`, nowhere else.
- `SKILL.md` frontmatter uses only the six fields defined by the [Agent Skills spec](https://agentskills.io/specification): `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Extra fields break validation on claude.ai and the Skills API.
- After editing anything under `agent-skills/`, run `python3 agent-skills/validate.py` before committing.
- Reference files under `references/` are loaded on demand by lifecycle stage — see the table in `SKILL.md`. Don't merge stages back together for convenience; that's what causes the skill to load stale context.

## No project-specific tech stack here

There is no application code in this repository — it exists to define and distribute the skill above. `CLAUDE.md` is a symlink to this file.
