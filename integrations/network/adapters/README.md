# integrations/network/adapters/ — Network device vendor adapters

Per-vendor implementations of the adapter contract (discover, read_config, read_interfaces, read_flows, validate_change, apply_change, rollback). Writes only for explicitly supported vendors and approved templates.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §C5#48–52 |
| Owner (role) | Network Lead |
| Claude agent | `network-infrastructure-engineer` |
| Requirements | NG-NET-001, NG-NET-003, NG-NET-006, NG-NET-007 |
| Contracts | CTR-007 adapter interface + fixture set; ChangePlan |
| Gate | G-C5 (NG-NET-001 program gate G8) |

- Config changes need two-person approval, a rollback timer and out-of-band recovery.

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
