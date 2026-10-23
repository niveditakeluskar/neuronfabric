# integrations/kubernetes/chart/ — Helm chart

Helm chart deploying the Linux sensor DaemonSet and the Kubernetes controller, with images pinned by digest and least-privilege RBAC.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §C4#41, §C4 table |
| Owner (role) | K8s Lead |
| Claude agent | `kubernetes-engineer` |
| Requirements | NG-K8S-002, NG-K8S-004 |
| Contracts | — |
| Gate | G-C4 |

- Every privileged setting and host mount must be documented with a justification.

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
