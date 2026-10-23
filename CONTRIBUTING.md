# Contributing to NeuroGuard

This document defines how work moves from a requirement to a release. The lifecycle states, transitions and approval authorities that can be checked by tools are in [governance/workflow.yaml](governance/workflow.yaml). This file explains them for people.

## 1. Lifecycle

```
DRAFT → REVIEW → APPROVED → IMPLEMENTING → IMPLEMENTED → TESTED → VERIFIED → RELEASED
```

| State | Meaning | Evidence required to enter | Who may move it there |
|---|---|---|---|
| DRAFT | Captured; may be incomplete | Source reference | Anyone |
| REVIEW | Ready for decision | Owner, acceptance criteria, verification method, dependencies | Item owner |
| APPROVED | Baseline; implementation may start | Approval record in `governance/approvals/` | Owner's approving lead (security-impacting: + Security Lead) |
| IMPLEMENTING | Work in progress | Linked branch/PR, all dependencies APPROVED or later | Implementer |
| IMPLEMENTED | Code merged | Merged PR; traceability updated | CODEOWNER review |
| TESTED | Tests run in the defined environment | Evidence record with `result: PASS` and command output | QA Lead or delegate |
| VERIFIED | Acceptance criteria met and reviewed | Evidence reviewed by a named reviewer other than the implementer | QA Lead + item owner |
| RELEASED | Shipped in a gated release | Release gate (G0–G11) approval | Release gate approvers |

Backward transitions are allowed in these cases: any state → `DRAFT` when the requirement changes, and `TESTED`/`VERIFIED` → `IMPLEMENTING` on regression. Every backward transition needs a recorded reason.

## 2. Branches

- `main` is protected and stays releasable. No direct pushes.
- Branch names: `<type>/<REQ-or-WI-id>-<short-slug>`. Types: `feat`, `fix`, `contract`, `adr`, `docs`, `test`, `chore`, `spike`.
  Examples: `contract/NG-API-002-event-envelope`, `adr/ADR-011-brain-queue`, `spike/WI-013-ebpf-attach-poc`.
- `spike/*` branches are throwaway prototypes. They never merge to `main` without being re-done against approved contracts (TDS §F4: isolated prototypes are allowed before G0).
- Release branches: `release/<version>`. They are protected and need two-person signing approval (NG-REL-002).

## 3. Pull requests

Every PR uses [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) and must:

1. List the requirement IDs and the ADRs/contracts it touches, with versions.
2. Include an ADR when it changes a decision, and a contract/test impact review when it changes an interface. This is the TDS change rule.
3. Update `governance/traceability.yaml` for the requirements it implements or tests.
4. Attach real command output for lint/build/tests that were run. List what was **not** run.
5. Pass `tools/governance/validate_governance.py`.
6. Have approval from the CODEOWNERS of every touched path. Security-sensitive paths (`sensors/*`, `brain/services/policy`, `brain/services/response`, `gateway/`, `contracts/`, `release/`, `security/`) also need Security Lead review.

Merge method: squash, with the requirement IDs in the commit title.

## 4. Contracts before dependents

A component that consumes a contract (CTR-001…CTR-008, see [architecture_overview.md](docs/02-system-architecture/architecture_overview.md#cross-component-contracts)) starts production implementation only after that contract is `APPROVED`. Before then, work happens only on `spike/*` branches.

## 5. Decisions (ADRs)

Decisions are tracked in [governance/decisions/decision_register.yaml](governance/decisions/decision_register.yaml). A decision gets a full ADR markdown file when it enters `REVIEW`; the template is in the decisions README. If a TDS statement and an ADR disagree, raise a finding in `governance/findings_register.yaml`.

## 6. Merge controls (target configuration)

The list below describes intent. **It has not been verified as configured on GitHub.** See FND-012 and backlog item WI-004.

- Protected `main` and `release/*`: required PR, ≥1 CODEOWNER approval (≥2 for security-sensitive paths), required status checks, linear history, no force-push, no deletion.
- Signed commits on release branches.
- Required checks, added as CI lands: governance validation, lint, unit, build, contract compatibility (`buf breaking`), secret scan, SBOM.
