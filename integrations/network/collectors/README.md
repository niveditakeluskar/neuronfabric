# integrations/network/collectors/ — Network telemetry collectors (Go)

Read-only collection of SNMPv3 authPriv, syslog over TLS, NetFlow/IPFIX and NETCONF/RESTCONF data, normalized with source confidence.

| | |
|---|---|
| Status | **Not started.** No implementation exists (Prompt 00 initialization). |
| TDS v2 reference | §C5#47, §C5#49–51 |
| Owner (role) | Network Lead |
| Claude agent | `network-infrastructure-engineer` |
| Requirements | NG-NET-002, NG-NET-004, NG-NET-005 |
| Contracts | NetworkDevice record; CTR-002 events.proto |
| Gate | G-C5 |

- No broad unauthenticated scanning. Credentials are isolated per tenant/site.

See [governance/requirements_registry.yaml](../../../governance/requirements_registry.yaml) for the requirement details.
