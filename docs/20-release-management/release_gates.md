# Release gates

Source: TDS v2 §F4 (program gates), §A1–§E4 (section gates), §F5 (G0 checklist). Gate approvals are recorded only in [governance/approvals/approval_register.yaml](../../governance/approvals/approval_register.yaml). **No gate has been passed.**

## Program gates (TDS §F4)

| Gate | Month | Work packages | Exit evidence | Status |
|---|---|---|---|---|
| G0 | 1 | Hardware SKU selection; OS/BSP feasibility; contract freeze; threat model; team environments | Baseline sign-off (G0 checklist below) | NOT STARTED |
| G1 | 2 | Yocto boot image; Linux eBPF minimal agent; Brain identity/ingest skeleton | Kernel attach + signed boot POC | NOT STARTED |
| G2 | 3 | Linux process/network telemetry; Rust spool; API v1; Windows ETW prototype | Contract and event fixtures | NOT STARTED |
| G3 | 4 | Linux file/privilege; Windows WFP prototype; Brain tenant isolation; K8s watcher | Cross-platform telemetry | NOT STARTED |
| G4 | 5 | Policy compiler, signed distribution, monitor-only canary; network collectors | Policy integrity | NOT STARTED |
| G5 | 6 | Bounded Linux prevention; Windows WFP safety; PAM SSH; Brain detection rules | Prevention lab review | NOT STARTED |
| G6 | 7 | Behavior features; K8s admission; network adapters; OTA A/B | Integration end-to-end | NOT STARTED |
| G7 | 8 | Hardware stress, signed Windows packaging, Brain on-prem HA; pilot readiness | Alpha validation | NOT STARTED |
| G8 | 9 | Internal and design-partner pilots; false-positive tuning; security review | Controlled pilot | NOT STARTED |
| G9 | 10 | Independent penetration testing; DR, rollback and soak; remediation | Security exit | NOT STARTED |
| G10 | 11 | Manufacturing pilot batch; support runbooks; release candidate | RC evidence | NOT STARTED |
| G11 | 12 | Staged commercial GA, measured SLA baseline and support readiness | GA sign-off | NOT STARTED |

Before G0, parallel teams may build isolated prototypes (`spike/*` branches). Production implementation against shared contracts requires G0 and approval from the contract owner.

## G0 acceptance checklist (TDS §F5)

| Source ID | Registry ID | Evidence to attach | Pass condition | Status |
|---|---|---|---|---|
| ENV-001 | NG-TST-009 | Pinned OS/toolchain manifests and preflight logs | All reference build hosts reproducible | NOT STARTED: no reference host provisioned (FND-011) |
| HW-001 | NG-HW-002 | OEM SKU/BSP/TPM/NIC inventory | Lead approval and procurement feasibility | NOT STARTED |
| OS-001 | NG-OS-003 | Yocto minimal signed boot POC | Boot verified on physical hardware | NOT STARTED; scheduling conflict FND-004 |
| KRN-001 | NG-LNX-006 | eBPF probe load/attach on selected kernel | Verifier and event fixture pass | NOT STARTED; scheduling conflict FND-004, ABI FND-006 |
| WIN-001 | NG-WIN-005 | ETW/WFP and signing feasibility report | Supported Windows build matrix | NOT STARTED; needs ADR-028 |
| API-001 | NG-API-001 | Protobuf schemas and generated SDKs | buf breaking/compile tests pass | NOT STARTED |
| SEC-001 | NG-SEC-009 | Threat model and prevention recovery plan | Security Lead sign-off | NOT STARTED; needs ADR-029 |
| OPS-001 | NG-OPS-008 | Pilot telemetry volumes and resource model | Sizing assumptions documented | NOT STARTED |
| GOV-001 | NG-REL-007 | Requirement IDs, owners, ADR and change workflow | All critical decisions assigned | IN PROGRESS: Prompt 00 created the registry, decision register and workflow. Owners are still unassigned (FND-014) and approval is pending |

## Section gates

| Gate | Pass condition (TDS) | Approver |
|---|---|---|
| G-A1 | Architecture/security owners sign topology and trust-boundary map | Architecture + Security leads |
| G-B1 | OEM SKU and firmware frozen with signed hardware qualification report | Hardware Lead |
| G-B2 | Signed OS boot and rollback proven on OEM hardware | OS Lead |
| G-C1 | Reference kernel load/attach and event ABI fixtures pass | Kernel Lead |
| G-C2 | Rust service soak and failover pass with measurable resource limits | Kernel Lead |
| G-C3 | Signed driver path, OS matrix and recovery validated | Windows Lead |
| G-C4 | Cluster lifecycle and API outage tests pass | K8s Lead |
| G-C5 | Vendor adapter certification and recovery plan approved | Network Lead |
| G-C6 | Privileged session threat model and audit retention approved | Security Lead |
| G-D1 | Contract compatibility and tenant isolation tests pass | Platform Lead |
| G-D2 | API council signs v1 contracts and test fixtures | API council |
| G-D3 | DBA and security lead approve migrations and recovery targets | DBA + Security Lead |
| G-D4 | Detection quality targets defined and measured on representative pilots | Detection Lead |
| G-D5 | Independent prevention safety review and canary evidence | Security Lead + independent reviewer |
| G-E1 | Security architecture review and certificate lifecycle drill | Security + PKI leads |
| G-E2 | Clean environment reproducibility and signing pipeline pass | QA Lead |
| G-E3 | QA and security leads approve evidence bundle for release candidate | QA + Security leads |
| G-E4 | Manufacturing readiness and customer operations runbooks approved | Hardware + Platform leads |

### Proposed section → program gate mapping (PROPOSAL, not approved; FND-005)

The TDS does not map section gates to program gates. The proposal below is inferred from the §F4 work packages and needs approval (WI-017):

| Program gate | Section gates expected to be met |
|---|---|
| G0 | G-A1 |
| G1 | G-C1 (reference kernel), G-B2 (POC level) |
| G2 | G-D2 |
| G3 | G-D1 (tenant isolation part) |
| G4 | G-E1, G-D3 |
| G5 | G-C2 |
| G6 | G-C4 |
| G7 | G-B1, G-B2 (full), G-C3 |
| G8 | G-D4, G-C5, G-C6 |
| G9 | G-D5, G-E2 |
| G10 | G-E3 |
| G11 | G-E4 |

This proposal moves NG-HW-001 from G1 (as stated in TDS §F6) to G7, because the 72-hour thermal and power-cut qualification falls under Month 8 "Hardware stress". Approval of WI-017 decides this.

## Release-blocking conditions (TDS §E3)

Any kernel panic, Windows bugcheck, irreversible lockout, tenant leakage, OPEN finding of severity `high`, or requirement claimed VERIFIED without an evidence record blocks every gate.
