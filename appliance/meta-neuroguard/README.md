# appliance/meta-neuroguard/ — Yocto layer for the NeuroGuard appliance OS

The meta-neuroguard Yocto layer: machine and distro config, kernel config fragments, image recipes, agent/policy recipes, hardened systemd units, A/B OTA and recovery. Planned layout is in TDS §B2.1: conf/{layer.conf,distro/neuroguard.conf,machine/ng-oem-x86.conf}, recipes-core/, recipes-kernel/, recipes-security/.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §B2, §B2.1 |
| Owner (role) | OS Lead |
| Claude agent | `yocto-os-engineer` |
| Requirements | NG-OS-001 … NG-OS-009 |
| Contracts | Boot manifest, OTA desired state (NG-OS-009) |
| Gate | G-B2 |

- Blocked on ADR-009 (kernel/BSP) and ADR-012 (RAUC vs SWUpdate).
- Builds need a Linux x86_64 reference host with kas/BitBake (see docs/16-development-environments/environment_matrix.md). Build directories are git-ignored.

See [governance/requirements_registry.yaml](../../governance/requirements_registry.yaml) for the requirement details.
