# gateway/pam/ — Privileged access gateway

Identity-controlled SSH (and RDP via a selected audited component) access with approvals, per-session short-lived credentials, integrity-chained recording and revocation.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §C6 |
| Owner (role) | Security Lead (interim; see FND-014) |
| Claude agent | `central-brain-engineer (with mandatory security-assurance-reviewer review)` |
| Requirements | NG-PAM-001 … NG-PAM-007 |
| Contracts | Session API; recording metadata |
| Gate | G-C6 (NG-PAM-001 program gate G8) |

- RDP component pending ADR-014. Do not promise arbitrary RDP feature coverage.

See [governance/requirements_registry.yaml](../../governance/requirements_registry.yaml) for the requirement details.
