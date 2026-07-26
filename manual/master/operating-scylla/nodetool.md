# Nodetool

The `nodetool` utility provides a simple command-line interface to the following exposed operations and attributes.

<a id="nodetool-generic-options"></a>

## Nodetool generic options

* `-p <port>` or `--port <port>` - The port of the REST API of the ScyllaDB node.
* `--` - Separates command-line options from the list of argument(useful when an argument might be mistaken for a command-line option).

## Supported Nodetool operations

Operations that are not listed below are currently not available.

* [backup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/backup.md) - Copy SSTables from a specified keyspace’s snapshot to a designated bucket in object storage.
* [cfhistograms](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/cfhistograms.md) - Provides statistics about a table, including number of SSTables, read/write latency, partition size and column count.
* [cfstats](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/cfstats.md) - Provides in-depth diagnostics regard table.
* [checkandrepaircdcstreams](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/checkandrepaircdcstreams.md) - Checks and fixes CDC streams.
* [cleanup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/cleanup.md) - Triggers the immediate cleanup of keys no longer belonging to a node.
* [clearsnapshot](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/clearsnapshot.md) - This command removes snapshots.
* [cluster](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/cluster/index.md) - Run a cluster operation.
* [compact](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/compact.md)- Force a (major) compaction on one or more column families.
* [compactionhistory](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/compactionhistory.md) - Provides the history of compactions.
* [compactionstats](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/compactionstats.md)- Print statistics on compactions.
* [decommission](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/decommission.md) - Decommission the node.
* [describecluster](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/describecluster.md) - Print the name, snitch, partitioner and schema version of a cluster.
* [describering](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/describering.md) - `<keyspace>`- Shows the partition ranges of a given keyspace.
* [disableautocompaction](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/disableautocompaction.md) - Disable automatic compaction of a keyspace or table.
* [disablebackup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/disablebackup.md) - Disable incremental backup.
* [disablebinary](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/disablebinary.md) - Disable native transport (binary protocol).
* [disablegossip](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/disablegossip.md) - Disable gossip (effectively marking the node down).
* [drain](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/drain.md) - Drain the node (stop accepting writes and flush all column families).
* [dropquarantinedsstables](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/dropquarantinedsstables.md) `<keyspace>` `<table>` Drop quarantined SSTables from the specified keyspace and table(s), or from all keyspaces if no keyspace is specified.
* [enableautocompaction](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/enableautocompaction.md) - Enable automatic compaction of a keyspace or table.
* [enablebackup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/enablebackup.md) - Enable incremental backup.
* [enablebinary](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/enablebinary.md) - Re-enable native transport (binary protocol).
* [enablegossip](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/enablegossip.md) - Re-enable gossip.
* [excludenode](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/excludenode.md)- Mark nodes as permanently down.
* [flush](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/flush.md) - Flush one or more column families.
* [getcompactionthroughput](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/getcompactionthroughput.md) - Print the throughput cap for compaction in the system
* [getendpoints](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/getendpoints.md) `<keyspace>` `<table>` `<key>`- Print the end points that owns the key.
* **getlogginglevels** - Get the runtime logging levels.
* [getsstables](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/getsstables.md) - Print the sstable filenames that own the key.
* [getstreamthroughput](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/getstreamthroughput.md) - Print the throughput cap for SSTables streaming in the system
* [gettraceprobability](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/gettraceprobability.md) - Displays the current trace probability value. 0 is disabled 1 is enabled.
* [gossipinfo](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/gossipinfo.md) - Shows the gossip information for the cluster.
* [help](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/help.md) - Display list of available nodetool commands.
* [info](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/info.md) - Print node information
* [listsnapshots](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/listsnapshots.md) - Lists all the snapshots along with the size on disk and true size.
* **move** `<new token>`- Move node on the token ring to a new token
* **netstats** - Print network information on provided host (connecting node by default)
* [proxyhistograms](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/proxyhistograms.md) - Print statistic histograms for network operations
* [rebuild](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/rebuild.md) `[<src-dc-name>]`- Rebuild data by streaming from other nodes
* [refresh](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/refresh.md)- Load newly placed SSTables to the system without restart
* [removenode](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/removenode.md)- Remove node with the provided ID
* [repair](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/repair.md)  `<keyspace>` `<table>` - Repair one or more vnode tables.
* [resetlocalschema](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/resetlocalschema.md) - Reset the node’s local schema.
* [restore](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/restore.md) - Load SSTables from a designated bucket in object store into a specified keyspace or table
* [ring](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/ring.md) - The nodetool ring command display the token ring information.
* [scrub](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/scrub.md) `[-m mode] [--no-snapshot] <keyspace> [<table>...]` - Scrub the SSTable files in the specified keyspace or table(s)
* [setcompactionthroughput](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/setcompactionthroughput.md) - Set the throughput cap for compaction in the system
* [setlogginglevel](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/setlogginglevel.md) - sets the logging level threshold for ScyllaDB classes
* [setstreamthroughput](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/setstreamthroughput.md) - Set the throughput cap for SSTables streaming in the system
* [settraceprobability](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/settraceprobability.md) `<value>` - Sets the probability for tracing a request. race probability value
* [snapshot](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/snapshot.md) `[-t tag] [-cf column_family] <keyspace>`  - Take a snapshot of specified keyspaces or a snapshot of the specified table.
* [sstableinfo](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/sstableinfo.md) - Get information about sstables per keyspace/table.
* [status](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/status.md) - Print cluster information.
* [statusbackup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/statusbackup.md) - Status of incremental backup.
* [statusbinary](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/statusbinary.md) - Status of native transport (binary protocol).
* [statusgossip](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/statusgossip.md) - Status of gossip.
* [stop](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/stop.md) - Stop compaction operation.
* **tablehistograms** see [cfhistograms](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/cfhistograms.md)
* [tablestats](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/tablestats.md) - Provides in-depth diagnostics regard table.
* [tasks](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/tasks/index.md) - Manage tasks manager tasks.
* [toppartitions](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/toppartitions.md) - Samples cluster writes and reads and reports the most active partitions in a specified table and time frame.
* [upgradesstables](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/upgradesstables.md) - Upgrades each table that is not running the latest ScyllaDB version, by rewriting SSTables.
* [version](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/version.md) - Print the DB version.
* [viewbuildstatus](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/viewbuildstatus.md) - Shows the progress of a materialized view build.
