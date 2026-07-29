# Codex Security Skills for Claude

An unofficial Claude Code marketplace containing all thirteen open-source security skills bundled with OpenAI Codex Security, adapted to run as one Claude Code plugin.

This project is not affiliated with or endorsed by OpenAI or Anthropic.

## Why one plugin

The skills share references, schemas, artifact contracts, and Python helpers. Packaging them together preserves those relative links and installs one coherent security-review workflow instead of thirteen incomplete fragments.

After installation, every skill is available under the `codex-security-skills` namespace.

## Included skills

- `/codex-security-skills:security-scan`
- `/codex-security-skills:deep-security-scan`
- `/codex-security-skills:security-diff-scan`
- `/codex-security-skills:threat-model`
- `/codex-security-skills:finding-discovery`
- `/codex-security-skills:validation`
- `/codex-security-skills:attack-path-analysis`
- `/codex-security-skills:vulnerability-writeup`
- `/codex-security-skills:fix-finding`
- `/codex-security-skills:propose-security-hardening`
- `/codex-security-skills:triage-finding`
- `/codex-security-skills:track-findings`
- `/codex-security-skills:define-security-policy`

## Local installation

Start Claude Code and add this repository as a local marketplace:

```text
/plugin marketplace add /absolute/path/to/codex-security-claude-marketplace
/plugin install codex-security-skills@njs-security-skills
/reload-plugins
```

## Installation from GitHub

Users with access to the private repository can add it directly:

```text
/plugin marketplace add barvhaim/codex-security-claude-marketplace
/plugin install codex-security-skills@njs-security-skills
/reload-plugins
```

Then invoke a skill explicitly:

```text
/codex-security-skills:threat-model
```

Or ask Claude naturally to perform a security task matching a skill's description.

## Development loading

Load the plugin directly without installing the marketplace:

```bash
claude --plugin-dir ./plugins/codex-security-skills
```

## Validation

Validate the marketplace and all plugin components with Claude Code:

```bash
claude plugin validate .
claude plugin validate ./plugins/codex-security-skills
```

Run the repository checks:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_portability.py
```

Exercise the deterministic upstream finalizer using the bundled contract example:

```bash
python3 scripts/smoke_finalize.py
```

Exercise Claude Code's real plugin loader without requiring model authentication:

```bash
python3 scripts/smoke_plugin_load.py
```

## Architecture

The repository contains one marketplace and one multi-skill plugin:

```text
.claude-plugin/marketplace.json
plugins/codex-security-skills/
├── .claude-plugin/plugin.json
├── skills/
├── references/
├── scripts/
├── schemas/
├── examples/
├── ADAPTATION.md
├── THIRD_PARTY_NOTICES.md
└── UPSTREAM_SOURCE.json
```

The top-level scan workflows were rewritten for Claude Code. The detailed phase skills, references, schemas, examples, and deterministic Python helpers are derived from the pinned upstream source.

## Compatibility and limitations

Installing this plugin does not install the Codex Security product, Codex SDK, Codex desktop application, or Codex Security MCP coordinator.

The port does not reproduce upstream authentication, desktop setup, resumable deep-scan coordination, durable MCP lifecycle, or SDK event streaming. Deep scans use Claude Code subagents when available and sequential independent passes otherwise.

The canonical JSON contract and finalizer can validate artifact structure and consistency. They do not prove that a model-generated finding is correct or that every vulnerability was found.

Read [`ADAPTATION.md`](plugins/codex-security-skills/ADAPTATION.md) before relying on the plugin for consequential security decisions.

## Upstream and license

Original project: <https://github.com/openai/codex-security>

Pinned source revision: `f22d4a36f26d16287bcdfd707b369116e02a08c3`

Original copyright: Copyright 2025 OpenAI

License: Apache License 2.0. See [`LICENSE`](LICENSE) and [`THIRD_PARTY_NOTICES.md`](plugins/codex-security-skills/THIRD_PARTY_NOTICES.md).
