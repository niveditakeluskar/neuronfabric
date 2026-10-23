# neuronfabric — NeuroGuard monorepo

NeuroGuard is a commercial security appliance and centralized behavioral security platform: a Yocto-based x86_64 appliance, Linux eBPF and Windows sensors, Kubernetes and network-device integrations, a privileged access gateway, and a multi-tenant "Central Brain" (SaaS and on-prem) that provides detection and **bounded** active prevention.

> **Stage: Project initialization (Prompt 00).** No product features are implemented yet. Nothing in this repository is lab-verified, hardware-qualified or independently security-assessed. All requirements and decisions are `DRAFT`/`REVIEW` until recorded approvals exist in [governance/approvals/](governance/approvals/).

## Governing specification

The human-readable design authority is **NeuroGuard TDS v2.0.0-candidate (NG-TDS-000, 23 Oct 2026)**. The binary originals are kept outside Git (see [docs/00-source-specifications/](docs/00-source-specifications/)). They are identified by SHA-256 in [specification_manifest.yaml](docs/00-source-specifications/specification_manifest.yaml).

Source-of-truth hierarchy (highest first). A conflict between levels blocks dependent work until it is resolved by an approved decision:

1. Approved product requirements and architecture decisions — [governance/requirements_registry.yaml](governance/requirements_registry.yaml), [governance/decisions/](governance/decisions/)
2. Approved, versioned machine-readable contracts — [contracts/](contracts/)
3. Approved component technical specifications — `docs/`
4. Implementation source code
5. Automated test evidence — [governance/evidence/](governance/evidence/)
6. Generated documentation and reports

## Repository map

| Path | Scope | TDS ref |
|---|---|---|
| [governance/](governance/) | Requirements, traceability, decisions (ADRs), findings, risks, approvals, evidence, backlog, workflow | F5–F9 |
| [docs/](docs/) | Source specification inventory, architecture, environments, release gates | all |
| [contracts/](contracts/) | Protobuf, OpenAPI, JSON Schema — the executable interface contracts | D2, F2 |
| [hardware/](hardware/) | OEM/ODM BOM and hardware qualification | B1 |
| [appliance/meta-neuroguard/](appliance/meta-neuroguard/) | Yocto layer, boot chain, OTA, recovery | B2 |
| [sensors/linux/](sensors/linux/) | eBPF programs, privileged loader, Rust agent | C1, C2 |
| [sensors/windows/](sensors/windows/) | Windows service, driver, installer | C3 |
| [integrations/kubernetes/](integrations/kubernetes/) | Helm chart and controller/admission webhook | C4 |
| [integrations/network/](integrations/network/) | Vendor adapters and telemetry collectors | C5 |
| [gateway/pam/](gateway/pam/) | Privileged access gateway and session audit | C6 |
| [brain/](brain/) | Central Brain services, databases, analytics, web console | D1–D5 |
| [deploy/](deploy/) | Helm, Terraform, local dev compose | D1, E4 |
| [tests/](tests/) | Contract, integration, e2e, security, performance, compatibility tests and test environments | E3 |
| [security/](security/) | Threat models and security assurance | E1, E3 |
| [release/](release/) | CI/CD pipelines, signing, SBOM, provenance | E2 |
| [operations/](operations/) | Runbooks, customer pilots, manufacturing | E4 |
| [tools/](tools/) | Non-destructive bootstrap and governance validation scripts | E2 |

The layout follows TDS §D1.1, plus additions recorded in [ADR-030](governance/decisions/decision_register.yaml) and explained in [architecture_overview.md](docs/02-system-architecture/architecture_overview.md#repository-layout).

## Getting started

```sh
tools/bootstrap/check_prereqs.sh                 # reports missing tools; installs nothing
tools/bootstrap/check_prereqs.sh --json out.json # machine-readable environment report
python3 tools/governance/validate_governance.py  # parses all YAML/JSON, checks IDs and links
```

Kernel, Yocto and Windows-driver work requires the reference hosts in [environment_matrix.md](docs/16-development-environments/environment_matrix.md). Other hosts report NO-GO for those components (TDS §E2).

See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and [SECURITY.md](SECURITY.md) for vulnerability reporting and secrets handling.
