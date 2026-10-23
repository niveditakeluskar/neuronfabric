# brain/services/ingest/ — Telemetry ingest service

mTLS gRPC telemetry ingestion — authenticates the device cert, derives tenancy server-side, validates schema/size/quotas, writes to the durable queue before ACK.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §D1#60–61 |
| Owner (role) | Platform Lead |
| Claude agent | `central-brain-engineer` |
| Requirements | NG-BRN-001, NG-BRN-002, NG-BRN-003, NG-BRN-008 |
| Contracts | CTR-002 events.proto (consumer) |
| Gate | G-D1 (NG-BRN-001 program gate G4) |

- Never acknowledge unpersisted events. Queue technology pending ADR-011.

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
