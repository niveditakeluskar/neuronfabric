# CLAUDE.md — NeuroGuard engineering instructions

These rules apply to every Claude Code session and subagent in this repository. They implement TDS v2.0 §F8 (Claude Code execution policy) and the governance in [CONTRIBUTING.md](CONTRIBUTING.md).

## Before changing anything

1. Read the relevant parts of the governing spec. The derived requirements are in `governance/requirements_registry.yaml` and the original TDS is identified in `docs/00-source-specifications/specification_manifest.yaml`. Also read the applicable ADRs in `governance/decisions/decision_register.yaml` and the contracts in `contracts/`.
2. State the task's **requirement IDs, scope, dependencies, assumptions and affected contract versions** (F8-116) before editing.
3. Check `governance/findings_register.yaml`. Do not implement anything that an `OPEN` finding with `blocks:` covers.
4. If a missing decision changes **security, ABI, data semantics or recovery behavior**, stop. Raise a finding or a draft ADR and ask for approval (F8-120). Do not choose silently.

## Source-of-truth hierarchy

Approved requirements/ADRs → approved machine-readable contracts → component specs → code → test evidence → generated docs. Keep one authoritative copy of each fact. If the TDS and a contract disagree, record a finding and block dependent work. Do not "fix" either side unilaterally.

## Hard rules

- **No fabrication.** Never record approvals, test results, benchmarks, hardware validation or completed features that did not happen. An unknown test state is `NOT_RUN`, never `PASS` (TDS §E3).
- **VERIFIED requires evidence.** A requirement or work item may move to `VERIFIED` only with a reproducible test result and a reviewer identity recorded in `governance/evidence/`. See the transitions in `governance/workflow.yaml`.
- Treat TDS code blocks (C1.1, D2.1, D3.1, E2.1) as **illustrative candidates**, not approved code (F8-117).
- Do not deploy to production or customer workloads, and do not enable active prevention outside a lab, without recorded canary and safety sign-off (F8-123).
- Do not run destructive or privileged operations without explicit user approval: `sudo`, package installs, kernel module/BPF loads on a non-lab host, force-push, history rewrite, deleting branches or files you did not create.
- Never commit secrets, keys, tokens or customer data. Never weaken or skip security checks, signature verification or tests to make a build pass.
- Do not commit the original specification documents (`*.docx`/`*.pdf`); see FND-013.
- Do not claim that GitHub settings (branch protection, teams, required reviews) are configured unless you verified them through the GitHub API in this session.

## Multi-agent work

- Use the fewest agents needed. Parallelize only independent work.
- Each agent in `.claude/agents/` owns the paths listed in its definition. Edit outside your ownership only through a hand-off to the owning agent or with explicit user approval.
- Use isolated worktrees for parallel agents (F8-118). Two agents never edit the same file concurrently.
- Dependent implementation starts only after its contract (`contracts/`, CTR-00x) is `APPROVED`.
- Keep summaries short and link to files and lines.

## Verification commands

```sh
python3 tools/governance/validate_governance.py   # YAML/JSON parse, ID uniqueness, links, status rules
tools/bootstrap/check_prereqs.sh                  # toolchain report (non-destructive)
```

Run targeted lint/build/unit tests before integration and attach real command output to evidence (F8-119). After each merge, update requirement→code→test links in `governance/traceability.yaml` (F8-122).

## Lifecycle states

`DRAFT → REVIEW → APPROVED → IMPLEMENTING → IMPLEMENTED → TESTED → VERIFIED → RELEASED`, with allowed transitions and approval authority defined in `governance/workflow.yaml`.
