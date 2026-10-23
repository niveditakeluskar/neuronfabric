# brain/services/policy/ — Policy service

Policy authoring lifecycle, compilation, signing of immutable desired-state artifacts, canary rollout and acknowledgement tracking.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §D1#63, §D5 |
| Owner (role) | Security Lead |
| Claude agent | `central-brain-engineer` |
| Requirements | NG-SEC-001, NG-POL-001 … NG-POL-009 |
| Contracts | CTR-003 policy.proto (producer) |
| Gate | G-D5 (NG-SEC-001 program gate G4) |

- An outage must never produce unsigned fallback commands.

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
