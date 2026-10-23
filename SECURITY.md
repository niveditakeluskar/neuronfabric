# Security policy

## Reporting a vulnerability

Do not open a public issue. Report vulnerabilities privately through **GitHub private vulnerability reporting** on this repository, or directly to the Security Lead.

> The security contact address and response SLA are **not yet assigned** (see FND-014). Until they are, private GitHub reports are the only channel.

Include the affected component and version or commit, reproduction steps, impact, and any proof-of-concept. Do not access data that is not yours, and do not test against customer systems.

## Supported versions

There are no released versions. This repository is pre-G0 (project initialization).

## Secrets and sensitive data

- Never commit secrets, private keys, certificates with private material, tokens, customer telemetry, prompts or credentials. `.gitignore` blocks common patterns, but it is not a control.
- Signing keys live only in KMS/HSM or a protected signing service, never in CI environment variables (TDS §E2, NG-SEC-010).
- Diagnostic and support bundles are redacted by default (NG-OPS-007).
- The original specification documents are classified *Internal / Controlled* (TDS v2) and *CONFIDENTIAL* (Master Plan v6). They are not stored in this repository (FND-013). Only their hashes and derived engineering content are tracked.

## Release-blocking security conditions

Any of the following blocks a release (TDS §E3): kernel panic, Windows bugcheck, irreversible host lockout, cross-tenant data leakage, unsigned policy or firmware accepted, or prevention enforced without a recorded capability and safety sign-off.

## Security-sensitive changes

PRs that touch sensors, policy, response, PKI/enrollment, the PAM gateway, contracts, release/signing or `security/` need Security Lead review (see [CONTRIBUTING.md](CONTRIBUTING.md#3-pull-requests)).
