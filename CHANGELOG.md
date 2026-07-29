# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses semantic versioning for marketplace releases.

## [Unreleased]

### Changed

- Renamed the public product to Code Security Skills.
- Replaced the marketplace, plugin, command namespace, directory, and maintainer-facing URLs with provider-neutral identifiers.
- Rewrote all thirteen workflows around explicit capabilities rather than a named model, coordinator, desktop application, or proprietary lifecycle.
- Introduced the independent `code-security` artifact contract, including new document types, schema identifiers, producer names, fingerprints, snapshot digests, and SARIF properties.
- Removed unused source-host preflight, workbench, orchestration, authentication, and coordinator code.
- Replaced the visual identity and regenerated the deterministic example report and SARIF export.

### Compatibility

- This is a breaking namespace and artifact-contract migration.
- Existing installations must add the renamed marketplace and install `code-security-skills@code-security`.
- The new artifact contract is not presented as wire-compatible with the original source contract.

## [0.1.1] - 2026-07-29

### Changed

- Replaced the original maintainer-prefixed marketplace identifier.
- Updated public installation instructions and marketplace maintainer metadata.

## [0.1.0] - 2026-07-29

### Added

- Initial Claude Code marketplace with thirteen attributed security workflows.
- Standard, deep, and diff scan workflows.
- Bundled references, schemas, deterministic Python helpers, and canonical artifact examples.
- Apache-2.0 attribution and pinned upstream provenance.

[Unreleased]: https://github.com/barvhaim/code-security-skills/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/barvhaim/code-security-skills/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/barvhaim/code-security-skills/releases/tag/v0.1.0
