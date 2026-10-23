# Development environment matrix

Source: TDS v2 §E2 (and the stack tables in §B2, §C1–§C6, §D1–§D4). Exact versions are pinned by lockfiles and toolchain files when each component is created (NG-REL-001). "Latest" is never acceptable in release manifests.

Run `tools/bootstrap/check_prereqs.sh --json <file>` to assess a host. The script is read-only.

## Reference environments by component

| Component | Reference host | Toolchain (TDS candidates) | Status of pin |
|---|---|---|---|
| Governance, docs | Any OS | git, Python 3 (+PyYAML or Ruby for YAML parsing) | n/a |
| Contracts | Any OS | buf, protoc; Rust tonic/prost and grpc-go generators | Versions pending |
| Linux eBPF | **Ubuntu 24.04 LTS x86_64** (VM acceptable), kernel with BTF | clang/llvm, bpftool, pahole, libbpf, make/CMake; QEMU/KVM kernel fixture matrix | Kernel pending ADR-009/ADR-028 |
| Rust agent/loader | Ubuntu 24.04 LTS x86_64 | rustup + `rust-toolchain.toml` (stable, pinned), cargo, clippy, rustfmt, cargo-nextest | Version pending |
| Yocto appliance | **Dedicated Ubuntu 24.04 x86_64 build host** with ample SSD/RAM | kas + BitBake, Yocto LTS (pending BSP) | Pending ADR-009 |
| Windows sensor/driver | **Windows** with Visual Studio Build Tools, Windows SDK + WDK, WinDbg, Hyper-V test VMs | C++20 (driver); Rust or C++ (service, ADR-019) | Pending ADR-010/019 |
| Kubernetes | Linux or macOS with Docker | kubectl, Helm, kind/k3s; multi-node managed K8s for staging | Versions pending ADR-028 |
| Network integrations | Linux | Go; virtual routers/switches, vendor simulators, physical switch lab | Pending |
| PAM gateway | Linux | Go/OpenSSH; RDP component pending ADR-014 | Pending |
| Brain services | Linux or macOS | Go 1.x (pinned), PostgreSQL, ClickHouse, queue (ADR-011), Docker Compose for dev only | Pending |
| Analytics | Linux or macOS | Python 3.12 candidate, Polars/Pandas, NumPy, scikit-learn, pytest; uv or pip-hash (ADR-027) | Pending |
| Web console | Any OS | Pending ADR-024 | Pending |
| CI | GitHub Actions or GitLab CI (ADR-023); isolated privileged runner pool for eBPF/driver tests | — | Pending |

macOS and Windows may be used as **editors**. Kernel builds run in a Linux VM (TDS §E2). An unsupported host must report NO-GO, never a guess.

## Current local workstation assessment (2026-10-23)

The machine-readable report is [reports/2026-10-23-macos-arm64.json](reports/2026-10-23-macos-arm64.json). It records no hostname or username.

| Fact | Value |
|---|---|
| OS / arch | macOS 27.0.1, Darwin 27.0.0, **arm64** |
| Reference Linux build host | **No** (FND-011) |
| Present | git 2.50.1, Python 3.9.6, Docker 29.8.2, Ruby 2.6.10, Apple clang 17.0.0, GNU Make 3.81, Node v26.10.0, npm 11.19.1, kubectl v1.36.1, textutil |
| Missing | rustup/rustc/cargo, llvm-config, llvm-strip, bpftool, pahole, cmake, qemu-system-x86_64, go, buf, protoc, kas, bitbake, helm, kind, gh, shellcheck, yamllint, uv, pandoc, pdftotext; Python module PyYAML |

| Component | Readiness on this host |
|---|---|
| Governance / docs | **GO** (YAML parsing uses the Ruby fallback) |
| Contracts | NO-GO (buf/protoc missing) |
| Linux eBPF | **NO-GO** (not Linux x86_64; no BTF; Apple clang is not a BPF toolchain substitute) |
| Rust agent | NO-GO (Rust missing; the target is Linux anyway, so build in a Linux VM) |
| Yocto | **NO-GO** (requires a Linux x86_64 build host) |
| Brain (Go) | NO-GO (Go missing) |
| Web console | GO for Node tooling; stack undecided |
| Kubernetes dev | NO-GO (helm/kind missing) |
| Windows driver | **NO-GO** (requires Windows + WDK) |

Python 3.9.6 is older than the TDS analytics candidate (3.12).

## Actions (approval required, nothing was installed)

1. Provision the Ubuntu 24.04 x86_64 reference build host or VM and run the preflight there to capture ENV-001 evidence (WI-005). On Apple-silicon Macs an x86_64 VM is emulated and slow, so a remote x86_64 host is preferable for Yocto.
2. Optional local user-space tools, installed only with approval: `rustup`, `go`, `buf`, `helm`, `kind`, `gh`, `shellcheck`, `yamllint`, `uv`.
3. Provision a Windows build host with the WDK for WI-014.
