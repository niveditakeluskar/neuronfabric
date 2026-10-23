# sensors/windows/service/ — Windows user-mode sensor service

ETW-based telemetry collection (process, image-load, network, security), normalization to the shared event schema, bounded spool and Brain connectivity.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §C3#35–36 |
| Owner (role) | Windows Lead |
| Claude agent | `windows-security-engineer` |
| Requirements | NG-WIN-001, NG-WIN-003, NG-WIN-007 |
| Contracts | CTR-006 Windows → normalized event mapping; CTR-002 events.proto |
| Gate | G-C3 |

- Language (Rust vs C++) pending ADR-019.

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
