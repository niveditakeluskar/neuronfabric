# release/ — Release engineering

CI pipeline definitions (lint→unit→build→contract→integration→security→performance smoke→sign), SBOM/provenance generation, signing-service integration and build manifests. GitHub workflow files live in .github/workflows/ and call into this directory.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §E2 |
| Owner (role) | QA Lead |
| Claude agent | `devsecops-release-engineer` |
| Requirements | NG-REL-001 … NG-REL-006, NG-SEC-010, NG-SEC-011, NG-TST-003, NG-TST-004 |
| Contracts | Build manifest (contracts/jsonschema/) |
| Gate | G-E2 |

- Added to the TDS §D1.1 layout (ADR-030). CI platform pending ADR-023. Signing keys never in CI env vars.

See [governance/requirements_registry.yaml](../governance/requirements_registry.yaml) for the requirement details.
