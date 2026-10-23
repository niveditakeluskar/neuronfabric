# integrations/kubernetes/controller/ — Kubernetes watcher, enrichment and admission webhook

Watches Pods/Nodes/Namespaces/owners, maps cgroup/container IDs to Pod UID and workload revision, and serves the admission webhook for deployment-time policy.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §C4#42–46 |
| Owner (role) | K8s Lead |
| Claude agent | `kubernetes-engineer` |
| Requirements | NG-K8S-001, NG-K8S-003, NG-K8S-005, NG-K8S-006 |
| Contracts | CTR-005 Kubernetes API versioned mapping; admission decision contract |
| Gate | G-C4 (NG-K8S-001 program gate G7) |

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
