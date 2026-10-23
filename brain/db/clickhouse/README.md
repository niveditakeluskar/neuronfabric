# brain/db/clickhouse/ — ClickHouse telemetry schema

High-volume event tables partitioned by date and ordered by tenant/site/time/event ID, with TTL and legal-hold-aware deletion.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §D3 |
| Owner (role) | Platform Lead |
| Claude agent | `central-brain-engineer` |
| Requirements | NG-DAT-005, NG-DAT-009, NG-DAT-010 |
| Contracts | Event table schema |
| Gate | G-D3 |

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
