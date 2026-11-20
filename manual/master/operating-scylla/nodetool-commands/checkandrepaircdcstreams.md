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

[Change Data Capture (CDC)](https://docs.scylladb.com/manual/master/features/cdc/index.md)

[Nodetool Reference](https://docs.scylladb.com/manual/master/operating-scylla/nodetool.md)
