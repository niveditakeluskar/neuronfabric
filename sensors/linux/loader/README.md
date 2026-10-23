# sensors/linux/loader/ — Privileged eBPF loader

Small privileged process that verifies signed BPF program bundles, attaches approved hooks one by one, pins and sizes maps, records the capability matrix, then drops capabilities.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §C2#27–28, §C1#24–25 |
| Owner (role) | Kernel Lead |
| Claude agent | `kernel-ebpf-engineer` |
| Requirements | NG-RST-001, NG-RST-002, NG-LNX-005, NG-LNX-006 |
| Contracts | Local IPC (versioned): status, attach manifest, policy stage/activate/rollback |
| Gate | G-C2 |

- The Brain must never be able to request loading of arbitrary BPF objects.

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
