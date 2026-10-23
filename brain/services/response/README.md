# brain/services/response/ — Response orchestrator

Approval-gated, time-boxed response actions with safety checks, rollback handles and idempotency keys.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §D1#65, §D5#91 |
| Owner (role) | Security Lead |
| Claude agent | `central-brain-engineer` |
| Requirements | NG-BRN-009, NG-POL-007 |
| Contracts | CTR-008 response.proto |
| Gate | G-D5 |

- No AI/ML output may trigger a response without the deterministic policy path (NG-SYS-007).

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
