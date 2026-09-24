# Nodetool checkAndRepairCdcStreams

Checks if CDC streams reflect the current cluster topology, and regenerates them if they don’t.

#### WARNING
Do not use this operation while performing other administrative tasks, such as
bootstrapping or decommissioning a node.

## Usage

```console
nodetool checkAndRepairCdcStreams
```

## See Also

[Change Data Capture (CDC)](https://docs.scylladb.com/manual/branch-2025.2/features/cdc/index.md)

[Upgrading from experimental CDC](https://docs.scylladb.com/manual/branch-2025.2/kb/cdc-experimental-upgrade.md)

[Nodetool Reference](https://docs.scylladb.com/manual/branch-2025.2/operating-scylla/nodetool.md)
