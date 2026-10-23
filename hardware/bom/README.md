# hardware/bom/ — OEM/ODM bill of materials

Frozen hardware BOM (HW-BOM-001) — OEM SKU, firmware version, NIC PCI IDs, storage model, TPM part — and the two-vendor qualification record.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §B1, §F7 Commercial OEM BOM |
| Owner (role) | Hardware Lead |
| Claude agent | `hardware-integration-engineer` |
| Requirements | NG-HW-002, NG-HW-003, NG-HW-004 |
| Contracts | Manufacturing manifest JSON (to be defined in contracts/jsonschema/) |
| Gate | G-B1 |

- Exact parts are pending ADR-015. Do not record a part as qualified without a signed qualification report.

See [governance/requirements_registry.yaml](../../governance/requirements_registry.yaml) for the requirement details.
