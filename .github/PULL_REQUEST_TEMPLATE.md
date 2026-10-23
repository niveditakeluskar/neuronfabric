## Summary

<!-- What does this change do and why? Keep it short. -->

## Traceability

- Requirement IDs: <!-- e.g. NG-LNX-001, NG-API-002 -->
- Backlog item: <!-- e.g. WI-013 -->
- ADRs touched/added: <!-- e.g. ADR-011 (REVIEW) -->
- Contracts touched (ID + version): <!-- e.g. CTR-002 events.proto v1.0.0-draft.2 -->
- Findings resolved/raised: <!-- e.g. resolves FND-006 -->

## Change classification

- [ ] Changes security behavior, ABI, data semantics or recovery behavior. An ADR is linked and approved (TDS §F8-120).
- [ ] Changes an interface contract. A contract/test impact review is included and `buf breaking` (or equivalent) was run.
- [ ] Touches a security-sensitive path. Security Lead review is requested.
- [ ] Only docs, governance or tooling.

## Evidence

<!-- Paste real command output or link evidence records. Do not summarize results you did not observe. -->

| Check | Command | Result |
|---|---|---|
| Governance validation | `python3 tools/governance/validate_governance.py` | |
| Lint | | |
| Unit tests | | |
| Build | | |

**Not run (and why):**

## Checklist

- [ ] `governance/traceability.yaml` updated for affected requirements
- [ ] No requirement or work item moved to `VERIFIED` without an evidence record and a named reviewer
- [ ] No secrets, keys, customer data or original specification documents committed
- [ ] No security check, signature verification or test was skipped or weakened to make CI pass
- [ ] Active prevention is not enabled outside lab/canary without recorded sign-off
