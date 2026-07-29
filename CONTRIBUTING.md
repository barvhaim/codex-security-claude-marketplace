# Contributing

Thanks for helping improve this Claude Code adaptation.

## Before opening a pull request

1. Check whether the behavior belongs to this port or to the upstream [OpenAI Codex Security](https://github.com/openai/codex-security) project.
2. Open an issue for substantial workflow, contract, or packaging changes.
3. Keep changes narrowly scoped and preserve the distinction between Claude Code behavior and unavailable Codex-specific runtime features.
4. Do not remove upstream attribution or modification notices.

## Development setup

Requirements:

- Python 3.10 or newer.
- Node.js and `npx` for Claude Code manifest and loader checks.
- Claude Code authentication only for model-invocation tests.
- Pillow only when regenerating `docs/social-preview.png` with `python3 scripts/generate_social_preview.py`.

Run the local checks:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_portability.py
python3 scripts/smoke_finalize.py
python3 -m compileall -q plugins/codex-security-skills/scripts scripts tests
npx --yes @anthropic-ai/claude-code@2.1.220 plugin validate .
npx --yes @anthropic-ai/claude-code@2.1.220 plugin validate ./plugins/codex-security-skills
python3 scripts/smoke_plugin_load.py
```

## Changing skills

Every skill must:

- Live at `plugins/codex-security-skills/skills/<skill-name>/SKILL.md`.
- Start with valid Claude Code frontmatter containing `name` and `description`.
- Keep supporting files inside the cached plugin directory.
- Avoid unresolved Codex-only namespaces, MCP lifecycle calls, and host placeholders.
- State clearly when behavior differs from the upstream implementation.

For files derived from OpenAI Codex Security, retain the Apache-2.0 license, upstream copyright, and a prominent modification notice. Update `UPSTREAM_SOURCE.json` only when intentionally synchronizing to a new reviewed upstream revision.

## Pull requests

Describe:

- The user-visible problem.
- The compatibility boundary affected.
- The exact validation commands run.
- Whether the change modifies upstream-derived content.
- Any behavior that remains unverified with an authenticated Claude model.

Do not present manifest validation or loader discovery as proof of model accuracy.
