# tools/

Repository tooling. Every script here is **read-only and non-destructive**: no installs, no `sudo`, no network calls.

| Script | Purpose | Requirement |
|---|---|---|
| [bootstrap/check_prereqs.sh](bootstrap/check_prereqs.sh) | Environment preflight. Reports tool versions, kernel BTF/BPF config on Linux and per-component GO/NO-GO. `--json FILE` writes a machine-readable report without hostname or username. | NG-TST-009 |
| [governance/validate_governance.py](governance/validate_governance.py) | Parses all YAML/JSON and checks ID uniqueness, cross-references, lifecycle/evidence rules, traceability coverage, backlog cycles and simple secret patterns. `--spec-root DIR` verifies source-spec hashes. | NG-TST-001, NG-REL-006 |

The validator uses PyYAML when it is installed. Otherwise it falls back to the Ruby YAML parser that ships with macOS. Exit codes: 0 pass, 1 errors, 2 cannot run.
