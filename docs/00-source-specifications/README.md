# Source specifications

[specification_manifest.yaml](specification_manifest.yaml) is the inventory of source documents. For each document it records the SHA-256, version, classification, role (governing / superseded / related-context) and which repository artifacts were derived from it.

## Storage policy (ADR-031, in REVIEW)

- **The originals are not committed.** TDS v2 is *Internal / Controlled* and Master Plan v6 is *CONFIDENTIAL*. The visibility of the Git remote has not been verified (FND-013). `.gitignore` blocks `*.docx` and `docs/00-source-specifications/originals/`.
- The originals were left **unchanged** at their registration location. Text extraction ran on copies in a temporary scratch directory, and the output was not committed.
- To check that a local copy is the registered version, run `python3 tools/governance/validate_governance.py --spec-root <dir>`.

## Governing document

**SPEC-001: NeuroGuard TDS v2.0.0-candidate** (NG-TDS-000). Its own limitation statement (§F9) says it is the design authority for Stage 0 and module planning. It is not a substitute for board schematics, a pinned BSP, a tested Windows driver, compilable `.proto` files, full SQL migrations, performance measurements or an independent security assessment.

The `.docx` is canonical. The PDF is a rendering of it. The section structure and spot-checked content match. A full automated text diff was **not** run because no PDF text-extraction tool is installed.

## How statements were classified

When the registry was derived, each TDS statement was treated as one of the following:

| TDS wording | Treated as |
|---|---|
| "Confirmed strategy/scope" | Decision in `REVIEW` (no recorded approval, FND-003) |
| "Proposed", "candidate", "ADR pending", "X or Y" | Open decision in `DRAFT` |
| Code blocks C1.1, D2.1, D3.1, E2.1 | Illustrative only (TDS §F8-117) |
| F3 numeric targets | Provisional targets, not verified results |
| Everything else in LLD / failure handling / verification | `DRAFT` requirements with acceptance criteria |

Conflicts and gaps are in [governance/findings_register.yaml](../../governance/findings_register.yaml).
