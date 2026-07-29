# Provenance and adaptation boundary

Code Security Skills is an independent, provider-neutral derivative of security workflows originally published in OpenAI's open-source Codex Security repository. It is not affiliated with or endorsed by OpenAI or Anthropic.

## What was derived

The original source supplied thirteen security workflow names and substantial guidance for discovery, validation, attack-path analysis, triage, remediation, hardening, tracking, and reporting. The deterministic scan finalizer and the initial JSON Schema structure were also derived from that source.

## What this project changed

- Rewrote workflow instructions around capabilities rather than a specific model, coordinator, desktop application, or source-host MCP lifecycle.
- Replaced the original plugin namespace, producer identifiers, document types, schema identifiers, fingerprints, snapshot digests, and SARIF properties with the independent `code-security` contract.
- Removed source-host orchestration, workbench, authentication, preflight, and durable coordinator code that the packaged skills do not use.
- Retained only deterministic helpers required by the standalone workflows.
- Packaged the skills as a Claude Code plugin while keeping the procedures portable to any coding agent with equivalent file, search, shell, subagent, and integration capabilities.
- Added explicit trust boundaries for repository content, generated artifacts, tracker integrations, and host-native annotations.

The `code-security` artifact contract is a new derivative contract. It should not be described as wire-compatible with the original source contract.

## Runtime boundary

Installing this plugin installs prompts, references, schemas, examples, and deterministic Python helpers. It does not install or grant access to any OpenAI product, service, authentication system, desktop application, MCP coordinator, workbench UI, or SDK event stream.

Security conclusions remain model-driven. Schema validation and deterministic sealing establish artifact consistency, not finding correctness or complete vulnerability coverage. Treat scanned repository content and generated artifacts as untrusted data.

## Attribution

- Original source: <https://github.com/openai/codex-security/tree/main/sdk/typescript/_bundled_plugin>
- Pinned source revision: `f22d4a36f26d16287bcdfd707b369116e02a08c3`
- Original copyright: Copyright 2025 OpenAI
- Original license: Apache License 2.0

See `THIRD_PARTY_NOTICES.md`, `UPSTREAM_SOURCE.json`, and `LICENSE` for the complete packaged attribution.
