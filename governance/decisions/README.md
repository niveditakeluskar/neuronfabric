# Architecture decisions

[decision_register.yaml](decision_register.yaml) is the single index of every decision and its state. A decision gets its own markdown record (`ADR-NNN-short-title.md` in this directory) when it enters `REVIEW` with a written rationale. The register's `record:` field then points to that file.

The rules:

- IDs are never reused. ADR-001…008 keep their TDS v2 IDs.
- Use a draft ADR for any change to security behavior, ABI, data semantics or recovery behavior (TDS §F8-120).
- `APPROVED` requires an entry in [../approvals/approval_register.yaml](../approvals/approval_register.yaml).
- A superseded ADR keeps its file. Its status changes, and the new ADR's register entry gets a `supersedes:` field.

## ADR template

```markdown
# ADR-NNN: <title>

- Status: DRAFT | REVIEW | APPROVED | SUPERSEDED
- Owner: <role / person>
- Freeze by: <gate>
- Requirements affected: <NG-… IDs>
- Contracts affected: <CTR-… + versions>

## Context
<forces, constraints, source references>

## Options considered
| Option | Pros | Cons | Evidence |

## Decision
<the choice and its scope>

## Consequences
<follow-up work, risks, what becomes blocked/unblocked>

## Validation
<how we will know the decision holds; evidence links>
```
