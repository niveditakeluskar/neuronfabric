# sensors/linux/ebpf/ — Linux eBPF programs (C/libbpf CO-RE)

Minimal kernel probes — process lifecycle tracepoints, cgroup/connect egress hooks, BPF LSM file/exec hooks — that emit bounded binary events into the ring buffer.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §C1, §C1.1, §C1.2 |
| Owner (role) | Kernel Lead |
| Claude agent | `kernel-ebpf-engineer` |
| Requirements | NG-LNX-001 … NG-LNX-010 |
| Contracts | CTR-001 kernel event header (C header + generated Rust layout tests) |
| Gate | G-C1 |

- CTR-001 is blocked by FND-006 (field-name mismatch). Do not write production probes until the header is APPROVED.
- No unbounded loops, path walks or remote networking in kernel code.

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
