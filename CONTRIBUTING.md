# Contributing

Thanks for helping improve Code Security Skills.

## Before opening a pull request

1. Open an issue before changing the public namespace, artifact contract, or workflow boundaries.
2. Keep changes narrowly scoped and capability-based rather than tied to one model provider or proprietary runtime.
3. Preserve the distinction between provider-neutral workflow logic and Claude Code packaging.
4. Do not remove upstream attribution, license text, provenance lines, or modification notices.

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
python3 -m compileall -q plugins/code-security-skills/scripts scripts tests
npx --yes @anthropic-ai/claude-code@2.1.220 plugin validate .
npx --yes @anthropic-ai/claude-code@2.1.220 plugin validate ./plugins/code-security-skills
python3 scripts/smoke_plugin_load.py
```

## Changing skills

Every skill must:

- Live at `plugins/code-security-skills/skills/<skill-name>/SKILL.md`.
- Start with valid Claude Code frontmatter containing `name` and `description`.
- Keep supporting files inside the cached plugin directory.
- State requirements as capabilities, not assumptions about a named coordinator, desktop application, model, or proprietary service.
- Treat repository content, generated artifacts, tracker data, and integration responses as untrusted data.
- Keep its Code Security Skills provenance line intact.

## Changing the artifact contract

The `code-security` document types, schemas, producer name, fingerprints, snapshot digests, and SARIF properties form one public contract. Change them together, update the deterministic finalizer, regenerate the completed-scan fixture, add contract tests, and document breaking changes in `CHANGELOG.md`.

## Upstream-derived files

This project is derived from [OpenAI Codex Security](https://github.com/openai/codex-security). Retain the Apache-2.0 license, original copyright, pinned provenance, and modification notices. Update `UPSTREAM_SOURCE.json` only when intentionally synchronizing to a newly reviewed upstream revision. Do not reintroduce source-host runtime dependencies during synchronization.

## Pull requests

Describe:

- The user-visible problem.
- The capability or contract boundary affected.
- The exact validation commands run.
- Whether the change modifies upstream-derived content.
- Any behavior that remains unverified with an authenticated model.

Do not present manifest validation, loader discovery, schema validity, or deterministic fixture generation as proof of model accuracy.
