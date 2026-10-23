# contracts/proto/neuroguard/v1/ — Protobuf contracts v1

The single source for wire contracts: events.proto (CTR-002), policy.proto (CTR-003), enrollment.proto (CTR-004), health.proto, finding.proto and response.proto (CTR-008). Checked with buf lint and buf breaking.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §D2, §D2.1, §F2 |
| Owner (role) | Platform Lead (CTR-002), Security Lead (CTR-003), PKI Lead (CTR-004), Detection Lead (CTR-008) |
| Claude agent | `system-architect` |
| Requirements | NG-API-001 … NG-API-008 |
| Contracts | CTR-002, CTR-003, CTR-004, CTR-008 |
| Gate | G-D2 (NG-API-001 program gate G2) |

- The TDS §D2.1 skeleton is illustrative. FND-007 and FND-008 must be resolved before freeze.
- Never reuse field numbers; reserve removed ones.

See [governance/requirements_registry.yaml](../../../../governance/requirements_registry.yaml) for the requirement details.
