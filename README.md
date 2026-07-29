# Code Security Skills

<p align="center">
  <img src="docs/social-preview.png" alt="Code Security Skills: 13 evidence-driven security workflows in one plugin" width="100%">
</p>

<p align="center">
  <a href="https://github.com/barvhaim/code-security-skills/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/barvhaim/code-security-skills/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/barvhaim/code-security-skills/releases"><img alt="Release" src="https://img.shields.io/github/v/release/barvhaim/code-security-skills?display_name=tag"></a>
  <a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-blue.svg"></a>
  <img alt="Claude Code plugin" src="https://img.shields.io/badge/Claude_Code-plugin-6b5cff">
</p>

Thirteen evidence-driven workflows for threat modeling, code review, finding validation, attack-path analysis, remediation, tracking, and deterministic security reporting.

The procedures are provider-neutral: they describe required capabilities and evidence, not a particular model, coordinator, desktop application, or proprietary service. This repository packages them as a Claude Code plugin.

## Install

Open Claude Code and run:

```text
/plugin marketplace add barvhaim/code-security-skills
/plugin install code-security-skills@code-security
/reload-plugins
```

Review the current branch, PR, commit, staged changes, or working tree:

```text
/code-security-skills:security-diff-scan Review the current working tree for security regressions. Do not modify files.
```

Or scan the whole repository:

```text
/code-security-skills:security-scan Scan this repository. Do not modify source files.
```

By default, scan artifacts are written outside the target repository under the active system temporary directory at `code-security-scans/<repository>/`; you can select another output directory.

## Pick the right workflow

| Goal | Command |
| --- | --- |
| Review a PR, commit, branch, patch, staged changes, or working tree | `/code-security-skills:security-diff-scan` |
| Run the default single-pass repository audit | `/code-security-skills:security-scan` |
| Run repeated independent discovery passes for higher recall | `/code-security-skills:deep-security-scan` |
| Map assets, trust boundaries, entry points, and abuse cases | `/code-security-skills:threat-model` |
| Investigate a candidate vulnerability | `/code-security-skills:finding-discovery` |
| Reproduce or disprove a candidate finding | `/code-security-skills:validation` |
| Connect validated findings into attacker journeys | `/code-security-skills:attack-path-analysis` |
| Draft a vulnerability report | `/code-security-skills:vulnerability-writeup` |
| Implement and verify a narrow fix | `/code-security-skills:fix-finding` |
| Propose hardening without editing source | `/code-security-skills:propose-security-hardening` |
| Triage a ticket, advisory, or report | `/code-security-skills:triage-finding` |
| Synchronize validated findings with trackers | `/code-security-skills:track-findings` |
| Define a repository security policy | `/code-security-skills:define-security-policy` |

## Provider-neutral execution model

Each workflow declares the capability it needs instead of assuming a named host runtime:

- Repository access through file, search, and bounded shell capabilities.
- Optional independent workers or subagents for repeated discovery passes.
- Explicit tracker capabilities for identity, search, mutation, and exact readback.
- Optional host-native review annotations only when the host documents them.
- Deterministic local helpers for normalization, validation, sealing, report generation, and SARIF export.

Claude Code supplies the current packaging and command namespace. The procedures can be adapted to another coding agent that offers equivalent capabilities and preserves the same trust boundaries.

## Independent artifact contract

The scan workflows produce the provider-neutral `code-security` contract:

- `scan-manifest.json` for target identity, scope, status, producer, and artifact hashes.
- `findings.json` for structured findings, evidence, confidence, severity, and remediation.
- `coverage.json` for reviewed surfaces, exclusions, and deferred work.
- `report.md` as a deterministic human-readable projection.
- `exports/results.sarif` for compatible code-scanning tools.

The contract uses independent document types, schema identifiers, producer names, fingerprints, snapshot digests, and SARIF properties. It is not presented as wire-compatible with the upstream source contract.

A bundled deterministic fixture demonstrates the final output without model credentials:

| Result | Value |
| --- | --- |
| Finding | Unsafe archive extraction can escape the output directory |
| Severity | High, CVSS 8.1 |
| Confidence | High |
| Taxonomy | CWE-22, path traversal |
| Coverage | Complete |

View the generated [example report](plugins/code-security-skills/examples/completed-scan/report.md) and [SARIF export](plugins/code-security-skills/examples/completed-scan/exports/results.sarif). The example proves deterministic artifact generation, not model accuracy.

## Why one plugin

The skills share references, schemas, artifact contracts, and deterministic helpers. Packaging them together preserves relative links and installs one coherent workflow instead of thirteen incomplete fragments. Claude Code discovers each skill independently under the `code-security-skills` namespace.

## Local development

Add a local checkout as a marketplace:

```text
/plugin marketplace add /absolute/path/to/code-security-skills
/plugin install code-security-skills@code-security
/reload-plugins
```

Or load only the plugin during development:

```bash
claude --plugin-dir ./plugins/code-security-skills
```

Run the verification suite:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_portability.py
python3 scripts/smoke_finalize.py
python3 scripts/smoke_plugin_load.py
claude plugin validate .
claude plugin validate ./plugins/code-security-skills
```

See [`PROVENANCE.md`](plugins/code-security-skills/PROVENANCE.md) for the exact derivation and runtime boundary.

## Repository structure

```text
.claude-plugin/marketplace.json
plugins/code-security-skills/
├── .claude-plugin/plugin.json
├── skills/
├── references/
├── scripts/
├── schemas/
├── examples/
├── PROVENANCE.md
├── THIRD_PARTY_NOTICES.md
└── UPSTREAM_SOURCE.json
```

## Compatibility and limitations

Installing this plugin installs prompts, references, schemas, examples, and deterministic Python helpers. It does not install a coordinator, hosted scanning service, model credentials, tracker integration, or desktop application.

Linear and Jira tracking require separately configured MCP or tool integrations with identity, search, mutation, and exact-readback capabilities. GitHub tracking can use an explicitly selected authenticated `gh` identity.

Schema-valid output does not prove that a model-generated finding is correct or that every vulnerability was found. Review findings before making consequential security decisions.

## Contributing and security

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before changing derivative files or the artifact contract. Report vulnerabilities according to [`SECURITY.md`](SECURITY.md).

## Provenance and license

Code Security Skills is an independent, unofficial derivative of workflows originally published in [OpenAI Codex Security](https://github.com/openai/codex-security). It is not affiliated with or endorsed by OpenAI or Anthropic.

- Pinned source revision: `f22d4a36f26d16287bcdfd707b369116e02a08c3`
- Original copyright: Copyright 2025 OpenAI
- License: Apache License 2.0

See [`LICENSE`](LICENSE), [`PROVENANCE.md`](plugins/code-security-skills/PROVENANCE.md), [`THIRD_PARTY_NOTICES.md`](plugins/code-security-skills/THIRD_PARTY_NOTICES.md), and [`UPSTREAM_SOURCE.json`](plugins/code-security-skills/UPSTREAM_SOURCE.json).
