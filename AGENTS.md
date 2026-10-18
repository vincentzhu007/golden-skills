# Repository guidance

This repository maintains the user's personal skills.

- Treat `skills/` as the source of truth. Put each skill in `skills/<lowercase-hyphenated-name>/SKILL.md` with `name` and `description` YAML frontmatter.
- Ask for real examples when a proposed skill's inputs, output, or decision criteria cannot be inferred. Continue with repo maintenance that does not depend on the answer.
- Keep each skill scoped to one repeatable job. Prefer useful decision rules over generic instructions or a transcript of one successful run.
- Add `references/`, `scripts/`, and `assets/` only when the skill needs them. Scripts must be exercised on a representative safe case.
- Before finishing a skill change, run `python3 scripts/validate_skills.py` and check the skill against a realistic request. Do not claim the validator proves behavior.
- Do not copy private data, credentials, or project-specific facts into a reusable skill unless the user explicitly wants that content there.
- Do not install skills outside this repository or publish them merely because they were created here; follow the user's requested scope.
