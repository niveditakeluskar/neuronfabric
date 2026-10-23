# sensors/windows/driver/ — Windows kernel components (WFP callout; minifilter only if justified)

Scoped network enforcement through supported WFP APIs and, only if ETW coverage proves inadequate, a file-system minifilter.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §C3#37–40 |
| Owner (role) | Windows Lead |
| Claude agent | `windows-security-engineer` |
| Requirements | NG-WIN-002, NG-WIN-004, NG-WIN-005, NG-WIN-006 |
| Contracts | Brain policy → WFP rule translation (after capability validation) |
| Gate | G-C3 |

- Driver scope pending ADR-010. Requires a Windows WDK build host; never use undocumented hooking.
- A driver fault must never block boot or persist broad network denial.

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
