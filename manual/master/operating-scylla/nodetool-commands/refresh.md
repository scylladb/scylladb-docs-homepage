# Nodetool refresh

**refresh** - Load newly placed SSTables to the system without a restart. This is the only supported way to upload SSTables directly to a node. Placing them directly in the node’s data directory is not supported and will lead to failures.

Copy the files to the table’s upload directory, by default it is located under `/var/lib/scylla/data/keyspace_name/table_name-UUID/upload`.

If the table has any [Materialized Views (MV)](https://docs.scylladb.com/manual/master/cql/mv.md) or [Secondary Indexes (SI)](https://docs.scylladb.com/manual/master/cql/secondary-indexes.md), content view updates will be generated from the uploaded SSTables. Uploading MV or SI SSTables is not required and will fail.

<a id="nodetool-refresh-local"></a>

## Local refresh

#### NOTE
This mode is not supported for [tablets](https://docs.scylladb.com/manual/master/architecture/tablets.md).

SSTables are copied from the upload directory to the table’s data directory and added to the table’s SSTable registry.

After the upload, ScyllaDB will run cleanup on the uploaded SSTables, to remove any partition which is not owned by the target node.
Use `--skip-cleanup` to skip this step. Note that this can lead to increased disk utilization, use only if you are certain the SSTables contain only data owned by the target node.

The uploaded SSTables may disrupt the SSTable layout maintained by the table’s compaction strategy. To remedy this, ScyllaDB runs an off-strategy compaction after the upload.
Use `--skip-reshape` to skip this step. Note that this can lead to increased read amplification and increased latencies due to reads having to consult more SSTables than optimal.

Although this is the default mode for `nodetool refresh`, using this mode to restore backed up SSTables is not efficient. For restoring backup use [–load-and-stream](#nodetool-refresh-load-and-stream) instead.
Use local upload if you are certain that uploaded SSTables contain data only for the target node.

Syntax:

```default
nodetool refresh <my_keyspace> <my_table> [--skip-cleanup] [--skip-reshape]
```

Example:

```default
cp /path/to/my/sstables/* /var/lib/scylla/data/nba/player_stats-91cd2060f99d11e6a47/upload

nodetool refresh nba player_stats
```

<a id="nodetool-refresh-load-and-stream"></a>

## Load and Stream

SSTables are read and each partition is streamed to its respective replica(s). Allows efficient upload of SSTables to a cluster.
Each SSTable has to be uploaded only once, as `--load-and-stream` will ensure that all partitions reach their respective replicas.
The `--scope` and `--primary-replica-only` options can be used to filter the set of target replicas for each partition.

Syntax:

```default
nodetool refresh <my_keyspace> <my_table> [(--load-and-stream | -las) [[(--primary-replica-only | -pro)] | [--scope <scope>]]]
```

### Filter target replicas

By default, each partition is streamed to all nodes which are replicas for the partition.
This can be inefficient in a large cluster, especially if there are multiple Datacenters.
Constraining the subset of replicas where data will be streamed to allows orchestrating concurrent upload to multiple nodes without duplicate work – the same partition being streamed to a replica from multiple source nodes.

There are two options available to manipulate the replica(s) to stream data to: `--primary-replica-only` and `--scope`.
The two are mutually exclusive.

The `--primary-replica-only` (or `-pro`) option makes ScyllaDB only stream each partition to its primary replica.
After all SSTables are uploaded to the cluster, a repair is required to replicate data to all replicas.

The `--scope` parameter allows for more advanced constraining of the subset of nodes where data will be streamed:

* `node` - the local node (roughly equivalent to [local refresh](#nodetool-refresh-local))
* `rack` - replicas in the local rack
* `dc` - replicas in the local datacenter (DC)
* `all` (default) - all replicas in the cluster

## Compatibility with Apache Cassandra SSTables

Uploading SSTable from Apache Cassandra is supported. For the supported SSTable versions, see [ScyllaDB SSTable Format](https://docs.scylladb.com/manual/master/architecture/sstable/index.md). Note that SSTables using Trie-Based Indexes are *not* supported.

### Known Problems

#### Digest mismatch

Apache Cassandra and ScyllaDB slightly diverged on how digests are calculated on SSTable Data components.
For compressed SSTables, Apache Cassandra allows for a trailing zero-sized (pre-compression) chunk in the Data component.
This chunk has no data but has non-zero size after compression.
This trailing chunk is ignored by ScyllaDB and thus excluded from the Digest calculation, therefore the digest calculated by ScyllaDB will not match that in the Digest component.
Consequently ScyllaDB will reject the SSTable file.

Example:

```default
sstables::malformed_sstable_exception Failed to read partition from SSTable .../me-71-big-Data.db due to Digest mismatch: expected=1580246239, actual=3782253270
```

Workaround: delete the Digest component (`me-*-big-Digest.crc32`) and remove it from the TOC file (`me-*-big-TOC.txt`) too.
Before doing so, it is important to confirm that the cause of the digest mismatch is indeed a trailing 0-sized chunk, not a genuine corruption.

[Nodetool Reference](https://docs.scylladb.com/manual/master/operating-scylla/nodetool.md)
