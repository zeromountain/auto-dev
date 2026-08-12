#!/usr/bin/env python3
"""Validate SKILL.md files under agent-skills/ against the Agent Skills spec
(https://agentskills.io/specification) plus this repo's own conventions.

Checks:
  - required frontmatter fields (name, description) present
  - name: <=64 chars, lowercase/digits/hyphen only, no leading/trailing/double
    hyphen, matches parent directory name
  - description: 1-1024 chars
  - only the 6 spec-defined frontmatter fields are used (portability: extra
    keys are rejected by claude.ai / Skills API validation)
  - SKILL.md body <=500 lines (progressive disclosure budget)
  - every relative markdown link / bare reference to references/*.md,
    scripts/*, assets/* actually exists on disk

No third-party dependencies (stdlib only), so it runs the same way in any
host's sandbox.
"""
import re
import sys
from pathlib import Path

SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_SKILL_MD_LINES = 500

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = Path(__file__).resolve().parent


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, "SKILL.md must start with '---' YAML frontmatter"
    end = text.find("\n---", 4)
    if end == -1:
        return None, "unterminated frontmatter (missing closing '---')"
    raw = text[4:end]
    fields = {}
    current_key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")):
            # nested value (e.g. under `metadata:`) - skip, not needed for validation
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            return None, f"unparseable frontmatter line: {line!r}"
        key, val = m.group(1), m.group(2).strip()
        fields[key] = val
        current_key = key
    return fields, None


def validate_skill(skill_dir: Path) -> list[str]:
    errors = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir}: missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8")
    fields, err = parse_frontmatter(text)
    if err:
        return [f"{skill_md}: {err}"]

    extra = set(fields) - SPEC_FIELDS
    if extra:
        errors.append(f"{skill_md}: non-spec frontmatter fields {sorted(extra)} "
                       f"(breaks claude.ai / Skills API validation)")

    for required in ("name", "description"):
        if required not in fields or not fields[required]:
            errors.append(f"{skill_md}: missing required field '{required}'")

    name = fields.get("name", "")
    if name:
        if len(name) > 64:
            errors.append(f"{skill_md}: name exceeds 64 chars ({len(name)})")
        if not NAME_RE.match(name):
            errors.append(f"{skill_md}: name '{name}' violates lowercase/digits/hyphen rule")
        if "--" in name:
            errors.append(f"{skill_md}: name '{name}' has consecutive hyphens")
        if name != skill_dir.name:
            errors.append(f"{skill_md}: name '{name}' != parent directory '{skill_dir.name}'")

    desc = fields.get("description", "")
    if desc and len(desc) > 1024:
        errors.append(f"{skill_md}: description exceeds 1024 chars ({len(desc)})")

    line_count = text.count("\n") + 1
    if line_count > MAX_SKILL_MD_LINES:
        errors.append(f"{skill_md}: {line_count} lines exceeds {MAX_SKILL_MD_LINES}-line budget")

    # verify every references/, scripts/, assets/ path mentioned in SKILL.md or
    # in reference files themselves actually exists (one level deep from SKILL.md)
    ref_pattern = re.compile(r"(?:references|scripts|assets)/[A-Za-z0-9_./-]+\.\w+")
    all_md = [skill_md] + sorted((skill_dir / "references").glob("*.md")) if (skill_dir / "references").exists() else [skill_md]
    for md_file in all_md:
        content = md_file.read_text(encoding="utf-8")
        for match in ref_pattern.findall(content):
            target = skill_dir / match
            if not target.exists():
                errors.append(f"{md_file}: references missing path '{match}'")

    return errors


def main() -> int:
    skill_dirs = [
        p.parent for p in SKILLS_DIR.glob("*/SKILL.md")
    ]
    if not skill_dirs:
        print(f"no skills found under {SKILLS_DIR}")
        return 1

    all_errors = []
    for skill_dir in skill_dirs:
        errs = validate_skill(skill_dir)
        all_errors.extend(errs)
        status = "OK" if not errs else f"{len(errs)} error(s)"
        print(f"[{status}] {skill_dir.relative_to(REPO_ROOT)}")

    if all_errors:
        print()
        for e in all_errors:
            print(f"  - {e}")
        print(f"\n{len(all_errors)} error(s) found.")
        return 1

    print("\nAll skills valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
