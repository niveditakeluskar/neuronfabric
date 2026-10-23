# brain/services/enrollment/ — Enrollment service

Device claim workflow, CSR handling, certificate issuance/rotation/revocation and the enrollment state machine.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §D1, §E1 |
| Owner (role) | PKI Lead |
| Claude agent | `central-brain-engineer` |
| Requirements | NG-SEC-004, NG-SEC-005, NG-SEC-006, NG-BRN-002 |
| Contracts | CTR-004 enrollment.proto + SQL migrations |
| Gate | G-E1 |

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
