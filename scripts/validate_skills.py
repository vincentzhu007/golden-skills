#!/usr/bin/env python3
"""Check the repository's basic skill packaging conventions."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
FIELD = re.compile(r"^(name|description):\s*(.+?)\s*$", re.MULTILINE)


def check_skill(directory: Path) -> list[str]:
    errors = []
    if not NAME.fullmatch(directory.name) or len(directory.name) >= 64:
        errors.append(f"{directory}: invalid skill name")
    source = directory / "SKILL.md"
    if not source.is_file():
        return errors + [f"{source}: missing SKILL.md"]

    content = source.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return errors + [f"{source}: missing YAML frontmatter"]
    fields = dict(FIELD.findall(match.group(1)))
    if fields.get("name", "").strip('"\'') != directory.name:
        errors.append(f"{source}: frontmatter name must match directory")
    if not fields.get("description", "").strip('"\''):
        errors.append(f"{source}: description is required")
    if not content[match.end():].strip():
        errors.append(f"{source}: instructions are empty")
    if any(token in content for token in ("[TODO]", "TODO:", "<skill-name>")):
        errors.append(f"{source}: unfinished placeholder")
    return errors


def main() -> int:
    if not SKILLS.is_dir():
        print("skills/: missing", file=sys.stderr)
        return 1
    directories = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    if not directories:
        print("skills/: no skills found", file=sys.stderr)
        return 1
    errors = [error for directory in directories for error in check_skill(directory)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(directories)} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
