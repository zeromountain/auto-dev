# auto-dev

This repository holds a single shared Agent Skill, distributed as a plugin (and marketplace) named `auto-dev` for both Claude Code and Codex.

## What lives here

- `skills/autonomous-development/` — the skill source (`SKILL.md` + `references/`). This is the only content that matters; everything else supports distributing it.
- `.claude-plugin/marketplace.json` — the marketplace catalog. Both hosts read this file directly (confirmed against Codex 0.146.1 — `codex plugin list` resolves third-party marketplaces through `.claude-plugin/marketplace.json`, there is no separate Codex-specific marketplace manifest needed).
- `.claude-plugin/plugin.json` — Claude Code plugin manifest.
- `.codex-plugin/plugin.json` — Codex plugin manifest. Needs its own `"skills": "./skills/"` field; Claude Code discovers `skills/` automatically and ignores this file.
- `scripts/install.sh` — fallback symlink installer for setups that don't use the plugin system.
- `scripts/validate.py` — validates `SKILL.md` frontmatter and internal references against the Agent Skills spec (stdlib only, no dependencies).

## Conventions for changes in this repo

- Keep `SKILL.md` host-neutral. Any Claude Code- or Codex-specific behavior belongs in `skills/autonomous-development/references/hosts.md`, nowhere else.
- `SKILL.md` frontmatter uses only the six fields defined by the [Agent Skills spec](https://agentskills.io/specification): `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Extra fields break validation on claude.ai and the Skills API.
- Plugin installs **copy** the plugin directory into a per-host cache — don't reference anything outside this repo's own tree (e.g. no `../shared` paths), and don't rely on symlinks *inside* `skills/` surviving that copy.
- Bump `version` in **both** `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` together on every release (and the marketplace entry's `version` if set there) — mismatched versions make one host stop offering updates.
- After editing anything under `skills/`, run `python3 scripts/validate.py` before committing. After editing any manifest, run `claude plugin validate . --strict`.
- Reference files under `references/` are loaded on demand by lifecycle stage — see the table in `SKILL.md`. Don't merge stages back together for convenience; that's what causes the skill to load stale context.

## No project-specific tech stack here

There is no application code in this repository — it exists to define and distribute the skill above. `CLAUDE.md` is a symlink to this file.
