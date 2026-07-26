<a id="glossary"></a>

# Glossary

<a id="term-Anti-entropy"></a>

Anti-entropy
: A state where data is in order and organized. ScyllaDB has processes in place to make sure that data is antientropic where all replicas contain the most recent data and that data is consistent between replicas. See [ScyllaDB Anti-Entropy](https://docs.scylladb.com/manual/master/architecture/anti-entropy/index.md).

<a id="term-Bootstrap"></a>

Bootstrap
: When a new node is added to a cluster, the bootstrap process ensures that the data in the cluster is automatically redistributed to the new node. A new node in this case is an empty node without system tables or data. See [bootstrap](https://docs.scylladb.com/manual/master/kb/compaction.md#temporary-fallback-to-stcs).

<a id="term-CAP-Theorem"></a>

CAP Theorem
: The CAP Theorem is the notion that **C** (Consistency), **A** (Availability) and **P** (Partition Tolerance) of data are mutually dependent in a distributed system. Increasing any 2 of these factors will reduce the third. ScyllaDB chooses availability and partition tolerance over consistency. See [Fault Tolerance](https://docs.scylladb.com/manual/master/architecture/architecture-fault-tolerance.md).

<a id="term-Cluster"></a>

Cluster
: One or multiple ScyllaDB nodes, acting in concert, which own a single contiguous token range. State is communicated between nodes in the cluster via [Raft](https://docs.scylladb.com/manual/master/architecture/raft.md).

<a id="term-Clustering-Key"></a>

Clustering Key
: A single or multi-column clustering key determines a row’s uniqueness and sort order on disk within a partition. See [Ring Architecture](https://docs.scylladb.com/manual/master/architecture/ringarchitecture/index.md).

<a id="term-Colocated-Table"></a>

Colocated Table
: An internal table of a special type in a [tablets](https://docs.scylladb.com/manual/master/architecture/tablets.md) enabled keyspace that is colocated with another base table, meaning it always has the same tablet replicas as the base table.
  Current types of colocated tables include CDC log tables, local indexes, and materialized views that have the same partition key as their base table.

<a id="term-Column-Family"></a>

Column Family
: See [table](#term-Table).

<a id="term-Compaction"></a>

Compaction
: The process of reading several SSTables, comparing the data and time stamps and then writing one SSTable containing the merged, most recent, information. See [Compaction Strategies](https://docs.scylladb.com/manual/master/architecture/compaction/compaction-strategies.md).

<a id="term-Compaction-Strategy"></a>

Compaction Strategy
: Determines which of the SSTables will be compacted, and when. See [Compaction Strategies](https://docs.scylladb.com/manual/master/architecture/compaction/compaction-strategies.md).

<a id="term-Consistency-Level-CL"></a>

Consistency Level (CL)
: A dynamic value which dictates the number of replicas (in a cluster) that must acknowledge a read or write operation. This value is set by the client on a per operation basis. For the CQL Shell, the consistency level defaults to ONE for read and write operations. See [Consistency Levels](https://docs.scylladb.com/manual/master/cql/consistency.md).

<a id="term-Dummy-Rows"></a>

Dummy Rows
: Cache dummy rows are entries in the row set, which have a clustering position, although they do not represent CQL rows written by users.  ScyllaDB cache uses them to mark boundaries of population ranges, to represent the information that the whole range is complete, and there is no need to go to sstables to read the gaps between existing row entries when scanning.

<a id="term-Entropy"></a>

Entropy
: A state where data is not consistent. This is the result when replicas are not synced and data is random. ScyllaDB has measures in place to be antientropic. See [ScyllaDB Anti-Entropy](https://docs.scylladb.com/manual/master/architecture/anti-entropy/index.md).

<a id="term-Eventual-Consistency"></a>

Eventual Consistency
: In ScyllaDB, when considering the [CAP Theorem](#term-CAP-Theorem), availability and partition tolerance are considered a higher priority than consistency.

<a id="term-Hint"></a>

Hint
: A short record of a write request that is held by the co-ordinator until the unresponsive node becomes responsive again, at which point the write request data in the hint is written to the replica node. See [Hinted Handoff](https://docs.scylladb.com/manual/master/architecture/anti-entropy/hinted-handoff.md).

<a id="term-Hinted-Handoff"></a>

Hinted Handoff
: Reduces data inconsistency which can occur when a node is down or there is network congestion. In ScyllaDB, when data is written and there is an unresponsive replica, the coordinator writes itself a hint. When the node recovers, the coordinator sends the node the pending hints to ensure that it has the data it should have received. See [Hinted Handoff](https://docs.scylladb.com/manual/master/architecture/anti-entropy/hinted-handoff.md).

<a id="term-Idempotent"></a>

Idempotent
: Denoting an element of a set which is unchanged in value when multiplied or otherwise operated on by itself. [ScyllaDB Counters](https://docs.scylladb.com/manual/master/features/counters.md) are not indepotent because in the case of a write failure, the client cannot safely retry the request.

<a id="term-JBOD"></a>

JBOD
: JBOD or Just another Bunch Of Disks is a non-raid storage system using a server with multiple disks in order to instantiate a separate file system per disk. The benefit is that if a single disk fails, only it needs to be replaced and not the whole disk array. The disadvantage is that free space and load may not be evenly distributed. See the [FAQ](https://docs.scylladb.com/manual/master/faq.md#faq-raid0-required).

<a id="term-Key-Management-Interoperability-Protocol-KMIP"></a>

Key Management Interoperability Protocol (KMIP)
:  is a communication protocol that defines message formats for storing keys on a key management server (KMIP server). You can use a KMIP server to protect your keys when using Encryption at Rest. See [Encryption at Rest](https://docs.scylladb.com/manual/master/operating-scylla/security/encryption-at-rest.md).

<a id="term-Keyspace"></a>

Keyspace
: A collection of tables with attributes which define how data is replicated on nodes. See [Ring Architecture](https://docs.scylladb.com/manual/master/architecture/ringarchitecture/index.md).

<a id="term-Leveled-compaction-strategy-LCS"></a>

Leveled compaction strategy (LCS)
:  uses small, fixed-size (by default 160 MB) SSTables divided into different levels. See [Compaction Strategies](https://docs.scylladb.com/manual/master/architecture/compaction/compaction-strategies.md).

<a id="term-Liveness"></a>

Liveness
: The ability to update a configuration property without restarting the node. Properties that support live updates can be updated via the `system.config` virtual table or the REST API.
  The change will take effect without a node restart, changing the value in the config file, then sending `SIGHUP` to the scylla-process, triggering it to re-read its configuration.

<a id="term-Log-structured-merge-LSM"></a>

Log-structured-merge (LSM)
: A technique of keeping sorted files and merging them. LSM is a data structure that maintains key-value pairs. See [Compaction](https://docs.scylladb.com/manual/master/kb/compaction.md)

<a id="term-Logical-Core-lcore"></a>

Logical Core (lcore)
: A hyperthreaded core on a hyperthreaded system, or a physical core on a system without hyperthreading.

<a id="term-MemTable"></a>

MemTable
: An in-memory data structure servicing both reads and writes. Once full, the Memtable flushes to an [SSTable](#term-SSTable). See [Compaction Strategies](https://docs.scylladb.com/manual/master/architecture/compaction/compaction-strategies.md).

<a id="term-MurmurHash3"></a>

MurmurHash3
: A hash function [created by Austin Appleby](https://en.wikipedia.org/wiki/MurmurHash), and used by the [Partitioner](#term-Partitioner) to distribute the partitions between nodes.
  The name comes from two basic operations, multiply (MU) and rotate (R), used in its inner loop.
  The MurmurHash3 version used in ScyllaDB originated from [Apache Cassandra](https://commons.apache.org/proper/commons-codec/apidocs/org/apache/commons/codec/digest/MurmurHash3.html), and is **not** identical to the [official MurmurHash3 calculation](https://github.com/apache/cassandra/blob/trunk/src/java/org/apache/cassandra/utils/MurmurHash.java#L31-L33). More [here](https://github.com/russss/murmur3-cassandra).

<a id="term-Mutation"></a>

Mutation
: A change to data such as column or columns to insert, or a deletion. See [Hinted Handoff](https://docs.scylladb.com/manual/master/architecture/anti-entropy/hinted-handoff.md).

<a id="term-Node"></a>

Node
: A single installed instance of ScyllaDB. See [Ring Architecture](https://docs.scylladb.com/manual/master/architecture/ringarchitecture/index.md).

<a id="term-Nodetool"></a>

Nodetool
: A simple command-line interface for administering a ScyllaDB node. A nodetool command can display a given node’s exposed operations and attributes. ScyllaDB’s nodetool contains a subset of these operations. See [Ring Architecture](https://docs.scylladb.com/manual/master/architecture/ringarchitecture/index.md).

<a id="term-Partition"></a>

Partition
: A subset of data that is stored on a node and replicated across nodes. There are two ways to consider a partition. In CQL, a partition appears as a group of sorted rows, and is the unit of access for queried data, given that most queries access a single partition. On the physical layer, a partition is a unit of data stored on a node and is identified by a partition key. See [Ring Architecture](https://docs.scylladb.com/manual/master/architecture/ringarchitecture/index.md).

<a id="term-Partition-Key"></a>

Partition Key
: The unique identifier for a partition, a partition key may be hashed from the first column in the primary key. A partition key may also be hashed from a set of columns, often referred to as a compound primary key. A partition key determines which virtual node gets the first partition replica. See [Ring Architecture](https://docs.scylladb.com/manual/master/architecture/ringarchitecture/index.md).

<a id="term-Partitioner"></a>

Partitioner
: A hash function for computing which data is stored on which node in the cluster. The partitioner takes a partition key as an input, and returns a ring token as an output. By default ScyllaDB uses the 64 bit [MurmurHash3](#term-MurmurHash3) function and this hash range is numerically represented as a signed 64bit integer, see [Ring Architecture](https://docs.scylladb.com/manual/master/architecture/ringarchitecture/index.md).

<a id="term-Primary-Key"></a>

Primary Key
: In a CQL table definition, the primary key clause specifies the partition key and optional clustering key. These keys uniquely identify each partition and row within a partition. See [Ring Architecture](https://docs.scylladb.com/manual/master/architecture/ringarchitecture/index.md).

<a id="term-Quorum"></a>

Quorum
: Quorum is a *global* consistency level setting across the entire cluster including all data centers. See [Consistency Levels](https://docs.scylladb.com/manual/master/cql/consistency.md).

<a id="term-Read-Amplification"></a>

Read Amplification
: Excessive read requests which require many SSTables. RA is calculated by the number of disk reads per query. High RA occurs when there are many pages to read in order to answer a query.  See [Compaction Strategies](https://docs.scylladb.com/manual/master/architecture/compaction/compaction-strategies.md).

<a id="term-Read-Operation"></a>

Read Operation
: A  read operation occurs when an application gets information from an SSTable and does not change that information in any way. See [Fault Tolerance](https://docs.scylladb.com/manual/master/architecture/architecture-fault-tolerance.md).

<a id="term-Read-Repair"></a>

Read Repair
: An anti-entropy mechanism for read operations ensuring that replicas are updated with most recently updated data. These repairs run automatically, asynchronously, and in the background. See [ScyllaDB Read Repair](https://docs.scylladb.com/manual/master/architecture/anti-entropy/read-repair.md).

<a id="term-Reconciliation"></a>

Reconciliation
: A verification phase during a data migration where the target data is compared against original source data to ensure that the migration architecture has transferred the data correctly. See [ScyllaDB Read Repair](https://docs.scylladb.com/manual/master/architecture/anti-entropy/read-repair.md).

<a id="term-Repair"></a>

Repair
: A process which runs in the background and synchronizes the data between nodes, so that eventually, all the replicas hold the same data. See [ScyllaDB Repair](https://docs.scylladb.com/manual/master/operating-scylla/procedures/maintenance/repair.md).

<a id="term-Repair-Based-Node-Operations-RBNO"></a>

Repair Based Node Operations (RBNO)
:  is an internal ScyllaDB mechanism that uses repair to
  synchronize data between the nodes in a cluster instead of using streaming. RBNO significantly
  improve database performance and data consistency.
  <br/>
  RBNO is enabled by default for a subset node operations.
  See [Repair Based Node Operations](https://docs.scylladb.com/manual/master/operating-scylla/procedures/cluster-management/repair-based-node-operation.md) for details.

<a id="term-Replication"></a>

Replication
: The process of replicating data across nodes in a cluster. See [Fault Tolerance](https://docs.scylladb.com/manual/master/architecture/architecture-fault-tolerance.md).

<a id="term-Replication-Factor-RF"></a>

Replication Factor (RF)
: The total number of replica nodes across a given cluster. An  of 1 means that the data will only exist on a single node in the cluster and will not have any fault tolerance. This number is a setting defined for each keyspace. All replicas share equal priority; there are no primary or master replicas. An RF for any table, can be defined for each . See [Fault Tolerance](https://docs.scylladb.com/manual/master/architecture/architecture-fault-tolerance.md).

<a id="term-Reshape"></a>

Reshape
: Rewrite a set of SSTables to satisfy a compaction strategy’s criteria. For example, restoring data from an old backup or before the strategy update.

<a id="term-Reshard"></a>

Reshard
: Splitting an SSTable, that is owned by more than one shard (core), into SSTables that are owned by a single shard. For example: when restoring data from a different server, importing SSTables from Apache Cassandra, or changing the number of cores in a machine (upscale).

<a id="term-RF-rack-valid-keyspace"></a>

RF-rack-valid keyspace
: A keyspace with [tablets](https://docs.scylladb.com/manual/master/architecture/tablets.md) enabled is RF-rack-valid if all of its data centers
  have the [Replication Factor (RF)](#term-Replication-Factor-RF), which is either a rack list, or numerical
  of value 0, 1, or the number of racks in that data center.
  <br/>
  Keyspaces with tablets disabled are always deemed RF-rack-valid, even if they do not satisfy the aforementioned condition.

<a id="term-Shard"></a>

Shard
: Each ScyllaDB node is internally split into *shards*, an independent thread bound to a dedicated core.
  Each shard of data is allotted CPU, RAM, persistent storage, and networking resources which it uses as efficiently as possible.
  See [ScyllaDB Shard per Core Architecture](https://www.scylladb.com/product/technology/shard-per-core-architecture/) for more information.

<a id="term-Shedding"></a>

Shedding
: Dropping requests to protect the system. This will occur if the request is too large or exceeds the max number of concurrent requests per shard.

<a id="term-Size-tiered-compaction-strategy"></a>

Size-tiered compaction strategy
: Triggers when the system has enough (four by default) similarly sized SSTables.  See [Compaction Strategies](https://docs.scylladb.com/manual/master/architecture/compaction/compaction-strategies.md).

<a id="term-Snapshot"></a>

Snapshot
: Snapshots in ScyllaDB are an essential part of the backup and restore mechanism. Whereas in other databases a backup starts with creating a copy of a data file (cold backup, hot backup, shadow copy backup), in ScyllaDB the process starts with creating a table or keyspace snapshot.  See [ScyllaDB Snapshots](https://docs.scylladb.com/manual/master/kb/snapshots.md).

<a id="term-Snitch"></a>

Snitch
: The mapping from the IP addresses of nodes to physical and virtual locations, such as racks and data centers. There are several types of snitches. The type of snitch affects the request routing mechanism. See [ScyllaDB Snitches](https://docs.scylladb.com/manual/master/operating-scylla/system-configuration/snitch.md).

<a id="term-Space-amplification"></a>

Space amplification
: Excessive disk space usage which requires that the disk be larger than a perfectly-compacted representation of the data (i.e., all the data in one single SSTable). SA is calculated as the ratio of the size of database files on a disk to the actual data size. High SA occurs when there is more disk space being used than the size of the data.  See [Compaction Strategies](https://docs.scylladb.com/manual/master/architecture/compaction/compaction-strategies.md).

<a id="term-SSTable"></a>

SSTable
: A concept borrowed from Google Big Table, SSTables or Sorted String Tables store a series of immutable rows where each row is identified by its row key.  See [Compaction Strategies](https://docs.scylladb.com/manual/master/architecture/compaction/compaction-strategies.md). The SSTable format is a persistent file format. See [ScyllaDB SSTable Format](https://docs.scylladb.com/manual/master/architecture/sstable/index.md).

<a id="term-Table"></a>

Table
: A collection of columns fetched by row. Columns are ordered by Clustering Key. See [Ring Architecture](https://docs.scylladb.com/manual/master/architecture/ringarchitecture/index.md).

<a id="term-Tablet"></a>

Tablet
: The name of a [Token Range](#term-Token-Range) in the Tablet Model </architecture/tablets> of assigning ownership of data in a cluster.

<a id="term-Time-window-compaction-strategy"></a>

Time-window compaction strategy
: TWCS is designed for time series data. See [Compaction Strategies](https://docs.scylladb.com/manual/master/architecture/compaction/compaction-strategies.md).

<a id="term-Token"></a>

Token
: A hash value calculated over the partition key of a table. All tokens calculated over any partition key of any table are part the same token domain. This allows unified assignment of partitions to nodes in a ScyllaDB cluster via using [Token Range](#term-Token-Range) as the basis of ownership assignment.

<a id="term-Token-Range"></a>

Token Range
: A contiguous range of [Token](#term-Token) values, the basis of ownership assignment in a ScyllaDB cluster. A token range is defined by a start and end token. Each node in a ScyllaDB cluster owns a number of token ranges.
  There are two models of distributing token ranges in the cluster, the [VNode Model](https://docs.scylladb.com/manual/master/architecture/ringarchitecture/index.md) and the Tablet Model </architecture/tablets>.

<a id="term-Tombstone"></a>

Tombstone
: A marker that indicates that data has been deleted. A large number of tombstones may impact read performance and disk usage, so an efficient tombstone garbage collection strategy should be employed. See [Tombstones GC options](https://docs.scylladb.com/manual/master/cql/ddl.md#ddl-tombstones-gc).

<a id="term-Tunable-Consistency"></a>

Tunable Consistency
: The possibility for unique, per-query, Consistency Level settings. These are incremental and override fixed database settings intended to enforce data consistency. Such settings may be set directly from a CQL statement when response speed for a given query or operation is more important. See [Fault Tolerance](https://docs.scylladb.com/manual/master/architecture/architecture-fault-tolerance.md).

<a id="term-Virtual-node"></a>

Virtual node
: A range of tokens owned by a single ScyllaDB node. ScyllaDB nodes are configurable and support a set of . In legacy token selection, a node owns one token (or token range) per node. With Vnodes, a node can own many tokens or token ranges; within a cluster, these may be selected randomly from a non-contiguous set. In a Vnode configuration, each token falls within a specific token range which in turn is represented as a Vnode. Each Vnode is then allocated to a physical node in the cluster. See [Ring Architecture](https://docs.scylladb.com/manual/master/architecture/ringarchitecture/index.md).

<a id="term-Workload"></a>

Workload
: A database category that allows you to manage different sources of database activities, such as requests or administrative activities. By defining workloads, you can specify how ScyllaDB will process those activities. For example, ScyllaDB
  ships with a feature that allows you to prioritize one workload over another (e.g., user requests over administrative activities). See [Workload Prioritization](https://docs.scylladb.com/manual/master/features/workload-prioritization.md).

<a id="term-Write-Amplification"></a>

Write Amplification
: Excessive compaction of the same data.  is calculated by the ratio of bytes written to storage versus bytes written to the database. High WA occurs when there are more bytes/second written to storage than are actually written to the database. See [Compaction Strategies](https://docs.scylladb.com/manual/master/architecture/compaction/compaction-strategies.md).

<a id="term-Write-Operation"></a>

Write Operation
: A write operation occurs when information is added or removed from an SSTable. See [Fault Tolerance](https://docs.scylladb.com/manual/master/architecture/architecture-fault-tolerance.md).
