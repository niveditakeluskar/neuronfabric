# NeuroGuard architecture overview

Derived from TDS v2.0.0-candidate (NG-TDS-000). This is a navigational summary. Where it differs from the TDS or an approved ADR, those govern. Status: **DRAFT**. Nothing here is lab-verified.

## Planes and trust boundaries

```
                         ┌───────────────────────── Administration plane ─────────────────────────┐
  Operator browser ──OIDC──► API gateway (brain/services/api) ──► audit          PAM gateway (gateway/pam)
                         └──────────────────────────────────────┬────────────────────────── SSH/RDP ─┘
                                                                │                         to targets
                         ┌──────────────────────────── Control plane (Brain) ─────────────────────────┐
                         │ enrollment · inventory · policy (signs) · detection · response · audit      │
                         │ PostgreSQL (control, RLS) · ClickHouse (telemetry) · object store (evidence)│
                         │ durable queue (ADR-011)                                                     │
                         └──────▲────────────────────────▲──────────────────────────────▲─────────────┘
                     mTLS gRPC  │ telemetry (ingest)     │ signed desired state         │ SNMPv3/syslog-TLS/
                   outbound-only│ split from control     │ (policy, OTA)                │ IPFIX/NETCONF
  ┌──────────────── Data plane ─┴────────────────────────┴───────────┐        ┌──────────┴──────────┐
  │ Appliance (Yocto, TPM, A/B)  Linux host agent   Windows sensor     │        │ Network devices     │
  │ eBPF → loader → Rust agent   eBPF → Rust agent  ETW svc + WFP      │        │ (no kernel hooks)   │
  │                              K8s DaemonSet + controller/admission  │        └─────────────────────┘
  └───────────────────────────────────────────────────────────────────┘
```

Trust boundaries, where every crossing is authenticated and audited:

1. **Kernel ↔ user space.** BPF programs emit fixed-format events (CTR-001). The privileged loader is separate from the unprivileged agent (NG-RST-001).
2. **Sensor ↔ Brain.** mTLS with per-device identity. The Brain derives tenant identity from the certificate and never from payload fields (NG-BRN-002, FND-007). Sensors verify policy signatures before enforcing (NG-POL-003).
3. **Tenant ↔ tenant.** Isolation is enforced at every API, queue, database (forced RLS) and artifact (NG-SEC-013).
4. **Operator ↔ Brain.** OIDC with MFA at the IdP. Per-tenant roles are viewer, analyst, responder, admin and platform operator (NG-SEC-007).
5. **AI ↔ enforcement.** Analytics only score. Enforcement happens only through signed, approved, deterministic policy (NG-SYS-007).

## Components

| Component | Path | Language/tech (status) | TDS |
|---|---|---|---|
| Appliance OS | appliance/meta-neuroguard | Yocto + kas, systemd, RAUC/SWUpdate (ADR-012 open) | B2 |
| Hardware | hardware/ | OEM/ODM x86_64, TPM 2.0 (ADR-001 REVIEW, ADR-015 open) | B1 |
| eBPF probes | sensors/linux/ebpf | C11 + libbpf CO-RE (ADR-006 REVIEW) | C1 |
| Loader + agent | sensors/linux/{loader,agent} | Rust stable, Tokio, tonic/prost, rustls | C2 |
| Windows sensor | sensors/windows/* | ETW, WFP, C++20 driver, service in Rust or C++ (ADR-019 open) | C3 |
| Kubernetes | integrations/kubernetes/* | DaemonSet, controller, admission webhook, Helm | C4 |
| Network | integrations/network/* | Go collectors and adapters | C5 |
| PAM gateway | gateway/pam | OpenSSH proxy, RDP component (ADR-014 open) | C6 |
| Brain services | brain/services/* | Go, gRPC internal, REST/OpenAPI external (ADR-007 REVIEW) | D1 |
| Data | brain/db/* | PostgreSQL, ClickHouse, S3-compatible object store | D3 |
| Analytics | brain/analytics/* | Python (3.12 candidate), statistics first, ML later | D4 |
| Web console | brain/web | undecided (ADR-024) | A1 |

## Cross-component contracts

| ID | Producer → consumer | Canonical source (planned) | Owner | Status |
|---|---|---|---|---|
| CTR-001 | eBPF → Rust agent | `sensors/linux/ebpf` C header + Rust layout tests | Kernel Lead | Blocked by FND-006 |
| CTR-002 | Agent → Brain ingest | `contracts/proto/neuroguard/v1/events.proto` | Platform Lead | Not drafted (FND-007, FND-008) |
| CTR-003 | Brain → agent policy | `contracts/proto/neuroguard/v1/policy.proto` | Security Lead | Not drafted |
| CTR-004 | Enrollment → identity registry | `enrollment.proto` + SQL migrations | PKI Lead | Not drafted |
| CTR-005 | K8s watcher → enrichment | Kubernetes API versioned mapping | K8s Lead | Not drafted |
| CTR-006 | Windows → normalized event | Windows mapping test vectors | Windows Lead | Not drafted |
| CTR-007 | Network adapters → asset/event | Adapter interface + fixture set | Network Lead | Not drafted |
| CTR-008 | Detection → response | `finding.proto` + `response.proto` | Detection Lead | Not drafted |

Dependent production work starts only after the contract it consumes is `APPROVED` (CONTRIBUTING.md §4).

## Safety invariants

These invariants come from the TDS and apply to every component:

- No silent enforcement of an unsupported policy. The policy is rejected with a capability reason (NG-POL-002).
- No permanent lockout. Critical and recovery allowlists cannot be overridden remotely. Lease rollback, out-of-band recovery and break-glass are available (NG-POL-004, NG-POL-006).
- No unsigned fallback for policy, firmware or BPF bundles (NG-SEC-001, NG-OS-003, NG-RST-002).
- No acknowledgement of unpersisted telemetry (NG-BRN-001). The kernel never blocks waiting for the Brain (NG-LNX-004).
- A degraded collector is reported as degraded, never claimed as active (NG-LNX-006, NG-SYS-006).

## Repository layout

The layout is based on TDS §D1.1 (ADR-030, in REVIEW). Changes from §D1.1:

| TDS §D1.1 path | Repository path | Reason |
|---|---|---|
| `docs/adr/` | `governance/decisions/` | Decisions are governance records with a machine-readable register |
| `docs/requirements/` | `governance/requirements_registry.yaml` | One machine-readable registry |
| `docs/evidence/` | `governance/evidence/` | Evidence sits next to the traceability it supports |
| `docs/runbooks/` | `operations/runbooks/` | Operational ownership |
| *(not in §D1.1)* | `hardware/` | §F6 references `hardware/qualification` |
| *(not in §D1.1)* | `brain/web/` | Operator UI is in §A1 but has no path |
| *(not in §D1.1)* | `contracts/openapi/`, `contracts/jsonschema/` | Public REST API (§D2) and JSON manifests (§B1, §B2, §E2) |
| *(not in §D1.1)* | `tests/compatibility/`, `tests/environments/` | Compatibility matrices and test environments (Prompt 00 scope) |
| *(not in §D1.1)* | `security/`, `release/`, `operations/{pilots,manufacturing}/`, `tools/` | Security assurance, release engineering, pilots, manufacturing (§E2–§E4) |
| `docs/…` | `docs/NN-topic/` | Numbered topic folders, created only when they have content |

## Open architecture issues

These findings affect the architecture: FND-001 (product scope), FND-006 (kernel ABI), FND-007 (tenancy in events), FND-008 (typed payloads), FND-009 (UI stack) and FND-010 (platform matrix). See [findings_register.yaml](../../governance/findings_register.yaml).
