# Security policy

## Supported versions

Security fixes are applied to the latest release and the `main` branch.

## Reporting a vulnerability

Please do not disclose an exploitable vulnerability in a public issue.

Use GitHub's **Security** tab and choose **Report a vulnerability** when private vulnerability reporting is available. If that option is unavailable, contact the repository owner through the [barvhaim GitHub profile](https://github.com/barvhaim) before sharing sensitive details publicly.

Include:

- The affected file and revision.
- Reproduction steps or a minimal proof of concept.
- The security impact and required preconditions.
- Any suggested mitigation.

## Scope

Report vulnerabilities in this repository's Claude Code adaptation, plugin packaging, helper scripts, validation logic, or generated artifacts here.

For vulnerabilities in the original Codex Security project, follow the upstream project's reporting process at [openai/codex-security](https://github.com/openai/codex-security).

For vulnerabilities in Claude Code itself, use Anthropic's security reporting process.

## Security boundary

This plugin provides model-guided security-review workflows. It is not a sandbox, an authorization boundary, or a guarantee that all vulnerabilities will be found. Generated findings require human review before consequential use.
