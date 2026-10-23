# deploy/terraform/ — Infrastructure as code

Cloud/SaaS infrastructure (regions, networking, managed stores, KMS) and lab environments.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §E2, §E4 |
| Owner (role) | Platform Lead |
| Claude agent | `devsecops-release-engineer` |
| Requirements | NG-SYS-005, NG-DAT-008 |
| Contracts | — |
| Gate | G-E4 |

- Never commit state files or *.tfvars containing secrets (git-ignored).

See [governance/requirements_registry.yaml](../../governance/requirements_registry.yaml) for the requirement details.
