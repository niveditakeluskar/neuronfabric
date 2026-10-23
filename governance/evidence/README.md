# Evidence

Test and verification evidence lives here, one YAML record per test execution: `governance/evidence/<requirement-id>/<test-id>-<YYYYMMDD>-<short-commit>.yaml`. Large artifacts (logs, JUnit XML, verifier logs, metrics) are stored next to the record or in the CI artifact store, and the record references them by digest.

There is no evidence yet. No test has been run against product code.

## Evidence record (TDS §E3 contract)

```yaml
schema_version: 1
requirement_id: NG-LNX-001
test_id: T-LNX-EXEC-001
commit: <full git SHA>
environment_id: <reference host / CI runner ID from docs/16-development-environments/environment_matrix.md>
artifact_digest: sha256:<digest of the artifact under test>
command: <exact command run>
observed_metric: <measured values, with units>
result: PASS | FAIL | BLOCKED | ERROR      # NOT_RUN is implied by absence of a record
executed_at: "YYYY-MM-DDThh:mm:ssZ"
executed_by: <person or CI job URL>
reviewer: <named person, not the executor>  # required before VERIFIED
attachments: [<relative paths or URLs with sha256>]
```

## Defect record (TDS §E3 contract)

```yaml
id: DEF-NNN
severity: S1 | S2 | S3 | S4        # S1 includes all release-blocking classes (NG-TST-007)
repro: <steps>
affected_versions: [<versions/commits>]
mitigation: <workaround or fix>
owner: <role/person>
gate: <program gate this blocks>
```

## Rules

- Never write a record for a test that was not actually executed.
- Results come from tool output, not from reading source.
- A record is immutable once reviewed. A re-run creates a new record.
