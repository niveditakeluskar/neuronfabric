# brain/db/postgres/ — PostgreSQL schemas and migrations

Control-state tables (tenants, sites, sensors, certificates, policies, approvals, audit metadata) with forced row-level security and forward-only migrations.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §D3, §D3.1 |
| Owner (role) | Platform Lead |
| Claude agent | `central-brain-engineer` |
| Requirements | NG-DAT-001 … NG-DAT-004, NG-DAT-007, NG-DAT-008 |
| Contracts | SQL migrations (part of CTR-004) |
| Gate | G-D3 |

- Migration tool pending ADR-020. Each service owns its schema.

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
