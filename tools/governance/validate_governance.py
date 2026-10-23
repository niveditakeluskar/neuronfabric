#!/usr/bin/env python3
"""Validate NeuroGuard governance artifacts.

Checks: every YAML/JSON file parses; required files exist; requirement, decision, finding,
risk and backlog IDs are unique and well-formed; cross-references resolve; lifecycle rules
hold (no APPROVED without an approval record, no TESTED/VERIFIED/RELEASED without evidence,
no PASS test without evidence); traceability covers the registry 1:1; planned module paths
exist; the backlog has no dependency cycles; simple secret patterns are absent.

Optional: --spec-root DIR verifies SHA-256 of the registered source specifications.

Read-only. Uses PyYAML if installed, otherwise falls back to Ruby's bundled YAML parser.
Exit status: 0 = pass, 1 = errors found, 2 = could not run.
"""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", "node_modules", "target", "build", ".venv", "__pycache__"}

REQUIRED_FILES = [
    "CLAUDE.md", "README.md", "CONTRIBUTING.md", "SECURITY.md",
    ".github/CODEOWNERS", ".github/PULL_REQUEST_TEMPLATE.md",
    "governance/requirements_registry.yaml", "governance/traceability.yaml",
    "governance/findings_register.yaml", "governance/workflow.yaml", "governance/backlog.yaml",
    "governance/decisions/decision_register.yaml", "governance/risks/risk_register.yaml",
    "governance/approvals/approval_register.yaml",
    "docs/00-source-specifications/specification_manifest.yaml",
    "docs/02-system-architecture/architecture_overview.md",
    "docs/16-development-environments/environment_matrix.md",
    "docs/20-release-management/release_gates.md",
]

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA |)PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"(?i)(password|secret|api[_-]?key|token)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"),
]

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def _yaml_loader():
    try:
        import yaml  # type: ignore

        return lambda p: yaml.safe_load(p.read_text(encoding="utf-8"))
    except ImportError:
        pass
    ruby = shutil.which("ruby")
    if not ruby:
        return None
    script = "require 'yaml'; require 'json'; puts JSON.generate(YAML.safe_load(File.read(ARGV[0])))"

    def load(p):
        out = subprocess.run([ruby, "-e", script, str(p)], capture_output=True, text=True)
        if out.returncode != 0:
            lines = out.stderr.strip().splitlines()
            raise ValueError(lines[0] if lines else "ruby YAML error")
        return json.loads(out.stdout)

    return load


def walk(suffixes):
    for p in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        if p.is_file() and p.suffix in suffixes:
            yield p


def ids_unique(items, label):
    seen = set()
    for it in items:
        i = it.get("id")
        if i in seen:
            err(f"{label}: duplicate id {i}")
        seen.add(i)
    return seen


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--spec-root", help="directory holding the original specification files")
    args = ap.parse_args()

    load_yaml = _yaml_loader()
    if load_yaml is None:
        print("ERROR: no YAML parser available (install PyYAML or Ruby)", file=sys.stderr)
        return 2

    # 1. Required files
    for f in REQUIRED_FILES:
        if not (ROOT / f).is_file():
            err(f"missing required file: {f}")

    # 2. Parse every YAML/JSON file
    docs = {}
    for p in walk({".yaml", ".yml"}):
        try:
            docs[str(p.relative_to(ROOT))] = load_yaml(p)
        except Exception as e:  # noqa: BLE001 - report any parse failure
            err(f"YAML parse error in {p.relative_to(ROOT)}: {e}")
    for p in walk({".json"}):
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            err(f"JSON parse error in {p.relative_to(ROOT)}: {e}")

    def doc(rel):
        d = docs.get(rel)
        if not isinstance(d, dict):
            err(f"{rel}: not a mapping or failed to parse")
            return {}
        return d

    workflow = doc("governance/workflow.yaml")
    states = {s["id"] for s in workflow.get("states", [])}
    test_states = set(workflow.get("test_result_states", []))

    reg = doc("governance/requirements_registry.yaml")
    decisions = doc("governance/decisions/decision_register.yaml").get("decisions", [])
    findings = doc("governance/findings_register.yaml").get("findings", [])
    risks = doc("governance/risks/risk_register.yaml").get("risks", [])
    backlog = doc("governance/backlog.yaml").get("items", [])
    trace = doc("governance/traceability.yaml").get("links", [])
    approvals = doc("governance/approvals/approval_register.yaml").get("approvals", []) or []
    manifest = doc("docs/00-source-specifications/specification_manifest.yaml")

    approved_subjects = {a.get("subject") for a in approvals if a.get("decision") == "APPROVED"}

    # 3. Requirements
    reqs = reg.get("requirements", [])
    prefixes = set((reg.get("id_prefixes") or {}).keys())
    req_ids = ids_unique(reqs, "requirements")
    dec_ids = ids_unique(decisions, "decisions")
    fnd_ids = ids_unique(findings, "findings")
    rsk_ids = ids_unique(risks, "risks")
    wi_ids = ids_unique(backlog, "backlog")
    all_ids = req_ids | dec_ids | fnd_ids | rsk_ids | wi_ids

    req_fields = ["id", "title", "statement", "owner", "source_refs", "priority", "status",
                  "dependencies", "acceptance_criteria", "verification_method", "section_gate"]
    source_id_owner = {}
    for r in reqs:
        rid = r.get("id", "<no id>")
        for f in req_fields:
            if r.get(f) in (None, "", []) and f != "dependencies":
                err(f"{rid}: missing field '{f}'")
        m = re.fullmatch(r"(NG-[A-Z0-9]+)-(\d{3})", rid)
        if not m or m.group(1) not in prefixes:
            err(f"{rid}: id does not match NG-<PREFIX>-NNN with a registered prefix")
        if r.get("status") not in states:
            err(f"{rid}: unknown status {r.get('status')}")
        if r.get("priority") not in {"P0", "P1", "P2"}:
            err(f"{rid}: invalid priority {r.get('priority')}")
        vm = r.get("verification_method") or {}
        if vm.get("type") not in {"test", "inspection", "analysis", "demonstration", "review"}:
            err(f"{rid}: invalid verification_method.type")
        for d in r.get("dependencies") or []:
            if d not in req_ids and d not in dec_ids:
                err(f"{rid}: dependency {d} not found")
            if d == rid:
                err(f"{rid}: depends on itself")
        for s in r.get("source_ids") or []:
            if s in source_id_owner:
                err(f"source id {s} claimed by both {source_id_owner[s]} and {rid}")
            source_id_owner[s] = rid
        if r.get("status") in {"APPROVED", "IMPLEMENTING", "IMPLEMENTED", "TESTED", "VERIFIED", "RELEASED"} \
                and rid not in approved_subjects:
            err(f"{rid}: status {r.get('status')} without an APPROVED record in approval_register.yaml")

    for m in reg.get("id_mapping") or []:
        rid, sid = m.get("registry_id"), m.get("source_id")
        if rid not in req_ids:
            err(f"id_mapping: {sid} → {rid} does not exist")
        elif source_id_owner.get(sid) != rid:
            err(f"id_mapping: {sid} → {rid} but {rid}.source_ids does not contain {sid}")
    mapped = {m.get("source_id") for m in reg.get("id_mapping") or []}
    for s, rid in source_id_owner.items():
        if s not in mapped:
            err(f"{rid}: source id {s} has no entry in id_mapping")

    # 4. Decisions
    for d in decisions:
        if d.get("status") not in states:
            err(f"{d.get('id')}: unknown status {d.get('status')}")
        if not re.fullmatch(r"ADR-\d{3}", str(d.get("id"))):
            err(f"{d.get('id')}: id does not match ADR-NNN")
        if d.get("status") == "APPROVED" and d.get("id") not in approved_subjects:
            err(f"{d.get('id')}: APPROVED without approval record")
        rec = d.get("record")
        if rec and not (ROOT / rec.split("#")[0]).exists():
            err(f"{d.get('id')}: record path {rec} does not exist")

    # 5. Traceability (1:1 with registry)
    trace_ids = [t.get("requirement") for t in trace]
    for t in set(trace_ids):
        if trace_ids.count(t) > 1:
            err(f"traceability: duplicate entry for {t}")
    for rid in req_ids - set(trace_ids):
        err(f"traceability: no entry for {rid}")
    for rid in set(trace_ids) - req_ids:
        err(f"traceability: entry for unknown requirement {rid}")
    status_of = {r["id"]: r.get("status") for r in reqs}
    undefined_tests = 0
    for t in trace:
        rid = t.get("requirement")
        for mod in t.get("planned_modules") or []:
            if not (ROOT / mod).exists():
                err(f"traceability {rid}: planned module path '{mod}' does not exist")
        tests = t.get("tests") or []
        if not tests:
            undefined_tests += 1
        for tc in tests:
            if tc.get("status") not in test_states:
                err(f"traceability {rid}: test {tc.get('id')} has invalid status {tc.get('status')}")
            if tc.get("status") == "PASS" and not t.get("evidence"):
                err(f"traceability {rid}: test {tc.get('id')} PASS without evidence")
        for ev in t.get("evidence") or []:
            if not (ROOT / ev).is_file():
                err(f"traceability {rid}: evidence file {ev} not found")
        if status_of.get(rid) in {"TESTED", "VERIFIED", "RELEASED"} and not t.get("evidence"):
            err(f"{rid}: status {status_of.get(rid)} without evidence")
    if undefined_tests:
        warn(f"{undefined_tests} requirements have no test IDs defined yet (must be added before APPROVED)")

    # 6. Findings, risks, backlog references
    for f in findings:
        if f.get("status") not in {"OPEN", "RESOLVED", "ACCEPTED"}:
            err(f"{f.get('id')}: invalid status {f.get('status')}")
        for b in f.get("blocks") or []:
            if b not in all_ids:
                err(f"{f.get('id')}: blocks unknown id {b}")
    for r in risks:
        for x in r.get("related") or []:
            if x not in all_ids:
                err(f"{r.get('id')}: related unknown id {x}")

    agents_dir = ROOT / ".claude" / "agents"
    agent_names = {p.stem for p in agents_dir.glob("*.md")} if agents_dir.is_dir() else set()
    graph = {}
    for w in backlog:
        wid = w.get("id")
        if w.get("status") not in states:
            err(f"{wid}: unknown status {w.get('status')}")
        for key in ("requirements", "decisions", "resolves", "depends_on"):
            for x in w.get(key) or []:
                if x not in all_ids:
                    err(f"{wid}: {key} references unknown id {x}")
        if w.get("agent") and w.get("agent") not in agent_names:
            err(f"{wid}: agent {w.get('agent')} has no definition in .claude/agents/")
        graph[wid] = list(w.get("depends_on") or [])

    visiting, done = set(), set()

    def visit(n, path):
        if n in done:
            return
        if n in visiting:
            err(f"backlog dependency cycle: {' -> '.join(path + [n])}")
            return
        visiting.add(n)
        for m in graph.get(n, []):
            visit(m, path + [n])
        visiting.discard(n)
        done.add(n)

    for n in graph:
        visit(n, [])

    # 7. Specification manifest
    spec_ids = set()
    for s in manifest.get("documents", []) or []:
        if s.get("id") in spec_ids:
            err(f"manifest: duplicate {s.get('id')}")
        spec_ids.add(s.get("id"))
        for f in s.get("files", []):
            if not re.fullmatch(r"[0-9a-f]{64}", str(f.get("sha256"))):
                err(f"manifest {s.get('id')}: invalid sha256 for {f.get('name')}")
            if args.spec_root:
                p = Path(args.spec_root) / f["name"]
                if not p.is_file():
                    err(f"spec file not found: {p}")
                elif hashlib.sha256(p.read_bytes()).hexdigest() != f["sha256"]:
                    err(f"spec file CHANGED since registration: {p}")

    # 8. Secret patterns in tracked-type text files
    for p in walk({".md", ".yaml", ".yml", ".json", ".sh", ".py", ".toml", ".txt", ""}):
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                err(f"possible secret in {p.relative_to(ROOT)} (pattern {pat.pattern[:30]}...)")

    # Report
    print(f"Parsed {len(docs)} YAML files; {len(reqs)} requirements, {len(decisions)} decisions, "
          f"{len(findings)} findings, {len(risks)} risks, {len(backlog)} backlog items.")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print("RESULT:", "PASS" if not errors else f"FAIL ({len(errors)} errors)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
