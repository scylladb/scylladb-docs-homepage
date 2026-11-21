# Nodetool cluster

**cluster** - Nodetool supercommand for running cluster operations.

## Supported cluster suboperations

* [repair](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/cluster/repair.md)  `<keyspace>` `<table>` - Repair one or more tablet tables.
* [cleanup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/cluster/cleanup.md)  - Clean up all non tablet (vnode-based) keyspaces in a cluster
* [snapshot](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/snapshot.md) - Take a cluster-wide snapshot of keyspaces or tables.
* [backup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/backup.md) - Back up a cluster-wide snapshot to object storage.
