# sensors/linux/agent/ — Rust sensor runtime (reduced privilege)

Ring-buffer reader, ABI decoder, process-cache enrichment, batching/backpressure, encrypted durable spool, local policy and mTLS gRPC connection to the Brain.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §C2 |
| Owner (role) | Kernel Lead (interim; see FND-014) |
| Claude agent | `rust-systems-engineer` |
| Requirements | NG-RST-001 … NG-RST-010 |
| Contracts | CTR-001 (consumer), CTR-002 events.proto (producer), CTR-003 policy.proto (consumer) |
| Gate | G-C2 |

- The Rust toolchain is pinned via rust-toolchain.toml when the crate is created.

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
