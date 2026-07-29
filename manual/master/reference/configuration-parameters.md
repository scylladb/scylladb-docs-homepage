# Configuration Parameters

This section contains a list of properties that can be configured in `scylla.yaml` - the main configuration file for ScyllaDB.
In addition, properties that support live updates (liveness) can be updated via the `system.config` virtual table or the [REST API](https://docs.scylladb.com/manual/master/operating-scylla/rest.md).

Live update means that parameters can be modified dynamically while the server
is running. If `liveness` of a parameter is set to `true`, sending the `SIGHUP`
signal to the server processes will trigger ScyllaDB to re-read its configuration
and override the current configuration with the new value.

**Configuration Precedence**

As the parameters can be configured in more than one place, ScyllaDB applies them
in the following order with `scylla.yaml` parameters updated via `SIGHUP`
having the highest priority:

1. Live update via `scylla.yaml` (with `SIGHUP`) or REST API
2. `system.config` table
3. command line options
4. `scylla.yaml`

<!-- -*- mode: rst -*- -->

<a id="confgroup-initialization-properties"></a>

## Initialization properties

> The minimal properties needed for configuring a cluster.

<a id="confprop-cluster-name"></a>

### cluster_name

> The name of the cluster; used to prevent machines in one logical cluster from joining another. All nodes participating in a cluster must have the same value.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-listen-address"></a>

### listen_address

> The IP address or hostname that Scylla binds to for connecting to other Scylla nodes. You must change the default setting for multiple nodes to communicate. Do not set to 0.0.0.0, unless you have set broadcast_address to an address that other nodes can use to reach this node.

> * **Type:** `sstring`
> * **Default value:** `"localhost"`
> * Liveness: `False`

<a id="confprop-listen-interface-prefer-ipv6"></a>

### listen_interface_prefer_ipv6

> If you choose to specify the interface by name and the interface has an ipv4 and an ipv6 address    you can specify which should be chosen using listen_interface_prefer_ipv6. If false the first ipv4    address will be used. If true the first ipv6 address will be used. Defaults to false preferring    ipv4. If there is only one address it will be selected regardless of ipv4/ipv6.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confgroup-default-directories"></a>

## Default directories

> If you have changed any of the default directories during installation, make sure you have root access and set these properties.

<a id="confprop-workdir-w"></a>

### workdir,W

> The directory in which Scylla will put all its subdirectories. The location of individual subdirs can be overridden by the respective \`\`\*_directory\`\` options.

> * **Default value:** `"/var/lib/scylla"`
> * Liveness: `False`

<a id="confprop-commitlog-directory"></a>

### commitlog_directory

> The directory where the commit log is stored. For optimal write performance, it is recommended the commit log be on a separate disk partition (ideally, a separate physical device) from the data file directories.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-schema-commitlog-directory"></a>

### schema_commitlog_directory

> The directory where the schema commit log is stored. This is a special commitlog instance used for schema and system tables. For optimal write performance, it is recommended the commit log be on a separate disk partition (ideally, a separate physical device) from the data file directories.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-data-file-directories"></a>

### data_file_directories

> The directory location where table data (SSTables) is stored.

> * **Type:** `string_list`
> * **Default value:** `{ }`
> * Liveness: `False`

<a id="confprop-data-file-capacity"></a>

### data_file_capacity

> Total capacity in bytes for storing data files. Used by tablet load balancer to compute storage utilization.     If not set, will use file system’s capacity.

> * **Type:** `uint64_t`
> * **Default value:** `0`
> * Liveness: `True`

<a id="confprop-hints-directory"></a>

### hints_directory

> The directory where hints files are stored if hinted handoff is enabled.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-view-hints-directory"></a>

### view_hints_directory

> The directory where materialized-view updates are stored while a view replica is unreachable.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-logstor-directory"></a>

### logstor_directory

> The directory where data files for logstor storage are stored.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confgroup-common-initialization-properties"></a>

## Common initialization properties

> Be sure to set the properties in the Quick start section as well.

<a id="confprop-endpoint-snitch"></a>

### endpoint_snitch

> Set to a class that implements the IEndpointSnitch. Scylla uses snitches for locating nodes and routing requests.
> : * SimpleSnitch: Use for single-data center deployments or single-zone in public clouds. Does not recognize data center or rack information. It treats strategy order as proximity, which can improve cache locality when disabling read repair.
>   * GossipingPropertyFileSnitch: Recommended for production. The rack and data center for the local node are defined in the cassandra-rackdc.properties file and propagated to other nodes via gossip. To allow migration from the PropertyFileSnitch, it uses the cassandra-topology.properties file if it is present.
>   * Ec2Snitch: For EC2 deployments in a single region. Loads region and availability zone information from the EC2 API. The region is treated as the data center and the availability zone as the rack. Uses only private IPs. Subsequently it does not work across multiple regions.
>   * Ec2MultiRegionSnitch: Uses public IPs as the broadcast_address to allow cross-region connectivity. This means you must also set seed addresses to the public IP and open the storage_port or ssl_storage_port on the public IP firewall. For intra-region traffic, Scylla switches to the private IP after establishing a connection.
>   * GoogleCloudSnitch: For deployments on Google Cloud Platform across one or more regions. The region is treated as a datacenter and the availability zone is treated as a rack within the datacenter. The communication should occur over private IPs within the same logical network.
>   * RackInferringSnitch: Proximity is determined by rack and data center, which are assumed to correspond to the 3rd and 2nd octet of each node’s IP address, respectively. This snitch is best used as an example for writing a custom snitch class (unless this happens to match your deployment conventions).
>   <br/>
>   Related information: Snitches

> * **Type:** `sstring`
> * **Default value:** `"org.apache.cassandra.locator.SimpleSnitch"`
> * Liveness: `False`

<a id="confprop-rpc-address"></a>

### rpc_address

> The listen address for client connections (native transport).Valid values are:
> : * unset: Resolves the address using the hostname configuration of the node. If left unset, the hostname must resolve to the IP address of this node using /etc/hostname, /etc/hosts, or DNS.
>   * 0.0.0.0: Listens on all configured interfaces, but you must set the broadcast_rpc_address to a value other than 0.0.0.0.
>   * IP address
>   * hostname
>   <br/>
>   Related information: Network

> * **Type:** `sstring`
> * **Default value:** `"localhost"`
> * Liveness: `False`

<a id="confprop-rpc-interface-prefer-ipv6"></a>

### rpc_interface_prefer_ipv6

> If you choose to specify the interface by name and the interface has an ipv4 and an ipv6 address    you can specify which should be chosen using rpc_interface_prefer_ipv6. If false the first ipv4    address will be used. If true the first ipv6 address will be used. Defaults to false preferring    ipv4. If there is only one address it will be selected regardless of ipv4/ipv6.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-seed-provider"></a>

### seed_provider

> The addresses of hosts deemed contact points. Scylla nodes use the -seeds list to find each other and learn the topology of the ring.

> > > * class_name (Default: org.apache.cassandra.locator.SimpleSeedProvider): The class within Scylla that handles the seed logic. It can be customized, but this is typically not required.
> > > * seeds (Default: 127.0.0.1): A comma-delimited list of IP addresses used by gossip for bootstrapping new nodes joining a cluster. When running multiple nodes, you must change the list from the default value. In multiple data-center clusters, the seed list should include at least one node from each data center (replication group). More than a single seed node per data center is recommended for fault tolerance. Otherwise, gossip has to communicate with another data center when bootstrapping a node. Making every node a seed node is not recommended because of increased maintenance and reduced gossip performance. Gossip optimization is not critical, but it is recommended to use a small seed list (approximately three nodes per data center).

> > Related information: Initializing a multiple node cluster (single data center) and Initializing a multiple node cluster (multiple data centers).
> * **Type:** `seed_provider_type`
> * **Default value:** `seed_provider_type("org.apache.cassandra.locator.SimpleSeedProvider")`
> * Liveness: `False`

<a id="confgroup-common-compaction-settings"></a>

## Common compaction settings

> Be sure to set the properties in the Quick start section as well.

<a id="confprop-compaction-throughput-mb-per-sec"></a>

### compaction_throughput_mb_per_sec

> Throttles compaction to the specified total throughput across the entire system. The faster you insert data, the faster you need to compact in order to keep the SSTable count down. The recommended Value is 16 to 32 times the rate of write throughput (in MBs/second). Setting the value to 0 disables compaction throttling.

> > Related information: Configuring compaction
> * **Type:** `uint32_t`
> * **Default value:** `0`
> * Liveness: `True`

<a id="confprop-compaction-large-partition-warning-threshold-mb"></a>

### compaction_large_partition_warning_threshold_mb

> Log a warning when writing partitions larger than this value.

> * **Type:** `uint32_t`
> * **Default value:** `1000`
> * Liveness: `True`

<a id="confprop-compaction-large-row-warning-threshold-mb"></a>

### compaction_large_row_warning_threshold_mb

> Log a warning when writing rows larger than this value.

> * **Type:** `uint32_t`
> * **Default value:** `10`
> * Liveness: `True`

<a id="confprop-compaction-large-cell-warning-threshold-mb"></a>

### compaction_large_cell_warning_threshold_mb

> Log a warning when writing cells larger than this value.

> * **Type:** `uint32_t`
> * **Default value:** `1`
> * Liveness: `True`

<a id="confprop-large-cell-fail-threshold-mb"></a>

### large_cell_fail_threshold_mb

> Reject writes with cell value size exceeding this threshold in MB. Set to 0 to disable.

> * **Type:** `uint32_t`
> * **Default value:** `2`
> * Liveness: `True`

<a id="confprop-large-data-cql-warnings"></a>

### large_data_cql_warnings

> When true, soft limit violations detected by the coordinator-side large data guardrail check are reported to the     client as CQL warnings in the response frame. When false, this behavior is suppressed (only server-side logging is     performed).

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confprop-large-partition-fail-threshold-mb"></a>

### large_partition_fail_threshold_mb

> Reject writes targeting a partition whose on-disk size already exceeds this threshold in MB, as recorded in any SSTable’s large data records.     Set to 0 to disable.

> * **Type:** `uint32_t`
> * **Default value:** `2000`
> * Liveness: `True`

<a id="confprop-rows-count-fail-threshold"></a>

### rows_count_fail_threshold

> Reject writes targeting a partition whose on-disk row count already exceeds this threshold, as recorded in any SSTable’s large data records.     Set to 0 to disable.

> * **Type:** `uint32_t`
> * **Default value:** `200000`
> * Liveness: `True`

<a id="confprop-large-row-fail-threshold-mb"></a>

### large_row_fail_threshold_mb

> Reject writes targeting a partition that contains any row whose on-disk size already exceeds this threshold in MB, as recorded in any SSTable’s large data records.     Set to 0 to disable.

> * **Type:** `uint32_t`
> * **Default value:** `20`
> * Liveness: `True`

<a id="confprop-large-collection-elements-fail-threshold"></a>

### large_collection_elements_fail_threshold

> Reject writes targeting a partition that contains any collection whose element count already exceeds this threshold, as recorded in any SSTable’s large data records.     Set to 0 to disable.

> * **Type:** `uint32_t`
> * **Default value:** `20000`
> * Liveness: `True`

<a id="confprop-compaction-rows-count-warning-threshold"></a>

### compaction_rows_count_warning_threshold

> Log a warning when writing a number of rows larger than this value.

> * **Type:** `uint32_t`
> * **Default value:** `100000`
> * Liveness: `True`

<a id="confprop-compaction-collection-elements-count-warning-threshold"></a>

### compaction_collection_elements_count_warning_threshold

> Log a warning when writing a collection containing more elements than this value.

> * **Type:** `uint32_t`
> * **Default value:** `10000`
> * Liveness: `True`

<a id="confprop-compaction-large-data-records-per-sstable"></a>

### compaction_large_data_records_per_sstable

> Maximum number of large data records per type to store in each SSTable’s scylla metadata.

> * **Type:** `uint32_t`
> * **Default value:** `10`
> * Liveness: `True`

<a id="confgroup-common-automatic-backup-settings"></a>

## Common automatic backup settings

<a id="confprop-incremental-backups"></a>

### incremental_backups

> Backs up data updated since the last snapshot was taken. When enabled, Scylla creates a hard link to each SSTable flushed or streamed locally in a backups/ subdirectory of the keyspace data. Removing these links is the operator’s responsibility.

> > Related information: Enabling incremental backups
> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confgroup-common-fault-detection-setting"></a>

## Common fault detection setting

<a id="confprop-phi-convict-threshold"></a>

### phi_convict_threshold

> Adjusts the sensitivity of the failure detector on an exponential scale. Generally this setting never needs adjusting.

> > Related information: Failure detection and recovery
> * **Type:** `uint32_t`
> * **Default value:** `8`
> * Liveness: `False`

<a id="confprop-failure-detector-timeout-in-ms"></a>

### failure_detector_timeout_in_ms

> Maximum time between two successful echo message before gossip mark a node down in milliseconds.

> * **Type:** `uint32_t`
> * **Default value:** `20 * 1000`
> * Liveness: `True`

<a id="confprop-direct-failure-detector-ping-timeout-in-ms"></a>

### direct_failure_detector_ping_timeout_in_ms

> Duration after which the direct failure detector aborts a ping message, so the next ping can start.
> : Note: this failure detector is used by Raft, and is different from gossiper’s failure detector (configured by \`failure_detector_timeout_in_ms\`).

> * **Type:** `uint32_t`
> * **Default value:** `600`
> * Liveness: `False`

<a id="confgroup-commit-log-settings"></a>

## Commit log settings

<a id="confprop-commitlog-sync"></a>

### commitlog_sync

> The method that Scylla uses to acknowledge writes in milliseconds:
> : * periodic: Used with commitlog_sync_period_in_ms (Default: 10000 - 10 seconds ) to control how often the commit log is synchronized to disk. Periodic syncs are acknowledged immediately.
>   * batch: Used with commitlog_sync_batch_window_in_ms (Default: disabled \`\`\*\*\`\`) to control how long Scylla waits for other writes before performing a sync. When using this method, writes are not acknowledged until fsynced to disk.
>   <br/>
>   Related information: Durability

> * **Type:** `sstring`
> * **Default value:** `"periodic"`
> * Liveness: `False`

<a id="confprop-commitlog-segment-size-in-mb"></a>

### commitlog_segment_size_in_mb

> Sets the size of the individual commitlog file segments. A commitlog segment may be archived, deleted, or recycled after all its data has been flushed to SSTables. This amount of data can potentially include commitlog segments from every table in the system. The default size is usually suitable for most commitlog archiving, but if you want a finer granularity, 8 or 16 MB is reasonable. See Commit log archive configuration.

> > Related information: Commit log archive configuration
> * **Type:** `uint32_t`
> * **Default value:** `64`
> * Liveness: `False`

<a id="confprop-schema-commitlog-segment-size-in-mb"></a>

### schema_commitlog_segment_size_in_mb

> Sets the size of the individual schema commitlog file segments. The default size is larger than the default size of the data commitlog because the segment size puts a limit on the mutation size that can be written at once, and some schema mutation writes are much larger than average.

> > Related information: Commit log archive configuration
> * **Type:** `uint32_t`
> * **Default value:** `128`
> * Liveness: `False`

<a id="confprop-commitlog-sync-period-in-ms"></a>

### commitlog_sync_period_in_ms

> Controls how long the system waits for other writes before performing a sync in \`\`periodic\`\` mode.

> * **Type:** `uint32_t`
> * **Default value:** `10000`
> * Liveness: `False`

<a id="confprop-commitlog-sync-batch-window-in-ms"></a>

### commitlog_sync_batch_window_in_ms

> Controls how long the system waits for other writes before performing a sync in \`\`batch\`\` mode.

> * **Type:** `uint32_t`
> * **Default value:** `10000`
> * Liveness: `False`

<a id="confprop-commitlog-max-data-lifetime-in-seconds"></a>

### commitlog_max_data_lifetime_in_seconds

> Controls how long data remains in commit log before the system tries to evict it to sstable, regardless of usage pressure. (0 disables)

> * **Type:** `uint32_t`
> * **Default value:** `24*60*60`
> * Liveness: `True`

<a id="confprop-commitlog-total-space-in-mb"></a>

### commitlog_total_space_in_mb

> Total space used for commitlogs. If the used space goes above this value, Scylla rounds up to the next nearest segment multiple and flushes memtables to disk for the oldest commitlog segments, removing those log segments. This reduces the amount of data to replay on startup, and prevents infrequently-updated tables from indefinitely keeping commitlog segments. A small total commitlog space tends to cause more flush activity on less-active tables.

> > Related information: Configuring memtable throughput
> * **Type:** `int64_t`
> * **Default value:** `-1`
> * Liveness: `False`

<a id="confprop-commitlog-flush-threshold-in-mb"></a>

### commitlog_flush_threshold_in_mb

> Threshold for commitlog disk usage. When used disk space goes above this value, Scylla initiates flushes of memtables to disk for the oldest commitlog segments, removing those log segments. Adjusting this affects disk usage vs. write latency. Default is (approximately) commitlog_total_space_in_mb - <num shards>\*commitlog_segment_size_in_mb.

> * **Type:** `int64_t`
> * **Default value:** `-1`
> * Liveness: `False`

<a id="confprop-commitlog-use-o-dsync"></a>

### commitlog_use_o_dsync

> Whether or not to use O_DSYNC mode for commitlog segments IO. Can improve commitlog latency on some file systems.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-commitlog-use-fragmented-entries"></a>

### commitlog_use_fragmented_entries

> Whether or not to allow commitlog entries to fragment across segments, allowing for larger entry sizes.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confgroup-compaction-settings"></a>

## Compaction settings

> Related information: Configuring compaction

<a id="confprop-defragment-memory-on-idle"></a>

### defragment_memory_on_idle

> When set to true, will defragment memory when the cpu is idle.  This reduces the amount of work Scylla performs when processing client requests.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confgroup-memtable-settings"></a>

## Memtable settings

<a id="confprop-logstor-disk-size-in-mb"></a>

### logstor_disk_size_in_mb

> Total size in megabytes allocated for logstor storage on disk.

> * **Type:** `uint32_t`
> * **Default value:** `0`
> * Liveness: `False`

<a id="confprop-logstor-file-size-in-mb"></a>

### logstor_file_size_in_mb

> Total size in megabytes allocated for each logstor data file on disk.

> * **Type:** `uint32_t`
> * **Default value:** `32`
> * Liveness: `False`

<a id="confprop-logstor-format-on-startup"></a>

### logstor_format_on_startup

> Controls when logstor data files are formatted. When enabled, all logstor files are formatted during node startup, which increases startup time but ensures optimal write performance immediately after startup.     When disabled, logstor files are formatted lazily on first write, which reduces startup time but may cause slightly degraded write performance on first access to each file.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-logstor-separator-delay-limit-ms"></a>

### logstor_separator_delay_limit_ms

> Maximum delay in milliseconds for logstor separator debt control.

> * **Type:** `uint32_t`
> * **Default value:** `100`
> * Liveness: `False`

<a id="confprop-logstor-separator-max-memory-in-mb"></a>

### logstor_separator_max_memory_in_mb

> Maximum memory in megabytes for logstor separator memory buffers.

> * **Type:** `uint32_t`
> * **Default value:** `256`
> * Liveness: `False`

<a id="confgroup-cache-and-index-settings"></a>

## Cache and index settings

<a id="confprop-column-index-size-in-kb"></a>

### column_index_size_in_kb

> Granularity of the index of rows within a partition. For huge rows, decrease this setting to improve seek time. If you use key cache, be careful not to make this setting too large because key cache will be overwhelmed. If you’re unsure of the size of the rows, it’s best to use the default setting.

> * **Type:** `uint32_t`
> * **Default value:** `64`
> * Liveness: `False`

<a id="confprop-column-index-auto-scale-threshold-in-kb"></a>

### column_index_auto_scale_threshold_in_kb

> Auto-reduce the promoted index granularity by half when reaching this threshold, to prevent promoted index bloating due to partitions with too many rows. Set to 0 to disable this feature.

> * **Type:** `uint32_t`
> * **Default value:** `10240`
> * Liveness: `True`

<a id="confgroup-disks-settings"></a>

## Disks settings

<a id="confprop-stream-io-throughput-mb-per-sec"></a>

### stream_io_throughput_mb_per_sec

> Throttles streaming I/O to the specified total throughput (in MiBs/s) across the entire system. Streaming I/O includes the one performed by repair and both RBNO and legacy topology operations such as adding or removing a node. Setting the value to 0 disables stream throttling. It is recommended to set the value for this parameter to be 75% of network bandwidth

> * **Type:** `uint32_t`
> * **Default value:** `0`
> * Liveness: `True`

<a id="confprop-stream-plan-ranges-fraction"></a>

### stream_plan_ranges_fraction

> Specify the fraction of ranges to stream in a single stream plan. Value is between 0 and 1.

> * **Type:** `double`
> * **Default value:** `0.1`
> * Liveness: `True`

<a id="confprop-enable-file-stream"></a>

### enable_file_stream

> Set true to use file based stream for tablet instead of mutation based stream

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confgroup-advanced-initialization-properties"></a>

## Advanced initialization properties

> Properties for advanced users or properties that are less commonly used.

<a id="confprop-auto-bootstrap"></a>

### auto_bootstrap

> This setting has been removed from default configuration. It makes new (non-seed) nodes automatically migrate the right data to themselves. Do not set this to false unless you really know what you are doing.
> : Related information: Initializing a multiple node cluster (single data center) and Initializing a multiple node cluster (multiple data centers).

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-batch-size-warn-threshold-in-kb"></a>

### batch_size_warn_threshold_in_kb

> Log WARN on any batch size exceeding this value in kilobytes. Caution should be taken on increasing the size of this threshold as it can lead to node instability.

> * **Type:** `uint32_t`
> * **Default value:** `128`
> * Liveness: `False`

<a id="confprop-batch-size-fail-threshold-in-kb"></a>

### batch_size_fail_threshold_in_kb

> Fail any multiple-partition batch exceeding this value. 1 MiB (8x warn threshold) by default.

> * **Type:** `uint32_t`
> * **Default value:** `1024`
> * Liveness: `False`

<a id="confprop-broadcast-address"></a>

### broadcast_address

> The IP address a node tells other nodes in the cluster to contact it by. It allows public and private address to be different. For example, use the broadcast_address parameter in topologies where not all nodes have access to other nodes by their private IP addresses.
> : If your Scylla cluster is deployed across multiple Amazon EC2 regions and you use the EC2MultiRegionSnitch , set the broadcast_address to public IP address of the node and the listen_address to the private IP.

> * **Type:** `sstring`
> * **Default value:** `{}`
> * Liveness: `False`

<a id="confprop-listen-on-broadcast-address"></a>

### listen_on_broadcast_address

> When using multiple physical network interfaces, set this to true to listen on broadcast_address in addition to the listen_address, allowing nodes to communicate in both interfaces.  Ignore this property if the network configuration automatically routes between the public and private networks such as EC2.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-initial-token"></a>

### initial_token

> Used in the single-node-per-token architecture, where a node owns exactly one contiguous range in the ring space. Setting this property overrides num_tokens.
> : If you not using vnodes or have num_tokens set it to 1 or unspecified (#num_tokens), you should always specify this parameter when setting up a production cluster for the first time and when adding capacity. For more information, see this parameter in the Cassandra 1.1 Node and Cluster Configuration documentation.
>   This parameter can be used with num_tokens (vnodes) in special cases such as Restoring from a snapshot.

> * **Type:** `sstring`
> * **Default value:** `{}`
> * Liveness: `False`

<a id="confprop-num-tokens"></a>

### num_tokens

> Defines the number of tokens randomly assigned to this node on the ring when using virtual nodes (vnodes). The more tokens, relative to other nodes, the larger the proportion of data that the node stores. Generally all nodes should have the same number of tokens assuming equal hardware capability. The recommended value is 256. If unspecified (#num_tokens), Scylla uses 1 (equivalent to #num_tokens
> : If not using vnodes, comment #num_tokens : 256 or set num_tokens : 1 and use initial_token. If you already have an existing cluster with one token per node and wish to migrate to vnodes, see Enabling virtual nodes on an existing production cluster.
>   <br/>
>   #### NOTE
>   If using DataStax Enterprise, the default setting of this property depends on the type of node and type of install.

> * **Type:** `uint32_t`
> * **Default value:** `1`
> * Liveness: `False`

<a id="confprop-partitioner"></a>

### partitioner

> Distributes rows (by partition key) across all nodes in the cluster. At the moment, only Murmur3Partitioner is supported. For new clusters use the default partitioner.

> > Related information: Partitioners
> * **Type:** `sstring`
> * **Default value:** `"org.apache.cassandra.dht.Murmur3Partitioner"`
> * Liveness: `False`

<a id="confprop-storage-port"></a>

### storage_port

> The port for inter-node communication.

> * **Type:** `uint16_t`
> * **Default value:** `7000`
> * Liveness: `False`

<a id="confgroup-advanced-automatic-backup-setting"></a>

## Advanced automatic backup setting

<a id="confprop-auto-snapshot"></a>

### auto_snapshot

> Enable or disable whether a snapshot is taken of the data before keyspace truncation or dropping of tables. To prevent data loss, using the default setting is strongly advised. If you set to false, you will lose data on truncation or drop.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confprop-auto-snapshot-ttl"></a>

### auto_snapshot_ttl

> The time-to-live (TTL) for automatic snapshots in seconds. A value of 0 means snapshots are kept indefinitely.

> * **Type:** `uint32_t`
> * **Default value:** `0`
> * Liveness: `True`

<a id="confgroup-tombstone-settings"></a>

## Tombstone settings

> When executing a scan, within or across a partition, tombstones must be kept in memory to allow returning them to the coordinator. The coordinator uses them to ensure other replicas know about the deleted rows. Workloads that generate numerous tombstones may cause performance problems and exhaust the server heap. See Cassandra anti-patterns: Queues and queue-like datasets. Adjust these thresholds only if you understand the impact and want to scan more tombstones. Additionally, you can adjust these thresholds at runtime using the StorageServiceMBean.   Related information: Cassandra anti-patterns: Queues and queue-like datasets.

<a id="confprop-tombstone-warn-threshold"></a>

### tombstone_warn_threshold

> The maximum number of tombstones a query can scan before warning. Tombstone warnings are only logged for single-partition queries.     Tombstone logs for range-scans are logged with debug level (querier logger), as it is normal for range-scans to go through many tombstones.

> * **Type:** `uint32_t`
> * **Default value:** `1000`
> * Liveness: `False`

<a id="confprop-query-tombstone-page-limit"></a>

### query_tombstone_page_limit

> The number of tombstones after which a query cuts a page, even if not full or even empty.

> * **Type:** `uint64_t`
> * **Default value:** `10000`
> * Liveness: `True`

<a id="confprop-query-page-size-in-bytes"></a>

### query_page_size_in_bytes

> The size of pages in bytes, after a page accumulates this much data, the page is cut and sent to the client.     Setting a too large value increases the risk of OOM.

> * **Type:** `uint64_t`
> * **Default value:** `1 << 20`
> * Liveness: `True`

<a id="confprop-group0-tombstone-gc-refresh-interval-in-ms"></a>

### group0_tombstone_gc_refresh_interval_in_ms

> The interval in milliseconds at which we update the time point for safe tombstone expiration in group0 tables.

> * **Type:** `uint32_t`
> * **Default value:** `std::chrono::duration_cast<std::chrono::milliseconds>(60min).count()`
> * Liveness: `False`

<a id="confgroup-network-timeout-settings"></a>

## Network timeout settings

<a id="confprop-range-request-timeout-in-ms"></a>

### range_request_timeout_in_ms

> The time in milliseconds that the coordinator waits for sequential or index scans to complete.

> * **Type:** `uint32_t`
> * **Default value:** `10000`
> * Liveness: `True`

<a id="confprop-read-request-timeout-in-ms"></a>

### read_request_timeout_in_ms

> The time that the coordinator waits for read operations to complete

> * **Type:** `uint32_t`
> * **Default value:** `5000`
> * Liveness: `True`

<a id="confprop-counter-write-request-timeout-in-ms"></a>

### counter_write_request_timeout_in_ms

> The time that the coordinator waits for counter writes to complete.

> * **Type:** `uint32_t`
> * **Default value:** `5000`
> * Liveness: `True`

<a id="confprop-cas-contention-timeout-in-ms"></a>

### cas_contention_timeout_in_ms

> The time that the coordinator continues to retry a CAS (compare and set) operation that contends with other proposals for the same row.

> * **Type:** `uint32_t`
> * **Default value:** `1000`
> * Liveness: `True`

<a id="confprop-truncate-request-timeout-in-ms"></a>

### truncate_request_timeout_in_ms

> The time that the coordinator waits for truncates (remove all data from a table) to complete. The long default value allows for a snapshot to be taken before removing the data. If auto_snapshot is disabled (not recommended), you can reduce this time.

> * **Type:** `uint32_t`
> * **Default value:** `60000`
> * Liveness: `True`

<a id="confprop-write-request-timeout-in-ms"></a>

### write_request_timeout_in_ms

> The time in milliseconds that the coordinator waits for write operations to complete.

> > Related information: About hinted handoff writes
> * **Type:** `uint32_t`
> * **Default value:** `2000`
> * Liveness: `True`

<a id="confprop-request-timeout-in-ms"></a>

### request_timeout_in_ms

> The default timeout for other, miscellaneous operations.

> > Related information: About hinted handoff writes
> * **Type:** `uint32_t`
> * **Default value:** `10000`
> * Liveness: `True`

<a id="confprop-request-timeout-on-shutdown-in-seconds"></a>

### request_timeout_on_shutdown_in_seconds

> Timeout for CQL server requests on shutdown. After this timeout the server will shutdown all connections.

> * **Type:** `uint32_t`
> * **Default value:** `30`
> * Liveness: `False`

<a id="confprop-group0-raft-op-timeout-in-ms"></a>

### group0_raft_op_timeout_in_ms

> The time in milliseconds that group0 allows a Raft operation to complete.

> * **Type:** `uint32_t`
> * **Default value:** `60000`
> * Liveness: `True`

<a id="confgroup-inter-node-settings"></a>

## Inter-node settings

<a id="confprop-internode-compression"></a>

### internode_compression

> Controls whether traffic between nodes is compressed. The valid values are:
> : * all: All traffic is compressed.
>   * dc : Traffic between data centers is compressed.
>   * rack : Traffic between racks is compressed.
>   * none : No compression.

> * **Type:** `sstring`
> * **Default value:** `"none"`
> * Liveness: `False`

<a id="confprop-internode-compression-zstd-max-cpu-fraction"></a>

### internode_compression_zstd_max_cpu_fraction

> ZSTD compression of RPC will consume at most this fraction of each internode_compression_zstd_quota_refresh_period_ms time slice.
> : If you wish to try out zstd for RPC compression, 0.05 is a reasonable starting point.

> * **Type:** `float`
> * **Default value:** `0.000`
> * Liveness: `True`

<a id="confprop-internode-compression-zstd-cpu-quota-refresh-period-ms"></a>

### internode_compression_zstd_cpu_quota_refresh_period_ms

> Advanced. ZSTD compression of RPC will consume at most internode_compression_zstd_max_cpu_fraction (plus one message) of in each time slice of this length.

> * **Type:** `uint32_t`
> * **Default value:** `20`
> * Liveness: `True`

<a id="confprop-internode-compression-zstd-max-longterm-cpu-fraction"></a>

### internode_compression_zstd_max_longterm_cpu_fraction

> ZSTD compression of RPC will consume at most this fraction of each internode_compression_zstd_longterm_cpu_quota_refresh_period_ms time slice.

> * **Type:** `float`
> * **Default value:** `1.000`
> * Liveness: `True`

<a id="confprop-internode-compression-zstd-longterm-cpu-quota-refresh-period-ms"></a>

### internode_compression_zstd_longterm_cpu_quota_refresh_period_ms

> Advanced. ZSTD compression of RPC will consume at most internode_compression_zstd_max_longterm_cpu_fraction (plus one message) of in each time slice of this length.

> * **Type:** `uint32_t`
> * **Default value:** `10000`
> * Liveness: `True`

<a id="confprop-internode-compression-zstd-min-message-size"></a>

### internode_compression_zstd_min_message_size

> Minimum RPC message size which can be compressed with ZSTD. Messages smaller than this threshold will always be compressed with LZ4.     ZSTD has high per-message overhead, and might be a bad choice for small messages. This knob allows for some experimentation with that.

> * **Type:** `uint32_t`
> * **Default value:** `1024`
> * Liveness: `True`

<a id="confprop-internode-compression-zstd-max-message-size"></a>

### internode_compression_zstd_max_message_size

> Maximum RPC message size which can be compressed with ZSTD. RPC messages might be large, but they are always compressed at once. This might cause reactor stalls.     If this happens, this option can be used to make the stalls less severe.

> * **Type:** `uint32_t`
> * **Default value:** `std::numeric_limits<uint32_t>::max()`
> * Liveness: `True`

<a id="confprop-internode-compression-checksumming"></a>

### internode_compression_checksumming

> Computes and checks checksums for compressed RPC frames. This is a paranoid precaution against corruption bugs in the compression protocol.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confprop-internode-compression-algorithms"></a>

### internode_compression_algorithms

> Specifies RPC compression algorithms supported by this node.

> * **Type:** `netw::advanced_rpc_compressor::tracker::algo_config`
> * **Default value:** `{ netw::compression_algorithm::type::ZSTD, netw::compression_algorithm::type::LZ4, }`
> * Liveness: `True`

<a id="confprop-internode-compression-enable-advanced"></a>

### internode_compression_enable_advanced

> Enables the new implementation of RPC compression. If disabled, Scylla will fall back to the old implementation.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-rpc-dict-training-when"></a>

### rpc_dict_training_when

> Specifies when RPC compression dictionary training is performed by this node.
> : * \`never\` disables it unconditionally.
>   * \`when_leader\` enables it only whenever the node is the Raft leader.
>   * \`always\` (not recommended) enables it unconditionally.
>   <br/>
>   Training shouldn’t be enabled on more than one node at a time, because overly-frequent dictionary announcements might indefinitely delay nodes from agreeing on a new dictionary.

> * **Type:** `enum_option<netw::dict_training_loop::when>`
> * **Default value:** `netw::dict_training_loop::when::type::NEVER`
> * Liveness: `True`

<a id="confprop-rpc-dict-training-min-time-seconds"></a>

### rpc_dict_training_min_time_seconds

> Specifies the minimum duration of RPC compression dictionary training.

> * **Type:** `uint32_t`
> * **Default value:** `3600`
> * Liveness: `True`

<a id="confprop-rpc-dict-training-min-bytes"></a>

### rpc_dict_training_min_bytes

> Specifies the minimum volume of RPC compression dictionary training.

> * **Type:** `uint64_t`
> * **Default value:** `1'000'000'000`
> * Liveness: `True`

<a id="confprop-inter-dc-tcp-nodelay"></a>

### inter_dc_tcp_nodelay

> Enable or disable tcp_nodelay for inter-data center communication. When disabled larger, but fewer, network packets are sent. This reduces overhead from the TCP protocol itself. However, if cross data-center responses are blocked, it will increase latency.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confgroup-native-transport-cql-binary-protocol"></a>

## Native transport (CQL Binary Protocol)

<a id="confprop-start-native-transport"></a>

### start_native_transport

> Enable or disable the native transport server. Uses the same address as the rpc_address, but the port is different from the rpc_port. See native_transport_port.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-native-transport-port"></a>

### native_transport_port

> Port on which the CQL native transport listens for clients.

> * **Type:** `uint16_t`
> * **Default value:** `9042`
> * Liveness: `False`

<a id="confprop-maintenance-socket"></a>

### maintenance_socket

> The Unix Domain Socket the node uses for maintenance socket.
> : The possible options are:
>   <br/>
>   > ignore         the node will not open the maintenance socket.
>   <br/>
>   > workdir        the node will open the maintenance socket on the path <scylla’s workdir>/cql.m,
>   <br/>
>   > > where <scylla’s workdir> is a path defined by the workdir configuration option
>   <br/>
>   > <socket path>  the node will open the maintenance socket on the path <socket path>

> * **Type:** `sstring`
> * **Default value:** `"workdir"`
> * Liveness: `False`

<a id="confprop-maintenance-socket-group"></a>

### maintenance_socket_group

> The group that the maintenance socket will be owned by. If not set, the group will be the same as the user running the scylla node.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-maintenance-mode"></a>

### maintenance_mode

> If set to true, the node will not connect to other nodes. It will only serve requests to its local data.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-native-transport-port-ssl"></a>

### native_transport_port_ssl

> Port on which the CQL TLS native transport listens for clients.    Enabling client encryption and keeping native_transport_port_ssl disabled will use encryption    for native_transport_port. Setting native_transport_port_ssl to a different value    from native_transport_port will use encryption for native_transport_port_ssl while    keeping native_transport_port unencrypted.

> * **Type:** `uint16_t`
> * **Default value:** `9142`
> * Liveness: `False`

<a id="confprop-native-shard-aware-transport-port"></a>

### native_shard_aware_transport_port

> Like native_transport_port, but clients-side port number (modulo smp) is used to route the connection to the specific shard.

> * **Type:** `uint16_t`
> * **Default value:** `19042`
> * Liveness: `False`

<a id="confprop-native-shard-aware-transport-port-ssl"></a>

### native_shard_aware_transport_port_ssl

> Like native_transport_port_ssl, but clients-side port number (modulo smp) is used to route the connection to the specific shard.

> * **Type:** `uint16_t`
> * **Default value:** `19142`
> * Liveness: `False`

<a id="confprop-native-transport-port-proxy-protocol"></a>

### native_transport_port_proxy_protocol

> Port on which the CQL native transport listens for clients using proxy protocol v2. Disabled (0) by default.

> * **Type:** `uint16_t`
> * **Default value:** `0`
> * Liveness: `False`

<a id="confprop-native-transport-port-ssl-proxy-protocol"></a>

### native_transport_port_ssl_proxy_protocol

> Port on which the CQL TLS native transport listens for clients using proxy protocol v2. Disabled (0) by default.

> * **Type:** `uint16_t`
> * **Default value:** `0`
> * Liveness: `False`

<a id="confprop-native-shard-aware-transport-port-proxy-protocol"></a>

### native_shard_aware_transport_port_proxy_protocol

> Like native_transport_port_proxy_protocol, but clients-side port number (modulo smp) is used to route the connection to the specific shard.

> * **Type:** `uint16_t`
> * **Default value:** `0`
> * Liveness: `False`

<a id="confprop-native-shard-aware-transport-port-ssl-proxy-protocol"></a>

### native_shard_aware_transport_port_ssl_proxy_protocol

> Like native_transport_port_ssl_proxy_protocol, but clients-side port number (modulo smp) is used to route the connection to the specific shard.

> * **Type:** `uint16_t`
> * **Default value:** `0`
> * Liveness: `False`

<a id="confgroup-rpc-remote-procedure-call-settings"></a>

## RPC (remote procedure call) settings

> Settings for configuring and tuning client connections.

<a id="confprop-broadcast-rpc-address"></a>

### broadcast_rpc_address

> RPC address to broadcast to drivers and other Scylla nodes. This cannot be set to 0.0.0.0. If blank, it is set to the value of the rpc_address or rpc_interface. If rpc_address or rpc_interfaceis set to 0.0.0.0, this property must be set.

> * **Type:** `sstring`
> * **Default value:** `{}`
> * Liveness: `False`

<a id="confprop-rpc-keepalive"></a>

### rpc_keepalive

> Enable or disable keepalive on client connections (CQL native and the maintenance socket).

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-cache-hit-rate-read-balancing"></a>

### cache_hit_rate_read_balancing

> This boolean controls whether the replicas for read query will be chosen based on cache hit ratio.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confgroup-advanced-fault-detection-settings"></a>

## Advanced fault detection settings

> Settings to handle poorly performing or failing nodes.

<a id="confprop-hinted-handoff-enabled"></a>

### hinted_handoff_enabled

> Enable or disable hinted handoff. To enable per data center, add data center list. For example: hinted_handoff_enabled: DC1,DC2. A hint indicates that the write needs to be replayed to an unavailable node.     
> : Related information: About hinted handoff writes

> * **Type:** `hinted_handoff_enabled_type`
> * **Default value:** `db::config::hinted_handoff_enabled_type(db::config::hinted_handoff_enabled_type::enabled_for_all_tag())`
> * Liveness: `False`

<a id="confprop-max-hinted-handoff-concurrency"></a>

### max_hinted_handoff_concurrency

> Maximum concurrency allowed for sending hints. The concurrency is divided across shards and rounded up if not divisible by the number of shards. By default (or when set to 0), concurrency of 8\*shard_count will be used.

> * **Type:** `uint32_t`
> * **Default value:** `0`
> * Liveness: `True`

<a id="confprop-max-hint-window-in-ms"></a>

### max_hint_window_in_ms

> Maximum amount of time that hints are generates hints for an unresponsive node. After this interval, new hints are no longer generated until the node is back up and responsive. If the node goes down again, a new interval begins. This setting can prevent a sudden demand for resources when a node is brought back online and the rest of the cluster attempts to replay a large volume of hinted writes.

> > Related information: Failure detection and recovery
> * **Type:** `uint32_t`
> * **Default value:** `10800000`
> * Liveness: `False`

<a id="confprop-batchlog-replay-cleanup-after-replays"></a>

### batchlog_replay_cleanup_after_replays

> Clean up batchlog memtable after every N replays. Replays are issued on a timer, every 60 seconds. So if batchlog_replay_cleanup_after_replays is set to 60, the batchlog memtable is flushed every 60 \* 60 seconds.

> * **Type:** `uint32_t`
> * **Default value:** `1`
> * Liveness: `True`

<a id="confgroup-vector-search-settings"></a>

## Vector search settings

> Settings for configuring and tuning vector search functionality.

<a id="confprop-vector-store-primary-uri"></a>

### vector_store_primary_uri

> A comma-separated list of primary vector store node URIs. These nodes are preferred for vector search operations.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `True`

<a id="confprop-vector-store-secondary-uri"></a>

### vector_store_secondary_uri

> A comma-separated list of secondary vector store node URIs. These nodes are used as a fallback when all primary nodes are unavailable, and are typically located in a different availability zone for high availability.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `True`

<a id="confprop-vector-store-unreachable-node-detection-time-in-ms"></a>

### vector_store_unreachable_node_detection_time_in_ms

> Time in milliseconds for detecting an unreachable vector store node. This value is applied to the TCP connect timeout, keepalive parameters, and TCP_USER_TIMEOUT.     When any of these mechanisms detects that a node is unreachable within this window, the client fails over to the next available vector store node.

> * **Type:** `uint32_t`
> * **Default value:** `3000`
> * Liveness: `True`

<a id="confprop-vector-store-encryption-options"></a>

### vector_store_encryption_options

> Options for encrypted connections to the vector store. These options are used for HTTPS URIs in \`vector_store_primary_uri\` and \`vector_store_secondary_uri\`. The available options are:
> : * truststore: (Default: <not set, use system truststore>) Location of the truststore containing the trusted certificate for authenticating remote servers.

> * **Type:** `string_map`
> * **Default value:** `{}`
> * Liveness: `False`

<a id="confprop-enable-cassio-compatibility"></a>

### enable_cassio_compatibility

> When enabled, ScyllaDB rewrites CassIO’s SAI index DDL on map entries     (e.g. CREATE CUSTOM INDEX … ON table(ENTRIES(col)) USING ‘StorageAttachedIndex’)     to a regular secondary index, allowing LangChain/CassIO applications to run     without DDL errors. Disabled by default.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confgroup-security-properties"></a>

## Security properties

> Server and client security settings.

<a id="confprop-authenticator"></a>

### authenticator

> The authentication backend, used to identify users. The available authenticators are:
> : * org.apache.cassandra.auth.AllowAllAuthenticator: Disables authentication; no checks are performed.
>   * org.apache.cassandra.auth.PasswordAuthenticator: Authenticates users with user names and hashed passwords stored in the system_auth.credentials table. If you use the default, 1, and the node with the lone replica goes down, you will not be able to log into the cluster because the system_auth keyspace was not replicated.
>   * com.scylladb.auth.CertificateAuthenticator: Authenticates users based on TLS certificate authentication subject. Roles and permissions still need to be defined as normal. Super user can be set using the ‘auth_superuser_name’ configuration value. Query to extract role name from subject string is set using ‘auth_certificate_role_queries’.
>   * com.scylladb.auth.TransitionalAuthenticator: Wraps around the PasswordAuthenticator, logging them in if username/password pair provided is correct and treating them as anonymous users otherwise.
>   * com.scylladb.auth.SaslauthdAuthenticator : Use saslauthd for authentication.
>   <br/>
>   Related information: Internal authentication

> * **Type:** `sstring`
> * **Default value:** `"org.apache.cassandra.auth.AllowAllAuthenticator"`
> * Liveness: `False`

<a id="confprop-authorizer"></a>

### authorizer

> The authorization backend. It implements IAuthenticator, which limits access and provides permissions. The available authorizers are:
> : * AllowAllAuthorizer: Disables authorization; allows any action to any user.
>   * CassandraAuthorizer: Stores permissions in system_auth.permissions table. If you use the default, 1, and the node with the lone replica goes down, you will not be able to log into the cluster because the system_auth keyspace was not replicated.
>   * com.scylladb.auth.TransitionalAuthorizer: Wraps around the CassandraAuthorizer, which is used to authorize permission management. Other actions are allowed for all users.
>   <br/>
>   Related information: Object permissions

> * **Type:** `sstring`
> * **Default value:** `"org.apache.cassandra.auth.AllowAllAuthorizer"`
> * Liveness: `False`

<a id="confprop-role-manager"></a>

### role_manager

> The role-management backend, used to maintain grants and memberships between roles.    The available role-managers are:
> : * org.apache.cassandra.auth.CassandraRoleManager: Stores role data in the system_auth keyspace;
>   * com.scylladb.auth.LDAPRoleManager: Fetches role data from an LDAP server.

> * **Type:** `sstring`
> * **Default value:** `"org.apache.cassandra.auth.CassandraRoleManager"`
> * Liveness: `False`

<a id="confprop-permissions-validity-in-ms"></a>

### permissions_validity_in_ms

> How long authorized statements cache entries remain valid. The cached value is considered valid as long as both its value is not older than the permissions_validity_in_ms     and the cached value has been read at least once during the permissions_validity_in_ms time frame. If any of these two conditions doesn’t hold the cached value is going to be evicted from the cache.

> > Related information: Object permissions
> * **Type:** `uint32_t`
> * **Default value:** `10000`
> * Liveness: `True`

<a id="confprop-permissions-update-interval-in-ms"></a>

### permissions_update_interval_in_ms

> Refresh interval for authorized statements cache. After this interval, cache entries become eligible for refresh. An async reload is scheduled every permissions_update_interval_in_ms time period and the old value is returned until it completes. If permissions_validity_in_ms has a non-zero value, then this property must also have a non-zero value. It’s recommended to set this value to be at least 3 times smaller than the permissions_validity_in_ms. This option additionally controls the permissions refresh interval for LDAP.

> * **Type:** `uint32_t`
> * **Default value:** `2000`
> * Liveness: `True`

<a id="confprop-server-encryption-options"></a>

### server_encryption_options

> Enable or disable inter-node encryption. You must also generate keys and provide the appropriate key and trust store locations and passwords. The available options are:
> : * internode_encryption: (Default: none) Enable or disable encryption of inter-node communication using the TLS_RSA_WITH_AES_128_CBC_SHA cipher suite for authentication, key exchange, and encryption of data transfers. The available inter-node options are:
>     : * all: Encrypt all inter-node communications.
>       * none: No encryption.
>       * dc: Encrypt the traffic between the data centers (server only).
>       * rack: Encrypt the traffic between the racks(server only).
>   * certificate: (Default: conf/scylla.crt) The location of a PEM-encoded x509 certificate used to identify and encrypt the internode communication.
>   * keyfile: (Default: conf/scylla.key) PEM Key file associated with certificate.
>   * truststore: (Default: <not set, use system truststore> ) Location of the truststore containing the trusted certificate for authenticating remote servers.
>   * certficate_revocation_list: (Default: <not set>) PEM encoded certificate revocation list.
>   <br/>
>   The advanced settings are:
>   <br/>
>   * priority_string: (Default: not set, use default) GnuTLS priority string controlling TLS algorithms used/allowed.
>   * require_client_auth: (Default: false ) Enables or disables certificate authentication.
>   <br/>
>   Related information: Node-to-node encryption

> * **Type:** `string_map`
> * **Default value:** `{}`
> * Liveness: `False`

<a id="confprop-client-encryption-options"></a>

### client_encryption_options

> Enable or disable client-to-node encryption. You must also generate keys and provide the appropriate key and certificate. The available options are:
> : * enabled: (Default: false) To enable, set to true.
>   * certificate: (Default: conf/scylla.crt) The location of a PEM-encoded x509 certificate used to identify and encrypt the client/server communication.
>   * keyfile: (Default: conf/scylla.key) PEM Key file associated with certificate.
>   * truststore: (Default: <not set. use system truststore>) Location of the truststore containing the trusted certificate for authenticating remote servers.
>   * certficate_revocation_list: (Default: <not set> ) PEM encoded certificate revocation list.
>   <br/>
>   The advanced settings are:
>   <br/>
>   * priority_string: (Default: not set, use default) GnuTLS priority string controlling TLS algorithms used/allowed.
>   * require_client_auth: (Default: false) Enables or disables certificate authentication.
>   * enable_session_tickets: (Default: true) Enables or disables TLS1.3 session tickets.
>   <br/>
>   Related information: Client-to-node encryption

> * **Type:** `string_map`
> * **Default value:** `{}`
> * Liveness: `False`

<a id="confprop-alternator-encryption-options"></a>

### alternator_encryption_options

> When Alternator via HTTPS is enabled with alternator_https_port, where to take the key and certificate. The available options are:
> : * certificate: (Default: conf/scylla.crt) The location of a PEM-encoded x509 certificate used to identify and encrypt the client/server communication.
>   * keyfile: (Default: conf/scylla.key) PEM Key file associated with certificate.
>   <br/>
>   The advanced settings are:
>   <br/>
>   * priority_string: GnuTLS priority string controlling TLS algorithms used/allowed.
>   * enable_session_tickets: (Default: true) Enables or disables TLS1.3 session tickets.

> * **Type:** `string_map`
> * **Default value:** `{}`
> * Liveness: `False`

<a id="confprop-alternator-force-read-before-write"></a>

### alternator_force_read_before_write

> Forces Alternator to perform Read Before Write. Used for better DynamoDB compatibility in WCU calculation

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-ssl-storage-port"></a>

### ssl_storage_port

> The SSL port for encrypted communication. Unused unless enabled in encryption_options.

> * **Type:** `uint32_t`
> * **Default value:** `7001`
> * Liveness: `False`

<a id="confprop-enable-in-memory-data-store"></a>

### enable_in_memory_data_store

> Enable in memory mode (system tables are always persisted).

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-enable-cache"></a>

### enable_cache

> Enable cache.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-enable-commitlog"></a>

### enable_commitlog

> Enable commitlog.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-volatile-system-keyspace-for-testing"></a>

### volatile_system_keyspace_for_testing

> Don’t persist system keyspace - testing only!

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-api-port"></a>

### api_port

> Http Rest API port.

> * **Type:** `uint16_t`
> * **Default value:** `10000`
> * Liveness: `False`

<a id="confprop-api-address"></a>

### api_address

> Http Rest API address.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-api-ui-dir"></a>

### api_ui_dir

> The directory location of the API GUI.

> * **Type:** `sstring`
> * **Default value:** `"swagger-ui/dist/"`
> * Liveness: `False`

<a id="confprop-api-doc-dir"></a>

### api_doc_dir

> The API definition file directory.

> * **Type:** `sstring`
> * **Default value:** `"api/api-doc/"`
> * Liveness: `False`

<a id="confprop-consistent-rangemovement"></a>

### consistent_rangemovement

> When set to true, range movements will be consistent. It means: 1) it will refuse to bootstrap a new node if other bootstrapping/leaving/moving nodes detected. 2) data will be streamed to a new node only from the node which is no longer responsible for the token range. Same as -Dcassandra.consistent.rangemovement in cassandra.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-join-ring"></a>

### join_ring

> When set to true, a node will join the token ring. When set to false, a node will not join the token ring. This option cannot be changed after a node joins the cluster. If set to false, it overwrites the num_tokens and initial_token options. Setting to false is supported only if the cluster uses the raft-managed topology.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-load-ring-state"></a>

### load_ring_state

> When set to true, load tokens and host_ids previously saved. Same as -Dcassandra.load_ring_state in cassandra.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-replace-node-first-boot"></a>

### replace_node_first_boot

> The Host ID of a dead node to replace. If the replacing node has already been bootstrapped successfully, this option will be ignored.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-replace-address"></a>

### replace_address

> [[deprecated]] The listen_address or broadcast_address of the dead node to replace. Same as -Dcassandra.replace_address.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-replace-address-first-boot"></a>

### replace_address_first_boot

> [[deprecated]] Like replace_address option, but if the node has been bootstrapped successfully it will be ignored. Same as -Dcassandra.replace_address_first_boot.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-ignore-dead-nodes-for-replace"></a>

### ignore_dead_nodes_for_replace

> List dead nodes to ignore for replace operation using a comma-separated list of host IDs. E.g., scylla –ignore-dead-nodes-for-replace 8d5ed9f4-7764-4dbd-bad8-43fddce94b7c,125ed9f4-7777-1dbn-mac8-43fddce9123e

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-enable-repair-based-node-ops"></a>

### enable_repair_based_node_ops

> Set true to use enable repair based node operations instead of streaming based.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confprop-allowed-repair-based-node-ops"></a>

### allowed_repair_based_node_ops

> A comma separated list of node operations which are allowed to enable repair based node operations. The operations can be bootstrap, replace, removenode, decommission and rebuild.

> * **Type:** `sstring`
> * **Default value:** `"replace,removenode,rebuild"`
> * Liveness: `True`

<a id="confprop-enable-compacting-data-for-streaming-and-repair"></a>

### enable_compacting_data_for_streaming_and_repair

> Enable the compacting reader, which compacts the data for streaming and repair (load’n’stream included) before sending it to, or synchronizing it with peers. Can reduce the amount of data to be processed by removing dead data, but adds CPU overhead.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confprop-enable-tombstone-gc-for-streaming-and-repair"></a>

### enable_tombstone_gc_for_streaming_and_repair

> If the compacting reader is enabled for streaming and repair (see enable_compacting_data_for_streaming_and_repair), allow it to garbage-collect tombstones.     This can reduce the amount of data repair has to process.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-repair-partition-count-estimation-ratio"></a>

### repair_partition_count_estimation_ratio

> Specify the fraction of partitions written by repair out of the total partitions. The value is currently only used for bloom filter estimation. Value is between 0 and 1.

> * **Type:** `double`
> * **Default value:** `0.1`
> * Liveness: `True`

<a id="confprop-repair-hints-batchlog-flush-cache-time-in-ms"></a>

### repair_hints_batchlog_flush_cache_time_in_ms

> The repair hints and batchlog flush request cache time. Setting 0 disables the flush cache. The cache reduces the number of hints and batchlog flushes during repair when tombstone_gc is set to repair mode. When the cache is on, a slightly smaller repair time will be used with the benefits of dropped hints and batchlog flushes.

> * **Type:** `uint32_t`
> * **Default value:** `60 * 1000`
> * Liveness: `True`

<a id="confprop-repair-multishard-reader-buffer-hint-size"></a>

### repair_multishard_reader_buffer_hint_size

> The buffer size to use for the buffer-hint feature of the multishard reader when running repair in mixed-shard clusters. This can help the performance of mixed-shard repair (including RBNO). Set to 0 to disable the hint feature altogether.

> * **Type:** `uint64_t`
> * **Default value:** `1 * 1024 * 1024`
> * Liveness: `True`

<a id="confprop-repair-multishard-reader-enable-read-ahead"></a>

### repair_multishard_reader_enable_read_ahead

> The multishard reader has a read-ahead feature to improve latencies of range-scans. This feature can be detrimental when the multishard reader is used under repair, as is the case with repair in mixed-shard clusters.     This configuration option is disabled by default and it serves as a fall-back, to re-enable read-ahead in case it turns out that some mixed-shard repair suffer from disabling it.

> * **Type:** `uint64_t`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-enable-small-table-optimization-for-rbno"></a>

### enable_small_table_optimization_for_rbno

> Set true to enable small table optimization for repair based node operations

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confprop-small-table-optimization-for-rbno-max-table-size"></a>

### small_table_optimization_for_rbno_max_table_size

> Maximum on-disk size (in bytes) of a user table for it to be automatically eligible for the small table optimization for repair based node operations. The size is probed on the replicas the operation syncs from. Defaults to 1 GiB. Only takes effect when enable_small_table_optimization_for_rbno is true.

> * **Type:** `uint64_t`
> * **Default value:** `1073741824`
> * Liveness: `True`

<a id="confprop-ring-delay-ms"></a>

### ring_delay_ms

> Time a node waits to hear from other nodes before joining the ring in milliseconds. Same as -Dcassandra.ring_delay_ms in cassandra.

> * **Type:** `uint32_t`
> * **Default value:** `30 * 1000`
> * Liveness: `False`

<a id="confprop-shadow-round-ms"></a>

### shadow_round_ms

> The maximum gossip shadow round time. Can be used to reduce the gossip feature check time during node boot up.

> * **Type:** `uint32_t`
> * **Default value:** `300 * 1000`
> * Liveness: `False`

<a id="confprop-fd-max-interval-ms"></a>

### fd_max_interval_ms

> The maximum failure_detector interval time in milliseconds. Interval larger than the maximum will be ignored. Larger cluster may need to increase the default.

> * **Type:** `uint32_t`
> * **Default value:** `2 * 1000`
> * Liveness: `False`

<a id="confprop-fd-initial-value-ms"></a>

### fd_initial_value_ms

> The initial failure_detector interval time in milliseconds.

> * **Type:** `uint32_t`
> * **Default value:** `2 * 1000`
> * Liveness: `False`

<a id="confprop-shutdown-announce-in-ms"></a>

### shutdown_announce_in_ms

> Time a node waits after sending gossip shutdown message in milliseconds. Same as -Dcassandra.shutdown_announce_in_ms in cassandra.

> * **Type:** `uint32_t`
> * **Default value:** `2 * 1000`
> * Liveness: `False`

<a id="confprop-developer-mode"></a>

### developer_mode

> Relax environment checks. Setting to true can reduce performance and reliability significantly.

> * **Type:** `bool`
> * **Default value:** `DEVELOPER_MODE_DEFAULT`
> * Liveness: `False`

<a id="confprop-force-gossip-generation"></a>

### force_gossip_generation

> Force gossip to use the generation number provided by user.

> * **Type:** `int32_t`
> * **Default value:** `-1`
> * Liveness: `True`

<a id="confprop-lsa-reclamation-step"></a>

### lsa_reclamation_step

> Minimum number of segments to reclaim in a single step.

> * **Type:** `size_t`
> * **Default value:** `1`
> * Liveness: `False`

<a id="confprop-prometheus-port"></a>

### prometheus_port

> Prometheus port, set to zero to disable.

> * **Type:** `uint16_t`
> * **Default value:** `9180`
> * Liveness: `False`

<a id="confprop-prometheus-address"></a>

### prometheus_address

> Prometheus listening address, defaulting to listen_address if not explicitly set.

> * **Type:** `sstring`
> * **Default value:** `{}`
> * Liveness: `False`

<a id="confprop-prometheus-prefix"></a>

### prometheus_prefix

> Set the prefix of the exported Prometheus metrics. Changing this will break Scylla’s dashboard compatibility, do not change unless you know what you are doing.

> * **Type:** `sstring`
> * **Default value:** `"scylla"`
> * Liveness: `False`

<a id="confprop-prometheus-allow-protobuf"></a>

### prometheus_allow_protobuf

> If set allows the experimental Prometheus protobuf with native histogram

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-abort-on-lsa-bad-alloc"></a>

### abort_on_lsa_bad_alloc

> Abort when allocation in LSA region fails.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-murmur3-partitioner-ignore-msb-bits"></a>

### murmur3_partitioner_ignore_msb_bits

> Number of most significant token bits to ignore in murmur3 partitioner; increase for very large clusters.

> * **Type:** `unsigned`
> * **Default value:** `default_murmur3_partitioner_ignore_msb_bits`
> * Liveness: `False`

<a id="confprop-unspooled-dirty-soft-limit"></a>

### unspooled_dirty_soft_limit

> Soft limit of unspooled dirty memory expressed as a portion of the hard limit.

> * **Type:** `double`
> * **Default value:** `0.6`
> * Liveness: `False`

<a id="confprop-sstable-summary-ratio"></a>

### sstable_summary_ratio

> Enforces that 1 byte of summary is written for every N (2000 by default)    bytes written to data file. Value must be between 0 and 1.

> * **Type:** `double`
> * **Default value:** `0.0005`
> * Liveness: `False`

<a id="confprop-sstable-summary-max-partitions-per-page"></a>

### sstable_summary_max_partitions_per_page

> Hard limit on the number of partition keys covered by a single sstable summary entry.     A summary entry is forced (breaking the index page) once this many partitions accumulate, which prevents     pathologically large index pages.

> * **Type:** `uint64_t`
> * **Default value:** `10000`
> * Liveness: `True`

<a id="confprop-components-memory-reclaim-threshold"></a>

### components_memory_reclaim_threshold

> Ratio of available memory for all in-memory components of SSTables in a shard beyond which the memory will be reclaimed from components until it falls back under the threshold. Currently, this limit is only enforced for bloom filters.

> * **Type:** `double`
> * **Default value:** `.2`
> * Liveness: `True`

<a id="confprop-large-memory-allocation-warning-threshold"></a>

### large_memory_allocation_warning_threshold

> Warn about memory allocations above this size; set to zero to disable.

> * **Type:** `size_t`
> * **Default value:** `(size_t(128) << 10) + 1`
> * Liveness: `False`

<a id="confprop-enable-deprecated-partitioners"></a>

### enable_deprecated_partitioners

> Enable the byteordered and random partitioners. These partitioners are deprecated and will be removed in a future version.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-enable-keyspace-column-family-metrics"></a>

### enable_keyspace_column_family_metrics

> Enable per keyspace and per column family metrics reporting.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-enable-node-aggregated-table-metrics"></a>

### enable_node_aggregated_table_metrics

> Enable aggregated per node, per keyspace and per table metrics reporting, applicable if enable_keyspace_column_family_metrics is false.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-enable-sstable-data-integrity-check"></a>

### enable_sstable_data_integrity_check

> Enable interposer which checks for integrity of every sstable write.     Performance is affected to some extent as a result. Useful to help debugging problems that may arise at another layers.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-enable-sstable-key-validation"></a>

### enable_sstable_key_validation

> Enable validation of partition and clustering keys monotonicity     Performance is affected to some extent as a result. Useful to help debugging problems that may arise at another layers.

> * **Type:** `bool`
> * **Default value:** `ENABLE_SSTABLE_KEY_VALIDATION`
> * Liveness: `False`

<a id="confprop-ignore-component-digest-mismatch"></a>

### ignore_component_digest_mismatch

> When set, log a warning instead of refusing to load sstables with component digest mismatches.     Useful for recovering from corrupted non-vital components or working around bugs in digest calculation.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-view-building"></a>

### view_building

> Enable view building; should only be set to false when the node is experience issues due to view building.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-sstable-format"></a>

### sstable_format

> Default sstable file format

> * **Type:** `sstring`
> * **Default value:** `"me"`
> * Liveness: `True`

<a id="confprop-sstable-compression-user-table-options"></a>

### sstable_compression_user_table_options

> Server-global user table compression options. If enabled, all user tables    will be compressed using the provided options, unless overridden    by compression options in the table schema. User tables are all tables in non-system keyspaces. The available options are:
> : * sstable_compression: The compression algorithm to use. Supported values: LZ4Compressor, LZ4WithDictsCompressor (default), SnappyCompressor, DeflateCompressor, ZstdCompressor, ZstdWithDictsCompressor, ‘’ (empty string; disables compression).
>   * chunk_length_in_kb: (Default: 4) The size of chunks to compress in kilobytes. Allowed values are powers of two between 1 and 128.
>   * crc_check_chance: (Default: 1.0) Not implemented (option value is ignored).
>   * compression_level: (Default: 3) Compression level for ZstdCompressor and ZstdWithDictsCompressor. Higher levels provide better compression ratios at the cost of speed. Allowed values are integers between 1 and 22.

> * **Type:** `compression_parameters`
> * **Default value:** `compression_parameters{compression_parameters::algorithm::lz4_with_dicts}`
> * Liveness: `False`

<a id="confprop-sstable-compression-dictionaries-enable-writing"></a>

### sstable_compression_dictionaries_enable_writing

> Enables SSTable compression with shared dictionaries (for tables which opt in). If set to false, this node won’t write any new SSTables using dictionary compression.
> : Option meant not for regular usage, but for unforeseen problems that call for disabling dictionaries without modifying table schema.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confprop-sstable-compression-dictionaries-memory-budget-fraction"></a>

### sstable_compression_dictionaries_memory_budget_fraction

> Fall back to compression without dictionaries if RAM usage by dictionaries is greater or equal to this fraction of the shard’s memory.

> * **Type:** `float`
> * **Default value:** `0.01`
> * Liveness: `True`

<a id="confprop-sstable-compression-dictionaries-retrain-period-in-seconds"></a>

### sstable_compression_dictionaries_retrain_period_in_seconds

> Minimum age of the current compression dictionary before another dictionary for this table is trained.

> * **Type:** `float`
> * **Default value:** `86400`
> * Liveness: `True`

<a id="confprop-sstable-compression-dictionaries-autotrainer-tick-period-in-seconds"></a>

### sstable_compression_dictionaries_autotrainer_tick_period_in_seconds

> The period with which automatic dictionary training is attempted.

> * **Type:** `float`
> * **Default value:** `900`
> * Liveness: `True`

<a id="confprop-sstable-compression-dictionaries-min-training-dataset-bytes"></a>

### sstable_compression_dictionaries_min_training_dataset_bytes

> The minimum size a table has to reach before dictionaries will be trained for it.

> * **Type:** `uint64_t`
> * **Default value:** `1*1024*1024*1024`
> * Liveness: `True`

<a id="confprop-sstable-compression-dictionaries-min-training-improvement-factor"></a>

### sstable_compression_dictionaries_min_training_improvement_factor

> New dictionaries will be only published if the estimated compression ratio is smaller than current ratio multiplied by this factor.

> * **Type:** `float`
> * **Default value:** `0.95`
> * Liveness: `True`

<a id="confprop-table-digest-insensitive-to-expiry"></a>

### table_digest_insensitive_to_expiry

> When enabled, per-table schema digest calculation ignores empty partitions.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-enable-dangerous-direct-import-of-cassandra-counters"></a>

### enable_dangerous_direct_import_of_cassandra_counters

> Only turn this option on if you want to import tables from Cassandra containing counters, and you are SURE that no counters in that table were created in a version earlier than Cassandra 2.1.     It is not enough to have ever since upgraded to newer versions of Cassandra. If you EVER used a version earlier than 2.1 in the cluster where these SSTables come from, DO NOT TURN ON THIS OPTION! You will corrupt your data. You have been warned.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-enable-shard-aware-drivers"></a>

### enable_shard_aware_drivers

> Enable native transport drivers to use connection-per-shard for better performance.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-enable-ipv6-dns-lookup"></a>

### enable_ipv6_dns_lookup

> Use IPv6 address resolution

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-abort-on-internal-error"></a>

### abort_on_internal_error

> Abort the server instead of throwing exception when internal invariants are violated.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-max-partition-key-restrictions-per-query"></a>

### max_partition_key_restrictions_per_query

> Maximum number of distinct partition keys restrictions per query. This limit places a bound on the size of IN tuples,     especially when multiple partition key columns have IN restrictions. Increasing this value can result in server instability.

> * **Type:** `uint32_t`
> * **Default value:** `100`
> * Liveness: `True`

<a id="confprop-max-clustering-key-restrictions-per-query"></a>

### max_clustering_key_restrictions_per_query

> Maximum number of distinct clustering key restrictions per query. This limit places a bound on the size of IN tuples,     especially when multiple clustering key columns have IN restrictions. Increasing this value can result in server instability.

> * **Type:** `uint32_t`
> * **Default value:** `100`
> * Liveness: `True`

<a id="confprop-max-memory-for-unlimited-query-soft-limit"></a>

### max_memory_for_unlimited_query_soft_limit

> Maximum amount of memory a query, whose memory consumption is not naturally limited, is allowed to consume, e.g. non-paged and reverse queries.     This is the soft limit, there will be a warning logged for queries violating this limit.

> * **Type:** `uint64_t`
> * **Default value:** `uint64_t(1) << 20`
> * Liveness: `True`

<a id="confprop-max-memory-for-unlimited-query-hard-limit"></a>

### max_memory_for_unlimited_query_hard_limit

> Maximum amount of memory a query, whose memory consumption is not naturally limited, is allowed to consume, e.g. non-paged and reverse queries.     This is the hard limit, queries violating this limit will be aborted.

> * **Type:** `uint64_t`
> * **Default value:** `(uint64_t(100) << 20)`
> * Liveness: `True`

<a id="confprop-reader-concurrency-semaphore-serialize-limit-multiplier"></a>

### reader_concurrency_semaphore_serialize_limit_multiplier

> Start serializing reads after their collective memory consumption goes above $normal_limit \* $multiplier.

> * **Type:** `uint32_t`
> * **Default value:** `2`
> * Liveness: `True`

<a id="confprop-reader-concurrency-semaphore-kill-limit-multiplier"></a>

### reader_concurrency_semaphore_kill_limit_multiplier

> Start killing reads after their collective memory consumption goes above $normal_limit \* $multiplier.

> * **Type:** `uint32_t`
> * **Default value:** `4`
> * Liveness: `True`

<a id="confprop-reader-concurrency-semaphore-cpu-concurrency"></a>

### reader_concurrency_semaphore_cpu_concurrency

> Admit new reads while there are less than this number of requests that need CPU.

> * **Type:** `uint32_t`
> * **Default value:** `2`
> * Liveness: `True`

<a id="confprop-reader-concurrency-semaphore-preemptive-abort-factor"></a>

### reader_concurrency_semaphore_preemptive_abort_factor

> Admit new reads while their remaining time is more than this factor times their timeout times when arrived to a semaphore. Its vale means
> : * <= 0.0 means new reads will never get rejected during admission
>   * >= 1.0 means new reads will always get rejected during admission

> * **Type:** `float`
> * **Default value:** `0.3`
> * Liveness: `True`

<a id="confprop-reader-concurrency-semaphore-shared-pool-fraction"></a>

### reader_concurrency_semaphore_shared_pool_fraction

> Fraction of memory to allocate to the shared pool for reader concurrency semaphores. Clamped to the [0, 1] range. A setting of 0 effectively disables the shared pool.

> * **Type:** `double`
> * **Default value:** `0.5`
> * Liveness: `True`

<a id="confprop-view-update-reader-concurrency-semaphore-serialize-limit-multiplier"></a>

### view_update_reader_concurrency_semaphore_serialize_limit_multiplier

> Start serializing view update reads after their collective memory consumption goes above $normal_limit \* $multiplier.

> * **Type:** `uint32_t`
> * **Default value:** `2`
> * Liveness: `True`

<a id="confprop-view-update-reader-concurrency-semaphore-kill-limit-multiplier"></a>

### view_update_reader_concurrency_semaphore_kill_limit_multiplier

> Start killing view update reads after their collective memory consumption goes above $normal_limit \* $multiplier.

> * **Type:** `uint32_t`
> * **Default value:** `4`
> * Liveness: `True`

<a id="confprop-view-update-reader-concurrency-semaphore-cpu-concurrency"></a>

### view_update_reader_concurrency_semaphore_cpu_concurrency

> Admit new view update reads while there are less than this number of requests that need CPU.

> * **Type:** `uint32_t`
> * **Default value:** `1`
> * Liveness: `True`

<a id="confprop-maintenance-reader-concurrency-semaphore-count-limit"></a>

### maintenance_reader_concurrency_semaphore_count_limit

> Allow up to this many maintenance (e.g. streaming and repair) reads per shard to progress at the same time.

> * **Type:** `int`
> * **Default value:** `10`
> * Liveness: `True`

<a id="confprop-twcs-max-window-count"></a>

### twcs_max_window_count

> The maximum number of compaction windows allowed when making use of TimeWindowCompactionStrategy. A setting of 0 effectively disables the restriction.

> * **Type:** `uint32_t`
> * **Default value:** `50`
> * Liveness: `True`

<a id="confprop-initial-sstable-loading-concurrency"></a>

### initial_sstable_loading_concurrency

> Maximum amount of sstables to load in parallel during initialization. A higher number can lead to more memory consumption. You should not need to touch this.

> * **Type:** `unsigned`
> * **Default value:** `4u`
> * Liveness: `False`

<a id="confprop-enable-3-1-0-compatibility-mode"></a>

### enable_3_1_0_compatibility_mode

> Set to true if the cluster was initially installed from 3.1.0. If it was upgraded from an earlier version,     or installed from a later version, leave this set to false. This adjusts the communication protocol to     work around a bug in Scylla 3.1.0.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-enable-user-defined-functions"></a>

### enable_user_defined_functions

> Enable user defined functions. You must also set \`\`experimental-features=udf\`\`.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-user-defined-function-time-limit-ms"></a>

### user_defined_function_time_limit_ms

> The time limit for each UDF invocation.

> * **Type:** `unsigned`
> * **Default value:** `10`
> * Liveness: `False`

<a id="confprop-user-defined-function-allocation-limit-bytes"></a>

### user_defined_function_allocation_limit_bytes

> How much memory each UDF invocation can allocate.

> * **Type:** `unsigned`
> * **Default value:** `1024*1024`
> * Liveness: `False`

<a id="confprop-user-defined-function-contiguous-allocation-limit-bytes"></a>

### user_defined_function_contiguous_allocation_limit_bytes

> How much memory each UDF invocation can allocate in one chunk.

> * **Type:** `unsigned`
> * **Default value:** `1024*1024`
> * Liveness: `False`

<a id="confprop-schema-registry-grace-period"></a>

### schema_registry_grace_period

> Time period in seconds after which unused schema versions will be evicted from the local schema registry cache. Default is 1 second.

> * **Type:** `uint32_t`
> * **Default value:** `1`
> * Liveness: `False`

<a id="confprop-max-concurrent-requests-per-shard"></a>

### max_concurrent_requests_per_shard

> Maximum number of concurrent requests a single shard can handle before it starts shedding extra load. By default, no requests will be shed.

> * **Type:** `uint32_t`
> * **Default value:** `std::numeric_limits<uint32_t>::max()`
> * Liveness: `True`

<a id="confprop-uninitialized-connections-semaphore-cpu-concurrency"></a>

### uninitialized_connections_semaphore_cpu_concurrency

> Maximum number of new concurrent connections from drivers that a single shard can be processing before it starts throttling incoming connections. This limit applies only to new connections excluding the ones blocked on network IO; connections that are ready to serve requests are not affected. By default the limit is 8.

> * **Type:** `uint32_t`
> * **Default value:** `8`
> * Liveness: `True`

<a id="confprop-cdc-dont-rewrite-streams"></a>

### cdc_dont_rewrite_streams

> Disable rewriting streams from cdc_streams_descriptions to cdc_streams_descriptions_v2. Should not be necessary, but the procedure is expensive and prone to failures; this config option is left as a backdoor in case some user requires manual intervention.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-strict-allow-filtering"></a>

### strict_allow_filtering

> Match Cassandra in requiring ALLOW FILTERING on slow queries. Can be true, false, or warn. When false, Scylla accepts some slow queries even without ALLOW FILTERING that Cassandra rejects. Warn is same as false, but with warning.

> * **Type:** `tri_mode_restriction`
> * **Default value:** `strict_allow_filtering_default()`
> * Liveness: `True`

<a id="confprop-strict-is-not-null-in-views"></a>

### strict_is_not_null_in_views

> In materialized views, restrictions are allowed only on the view’s primary key columns.
> : In old versions Scylla mistakenly allowed IS NOT NULL restrictions on columns which were not part of the view’s     primary key. These invalid restrictions were ignored.
>   This option controls the behavior when someone tries to create a view with such invalid IS NOT NULL restrictions.
>   <br/>
>   Can be true, false, or warn:
>   : * \`true\`: IS NOT NULL is allowed only on the view’s primary key columns,     trying to use it on other columns will cause an error, as it should.
>     * \`false\`: Scylla accepts IS NOT NULL restrictions on regular columns, but they’re silently ignored.     It’s useful for backwards compatibility.
>     * \`warn\`: The same as false, but there’s a warning about invalid view restrictions.
>   <br/>
>   To preserve backwards compatibility on old clusters, Scylla’s default setting is \`warn\`.     New clusters have this option set to \`true\` by scylla.yaml (which overrides the default \`warn\`),     to make sure that trying to create an invalid view causes an error.

> * **Type:** `tri_mode_restriction`
> * **Default value:** `db::tri_mode_restriction_t::mode::WARN`
> * Liveness: `True`

<a id="confprop-enable-cql-config-updates"></a>

### enable_cql_config_updates

> Make the system.config table UPDATEable.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confprop-enable-parallelized-aggregation"></a>

### enable_parallelized_aggregation

> Use on a new, parallel algorithm for performing aggregate queries.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confprop-cql-duplicate-bind-variable-names-refer-to-same-variable"></a>

### cql_duplicate_bind_variable_names_refer_to_same_variable

> A bind variable that appears twice in a CQL query refers to a single variable (if false, no name matching is performed).

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confprop-max-relations-in-where-clause"></a>

### max_relations_in_where_clause

> Maximum number of relations allowed in a WHERE clause. Queries with too many relations can cause quadratic complexity.

> * **Type:** `uint32_t`
> * **Default value:** `100`
> * Liveness: `True`

<a id="confprop-select-internal-page-size"></a>

### select_internal_page_size

> SELECT statements with aggregation or GROUP BYs or a secondary index may use this page size for their internal reading data, not the page size specified in the query options.

> * **Type:** `uint32_t`
> * **Default value:** `10000`
> * Liveness: `True`

<a id="confprop-alternator-port"></a>

### alternator_port

> Alternator API port.

> * **Type:** `uint16_t`
> * **Default value:** `0`
> * Liveness: `False`

<a id="confprop-alternator-https-port"></a>

### alternator_https_port

> Alternator API HTTPS port.

> * **Type:** `uint16_t`
> * **Default value:** `0`
> * Liveness: `False`

<a id="confprop-alternator-port-proxy-protocol"></a>

### alternator_port_proxy_protocol

> Port on which the Alternator API listens for clients using proxy protocol v2. Disabled (0) by default.

> * **Type:** `uint16_t`
> * **Default value:** `0`
> * Liveness: `False`

<a id="confprop-alternator-https-port-proxy-protocol"></a>

### alternator_https_port_proxy_protocol

> Port on which the Alternator HTTPS API listens for clients using proxy protocol v2. Disabled (0) by default.

> * **Type:** `uint16_t`
> * **Default value:** `0`
> * Liveness: `False`

<a id="confprop-alternator-address"></a>

### alternator_address

> Alternator API listening address.

> * **Type:** `sstring`
> * **Default value:** `"0.0.0.0"`
> * Liveness: `False`

<a id="confprop-alternator-enforce-authorization"></a>

### alternator_enforce_authorization

> Enforce checking the authorization header for every request in Alternator.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-alternator-warn-authorization"></a>

### alternator_warn_authorization

> Count and log warnings about failed authentication or authorization

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-alternator-write-isolation"></a>

### alternator_write_isolation

> Default write isolation policy for Alternator.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-alternator-streams-time-window-s"></a>

### alternator_streams_time_window_s

> CDC query confidence window for alternator streams.

> * **Type:** `uint32_t`
> * **Default value:** `10`
> * Liveness: `False`

<a id="confprop-alternator-streams-increased-compatibility"></a>

### alternator_streams_increased_compatibility

> Increases compatibility with DynamoDB Streams at the cost of performance.     If enabled, Alternator compares the existing item with the new one during     data-modifying operations to determine which event type should be emitted.     This penalty is incurred only for tables with Alternator Streams enabled.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-alternator-timeout-in-ms"></a>

### alternator_timeout_in_ms

> The server-side timeout for completing Alternator API requests.

> * **Type:** `uint32_t`
> * **Default value:** `10000`
> * Liveness: `True`

<a id="confprop-alternator-ttl-period-in-seconds"></a>

### alternator_ttl_period_in_seconds

> The default period for Alternator’s expiration scan. Alternator attempts to scan every table within that period.

> * **Type:** `double`
> * **Default value:** `60*60*24`
> * Liveness: `False`

<a id="confprop-alternator-describe-endpoints"></a>

### alternator_describe_endpoints

> Overrides the behavior of Alternator’s DescribeEndpoints operation.     An empty value (the default) means DescribeEndpoints will return     the same endpoint used in the request. The string ‘disabled’     disables the DescribeEndpoints operation. Any other string is the     fixed value that will be returned by DescribeEndpoints operations.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `True`

<a id="confprop-alternator-max-items-in-batch-write"></a>

### alternator_max_items_in_batch_write

> Maximum amount of items in single BatchItemWrite call.

> * **Type:** `uint32_t`
> * **Default value:** `100`
> * Liveness: `False`

<a id="confprop-alternator-allow-system-table-write"></a>

### alternator_allow_system_table_write

> Allow writing to system tables using the .scylla.alternator.system prefix

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-alternator-max-expression-cache-entries-per-shard"></a>

### alternator_max_expression_cache_entries_per_shard

> Maximum number of cached parsed request expressions, per shard.

> * **Type:** `uint32_t`
> * **Default value:** `2000`
> * Liveness: `True`

<a id="confprop-alternator-max-users-query-size-in-trace-output"></a>

### alternator_max_users_query_size_in_trace_output

> Maximum size of user’s command in trace output (\`alternator_op\` entry). Larger traces will be truncated and have \`<truncated>\` message appended - which doesn’t count to the maximum limit.

> * **Type:** `uint64_t`
> * **Default value:** `uint64_t(4096)`
> * Liveness: `True`

<a id="confprop-alternator-describe-table-info-cache-validity-in-seconds"></a>

### alternator_describe_table_info_cache_validity_in_seconds

> The validity of DescribeTable information - table size in bytes. This is how long calculated value will be reused before recalculation.

> * **Type:** `uint32_t`
> * **Default value:** `60 * 60 * 6`
> * Liveness: `True`

<a id="confprop-alternator-response-gzip-compression-level"></a>

### alternator_response_gzip_compression_level

> Controls gzip and deflate compression level for Alternator response bodies (if the client requests it via Accept-Encoding header) Default of 6 is a compromise between speed and compression.
> : Valid values:
>   <br/>
>   > 0 : No compression (disables gzip/deflate)
>   <br/>
>   > 1-9: Compression levels (1 = fastest, 9 = best compression)

> * **Type:** `int`
> * **Default value:** `int8_t(6)`
> * Liveness: `True`

<a id="confprop-alternator-response-compression-threshold-in-bytes"></a>

### alternator_response_compression_threshold_in_bytes

> When the compression is enabled, this value indicates the minimum size of data to compress. Smaller responses will not be compressed.

> * **Type:** `uint32_t`
> * **Default value:** `uint64_t(4096)`
> * Liveness: `True`

<a id="confprop-alternator-http-response-disable-content-type-header"></a>

### alternator_http_response_disable_content_type_header

> Disable the Content-Type header in HTTP responses from Alternator.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-alternator-http-response-disable-date-header"></a>

### alternator_http_response_disable_date_header

> Disable the Date header in HTTP responses from Alternator.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-alternator-http-response-server-header"></a>

### alternator_http_response_server_header

> Value for the Server header in HTTP responses from Alternator. An empty string (the default) omits the Server header entirely.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `True`

<a id="confprop-abort-on-ebadf"></a>

### abort_on_ebadf

> Abort the server on incorrect file descriptor access. Throws exception when disabled.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-sanitizer-report-backtrace"></a>

### sanitizer_report_backtrace

> In debug mode, report log-structured allocator sanitizer violations with a backtrace. Slow.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-flush-schema-tables-after-modification"></a>

### flush_schema_tables_after_modification

> Flush tables in the system_schema keyspace after schema modification. This is required for crash recovery, but slows down tests and can be disabled for them

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confprop-restrict-twcs-without-default-ttl"></a>

### restrict_twcs_without_default_ttl

> Controls whether to prevent creating TimeWindowCompactionStrategy tables without a default TTL. Can be true, false, or warn.

> * **Type:** `tri_mode_restriction`
> * **Default value:** `db::tri_mode_restriction_t::mode::WARN`
> * Liveness: `True`

<a id="confprop-restrict-future-timestamp"></a>

### restrict_future_timestamp

> Controls whether to detect and forbid unreasonable USING TIMESTAMP, more than 3 days into the future.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confprop-unsafe-ignore-truncation-record"></a>

### unsafe_ignore_truncation_record

> Ignore truncation record stored in system tables as if tables were never truncated.

> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-task-ttl-in-seconds"></a>

### task_ttl_in_seconds

> Time for which information about finished task started internally stays in memory.

> * **Default value:** `0`
> * Liveness: `True`

<a id="confprop-user-task-ttl-in-seconds"></a>

### user_task_ttl_in_seconds

> Time for which information about finished task started by user stays in memory.

> * **Default value:** `3600`
> * Liveness: `True`

<a id="confprop-nodeops-watchdog-timeout-seconds"></a>

### nodeops_watchdog_timeout_seconds

> Time in seconds after which node operations abort when not hearing from the coordinator.

> * **Type:** `uint32_t`
> * **Default value:** `120`
> * Liveness: `True`

<a id="confprop-nodeops-heartbeat-interval-seconds"></a>

### nodeops_heartbeat_interval_seconds

> Period of heartbeat ticks in node operations.

> * **Type:** `uint32_t`
> * **Default value:** `10`
> * Liveness: `True`

<a id="confprop-cache-index-pages"></a>

### cache_index_pages

> Keep SSTable index pages in the global cache after a SSTable read. Expected to improve performance for workloads with big partitions, but may degrade performance for workloads with small partitions. The amount of memory usable by index cache is limited with \`\`index_cache_fraction\`\`.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `True`

<a id="confprop-index-cache-fraction"></a>

### index_cache_fraction

> The maximum fraction of cache memory permitted for use by index cache. Clamped to the [0.0; 1.0] range. Must be small enough to not deprive the row cache of memory, but should be big enough to fit a large fraction of the index. The default value 0.2 means that at least 80% of cache memory is reserved for the row cache, while at most 20% is usable by the index cache.

> * **Type:** `double`
> * **Default value:** `0.2`
> * Liveness: `True`

<a id="confprop-recovery-leader"></a>

### recovery_leader

> Host ID of the node restarted first while performing the Manual Raft-based Recovery Procedure. Warning: this option disables some guardrails for the needs of the Manual Raft-based Recovery Procedure. Make sure you unset it at the end of the procedure.

> * **Type:** `UUID`
> * **Default value:** `utils::null_uuid()`
> * Liveness: `True`

<a id="confprop-wasm-cache-memory-fraction"></a>

### wasm_cache_memory_fraction

> Maximum total size of all WASM instances stored in the cache as fraction of total shard memory.

> * **Type:** `double`
> * **Default value:** `0.01`
> * Liveness: `False`

<a id="confprop-wasm-cache-timeout-in-ms"></a>

### wasm_cache_timeout_in_ms

> Time after which an instance is evicted from the cache.

> * **Type:** `uint32_t`
> * **Default value:** `5000`
> * Liveness: `False`

<a id="confprop-wasm-cache-instance-size-limit"></a>

### wasm_cache_instance_size_limit

> Instances with size above this limit will not be stored in the cache.

> * **Type:** `size_t`
> * **Default value:** `1024*1024`
> * Liveness: `False`

<a id="confprop-wasm-udf-yield-fuel"></a>

### wasm_udf_yield_fuel

> Wasmtime fuel a WASM UDF can consume before yielding.

> * **Type:** `uint64_t`
> * **Default value:** `100000`
> * Liveness: `False`

<a id="confprop-wasm-udf-total-fuel"></a>

### wasm_udf_total_fuel

> Wasmtime fuel a WASM UDF can consume before termination.

> * **Type:** `uint64_t`
> * **Default value:** `100000000`
> * Liveness: `False`

<a id="confprop-wasm-udf-memory-limit"></a>

### wasm_udf_memory_limit

> How much memory each WASM UDF can allocate at most.

> * **Type:** `size_t`
> * **Default value:** `2*1024*1024`
> * Liveness: `False`

<a id="confprop-relabel-config-file"></a>

### relabel_config_file

> Optionally, read relabel config from file.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-live-updatable-config-params-changeable-via-cql"></a>

### live_updatable_config_params_changeable_via_cql

> If set to true, configuration parameters defined with LiveUpdate can be updated in runtime via CQL (by updating system.config virtual table), otherwise they can’t.

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-auth-superuser-name"></a>

### auth_superuser_name

> Initial authentication super username. Ignored if authentication tables already contain a super user.

> * **Type:** `std::string`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-auth-superuser-salted-password"></a>

### auth_superuser_salted_password

> Initial authentication super user salted password. Create using mkpassword or similar. The hashing algorithm used must be available on the node host.     Ignored if authentication tables already contain a super user password.

> * **Type:** `std::string`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-auth-certificate-role-queries"></a>

### auth_certificate_role_queries

> SUBJECT }, {query

> * **Type:** `std::vector<std::unordered_map<sstring, sstring>>`
> * **Default value:** `{ { { "source"`
> * Liveness: `False`

<a id="confprop-enable-create-table-with-compact-storage"></a>

### enable_create_table_with_compact_storage

> Enable the deprecated feature of CREATE TABLE WITH COMPACT STORAGE.  This feature will eventually be removed in a future version.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-minimum-replication-factor-fail-threshold"></a>

### minimum_replication_factor_fail_threshold

> * **Type:** `int`
> * **Default value:** `-1`
> * Liveness: `True`

<a id="confprop-minimum-replication-factor-warn-threshold"></a>

### minimum_replication_factor_warn_threshold

> * **Type:** `int`
> * **Default value:** `3`
> * Liveness: `True`

<a id="confprop-maximum-replication-factor-fail-threshold"></a>

### maximum_replication_factor_fail_threshold

> * **Type:** `int`
> * **Default value:** `-1`
> * Liveness: `True`

<a id="confprop-maximum-replication-factor-warn-threshold"></a>

### maximum_replication_factor_warn_threshold

> * **Type:** `int`
> * **Default value:** `-1`
> * Liveness: `True`

<a id="confprop-replication-strategy-fail-list"></a>

### replication_strategy_fail_list

> Controls which replication strategies are disallowed to be used when creating/altering a keyspace. Doesn’t affect the pre-existing keyspaces.

> * **Type:** `std::vector<enum_option<replication_strategy_restriction_t>>`
> * **Default value:** `{}`
> * Liveness: `True`

<a id="confprop-replication-strategy-warn-list"></a>

### replication_strategy_warn_list

> Controls which replication strategies to warn about when creating/altering a keyspace. Doesn’t affect the pre-existing keyspaces.

> * **Type:** `std::vector<enum_option<replication_strategy_restriction_t>>`
> * **Default value:** `{locator::replication_strategy_type::simple}`
> * Liveness: `True`

<a id="confprop-write-consistency-levels-disallowed"></a>

### write_consistency_levels_disallowed

> A list of consistency levels that are not allowed for write operations. Requests using these levels will fail.

> * **Type:** `std::vector<enum_option<consistency_level_restriction_t>>`
> * **Default value:** `{}`
> * Liveness: `True`

<a id="confprop-write-consistency-levels-warned"></a>

### write_consistency_levels_warned

> A list of consistency levels that will trigger a warning when used in write operations. Requests using these levels will contain a warning in the query response.

> * **Type:** `std::vector<enum_option<consistency_level_restriction_t>>`
> * **Default value:** `{}`
> * Liveness: `True`

<a id="confprop-tablets-initial-scale-factor"></a>

### tablets_initial_scale_factor

> Minimum average number of tablet replicas per shard per table. Suppressed by tablet options in table’s schema: min_per_shard_tablet_count and min_tablet_count

> * **Type:** `double`
> * **Default value:** `10`
> * Liveness: `True`

<a id="confprop-tablets-per-shard-goal"></a>

### tablets_per_shard_goal

> The goal for the maximum number of tablet replicas per shard. Tablet allocator tries to keep this goal.

> * **Type:** `unsigned`
> * **Default value:** `100`
> * Liveness: `True`

<a id="confprop-target-tablet-size-in-bytes"></a>

### target_tablet_size_in_bytes

> Allows target tablet size to be configured. Defaults to 5G (in bytes). Maintaining tablets at reasonable sizes is important to be able to    redistribute load. A higher value means tablet migration throughput can be reduced. A lower value may cause number of tablets to increase significantly,    potentially resulting in performance drawbacks.

> * **Type:** `uint64_t`
> * **Default value:** `service::default_target_tablet_size`
> * Liveness: `True`

<a id="confprop-tablet-streaming-read-concurrency-per-shard"></a>

### tablet_streaming_read_concurrency_per_shard

> Maximum number of tablets which may be leaving a shard at the same time. Effecting only on topology coordinator. Set to the same value on all nodes.

> * **Type:** `unsigned`
> * **Default value:** `2`
> * Liveness: `True`

<a id="confprop-tablet-streaming-write-concurrency-per-shard"></a>

### tablet_streaming_write_concurrency_per_shard

> Maximum number of tablets which may be pending on a shard at the same time. Effecting only on topology coordinator. Set to the same value on all nodes.

> * **Type:** `unsigned`
> * **Default value:** `2`
> * Liveness: `True`

<a id="confprop-service-levels-interval-ms"></a>

### service_levels_interval_ms

> Controls how often service levels module polls configuration table

> * **Default value:** `10000`
> * Liveness: `True`

<a id="confprop-audit"></a>

### audit

> Controls the audit feature:

> > none   : No auditing enabled.

> > syslog : Audit messages sent to Syslog.

> > table  : Audit messages written to column family named audit.audit_log.
> * **Type:** `sstring`
> * **Default value:** `"table"`
> * Liveness: `False`

<a id="confprop-audit-categories"></a>

### audit_categories

> Comma separated list of operation categories that should be audited.

> * **Type:** `sstring`
> * **Default value:** `"DCL,DDL,AUTH,ADMIN"`
> * Liveness: `True`

<a id="confprop-audit-tables"></a>

### audit_tables

> Comma separated list of table names (<keyspace>.<table>) that will be audited.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `True`

<a id="confprop-audit-keyspaces"></a>

### audit_keyspaces

> Comma separated list of keyspaces that will be audited. All tables in those keyspaces will be audited

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `True`

<a id="confprop-audit-unix-socket-path"></a>

### audit_unix_socket_path

> The path to the unix socket used for writing to syslog. Only applicable when audit is set to syslog.

> * **Type:** `sstring`
> * **Default value:** `"/dev/log"`
> * Liveness: `False`

<a id="confprop-audit-syslog-write-buffer-size"></a>

### audit_syslog_write_buffer_size

> The size (in bytes) of a write buffer used when writing to syslog socket.

> * **Type:** `size_t`
> * **Default value:** `1048576`
> * Liveness: `False`

<a id="confprop-audit-rules"></a>

### audit_rules

> List of granular audit rules. Each rule has: sinks, categories, qualified_table_names, roles.     When non-empty, these rules extend audit_categories, audit_tables, and audit_keyspaces;     events are audited if matched by either mechanism. Prefer audit_rules for new configurations.     Empty categories or roles lists mean ‘match nothing’.     Empty qualified_table_names prevents matching for table-scoped categories (DML, DDL, QUERY)     but has no effect on table-independent categories (AUTH, ADMIN, DCL).     Rule sinks must be a subset of the global ‘audit’ config.     In YAML, use a list of maps. In CQL, use a JSON array of objects.

> * **Type:** `std::vector<audit::audit_rule>`
> * **Default value:** `{}`
> * Liveness: `True`

<a id="confprop-ldap-url-template"></a>

### ldap_url_template

> LDAP URL template used by LDAPRoleManager for crafting queries.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-ldap-attr-role"></a>

### ldap_attr_role

> LDAP attribute containing Scylla role.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-ldap-bind-dn"></a>

### ldap_bind_dn

> Distinguished name used by LDAPRoleManager for binding to LDAP server.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-ldap-bind-passwd"></a>

### ldap_bind_passwd

> Password used by LDAPRoleManager for binding to LDAP server.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-saslauthd-socket-path"></a>

### saslauthd_socket_path

> UNIX domain socket on which saslauthd is listening.

> * **Type:** `sstring`
> * **Default value:** `""`
> * Liveness: `False`

<a id="confprop-object-storage-endpoints"></a>

### object_storage_endpoints

> Object storage endpoints configuration.

> * **Type:** `std::vector<object_storage_endpoint_param>`
> * **Default value:** `{}`
> * Liveness: `True`

<a id="confprop-object-storage-connections-per-shard"></a>

### object_storage_connections_per_shard

> Maximum number of object storage connections per shard.     Connections are distributed proportionally across scheduling groups based on their shares.

> * **Type:** `unsigned`
> * **Default value:** `128`
> * Liveness: `True`

<a id="confprop-topology-barrier-stall-detector-threshold-seconds"></a>

### topology_barrier_stall_detector_threshold_seconds

> Report sites blocking topology barrier if it takes longer than this.

> * **Type:** `double`
> * **Default value:** `2`
> * Liveness: `False`

<a id="confprop-enable-tablets"></a>

### enable_tablets

> Enable tablets for newly created keyspaces. (deprecated)

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-tablets-mode-for-new-keyspaces"></a>

### tablets_mode_for_new_keyspaces

> Control tablets for new keyspaces.  Can be set to the following values:

> > disabled: New keyspaces use vnodes by default, unless enabled by the tablets={‘enabled’:true} option

> > enabled:  New keyspaces use tablets by default, unless disabled by the tablets={‘enabled’:false} option

> > enforced: New keyspaces must use tablets. Tablets cannot be disabled using the CREATE KEYSPACE option
> * **Type:** `enum_option<tablets_mode_t>`
> * **Default value:** `tablets_mode_t::mode::unset`
> * Liveness: `True`

<a id="confprop-auto-repair-enabled-default"></a>

### auto_repair_enabled_default

> Set true to enable auto repair for tablet tables by default. The value will be overridden by the per keyspace or per table configuration which is not implemented yet.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-auto-repair-threshold-default-in-seconds"></a>

### auto_repair_threshold_default_in_seconds

> Set the default time in seconds for the auto repair threshold for tablet tables. If the time since last repair is bigger than the configured time, the tablet is eligible for auto repair. The value will be overridden by the per keyspace or per table configuration which is not implemented yet.

> * **Type:** `int32_t`
> * **Default value:** `24 * 3600`
> * Liveness: `True`

<a id="confprop-view-flow-control-delay-limit-in-ms"></a>

### view_flow_control_delay_limit_in_ms

> The maximal amount of time that materialized-view update flow control may delay responses     to try to slow down the client and prevent buildup of unfinished view updates.     To be effective, this maximal delay should be larger than the typical latencies.     Setting view_flow_control_delay_limit_in_ms to 0 disables view-update flow control.

> * **Type:** `uint32_t`
> * **Default value:** `1000`
> * Liveness: `True`

<a id="confprop-disk-space-monitor-normal-polling-interval-in-seconds"></a>

### disk_space_monitor_normal_polling_interval_in_seconds

> Disk-space polling interval while below polling threshold

> * **Type:** `int`
> * **Default value:** `10`
> * Liveness: `False`

<a id="confprop-disk-space-monitor-high-polling-interval-in-seconds"></a>

### disk_space_monitor_high_polling_interval_in_seconds

> Disk-space polling interval at or above polling threshold

> * **Type:** `int`
> * **Default value:** `1`
> * Liveness: `False`

<a id="confprop-disk-space-monitor-polling-interval-threshold"></a>

### disk_space_monitor_polling_interval_threshold

> Disk-space polling threshold. Polling interval is increased when disk utilization is greater than or equal to this threshold

> * **Type:** `float`
> * **Default value:** `0.9`
> * Liveness: `False`

<a id="confprop-critical-disk-utilization-level"></a>

### critical_disk_utilization_level

> Disk utilization level above which mechanisms preventing a node getting out of space are activated

> * **Type:** `float`
> * **Default value:** `0.98`
> * Liveness: `True`

<a id="confprop-rf-rack-valid-keyspaces"></a>

### rf_rack_valid_keyspaces

> Enforce RF-rack-valid keyspaces. Additionally, if there are existing RF-rack-invalid     keyspaces, attempting to start a node with this option ON will fail.     DEPRECATED. Use enforce_rack_list instead.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-enforce-rack-list"></a>

### enforce_rack_list

> Enforce rack list for tablet keyspaces.     When the option is on, CREATE STATEMENT expands numeric rfs to rack lists     and ALTER STATEMENT is allowed only when rack lists are used in all DCs.    Additionally, if there are existing tablet keyspaces with numeric rf in any DC     attempting to start a node with this option ON will fail.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`

<a id="confprop-tablet-load-stats-refresh-interval-in-seconds"></a>

### tablet_load_stats_refresh_interval_in_seconds

> Tablet load stats refresh rate in seconds.

> * **Type:** `uint32_t`
> * **Default value:** `60`
> * Liveness: `True`

<a id="confprop-force-capacity-based-balancing"></a>

### force_capacity_based_balancing

> Forces the load balancer to perform capacity based balancing, instead of size based balancing.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-size-based-balance-threshold-percentage"></a>

### size_based_balance_threshold_percentage

> Sets the maximum difference in percentages between the most loaded and least loaded nodes, below which the load balancer considers nodes balanced.

> * **Type:** `float`
> * **Default value:** `1.0`
> * Liveness: `True`

<a id="confprop-minimal-tablet-size-for-balancing"></a>

### minimal_tablet_size_for_balancing

> Sets the minimal tablet size for the load balancer. For any tablet smaller than this, the balancer will use this size instead of the actual tablet size.

> * **Type:** `uint64_t`
> * **Default value:** `service::default_target_tablet_size / 100`
> * Liveness: `True`

<a id="confgroup-ungrouped-properties"></a>

## Ungrouped properties

<a id="confprop-memtable-flush-static-shares"></a>

### memtable_flush_static_shares

> If set to higher than 0, ignore the controller’s output and set the memtable shares statically. Do not set this unless you know what you are doing and suspect a problem in the controller. This option will be retired when the controller reaches more maturity.

> * **Type:** `float`
> * **Default value:** `0`
> * Liveness: `True`

<a id="confprop-compaction-static-shares"></a>

### compaction_static_shares

> If set to higher than 0, ignore the controller’s output and set the compaction shares statically. Do not set this unless you know what you are doing and suspect a problem in the controller. This option will be retired when the controller reaches more maturity.

> * **Type:** `float`
> * **Default value:** `0`
> * Liveness: `True`

<a id="confprop-compaction-max-shares"></a>

### compaction_max_shares

> Set the maximum shares of regular compaction to the specific value. Do not set this unless you know what you are doing and suspect a problem in the controller. This option will be retired when the controller reaches more maturity.

> * **Type:** `float`
> * **Default value:** `default_compaction_maximum_shares`
> * Liveness: `True`

<a id="confprop-compaction-enforce-min-threshold"></a>

### compaction_enforce_min_threshold

> If set to true, enforce the min_threshold option for compactions strictly. If false (default), Scylla may decide to compact even if below min_threshold.

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `True`

<a id="confprop-compaction-flush-all-tables-before-major-seconds"></a>

### compaction_flush_all_tables_before_major_seconds

> Set the minimum interval in seconds between flushing all tables before each major compaction (default is 86400).    This option is useful for maximizing tombstone garbage collection by releasing all active commitlog segments.    Set to 0 to disable automatic flushing all tables before major compaction.

> * **Type:** `uint32_t`
> * **Default value:** `86400`
> * Liveness: `False`

<a id="confprop-maintenance-io-throughput-mb-per-sec"></a>

### maintenance_io_throughput_mb_per_sec

> Throttles background I/O to the specified total throughput (in MiBs/s) across the entire system. Background I/O includes the one performed by repair and both RBNO and legacy topology operations such as adding or removing a node. Setting the value to 0 disables background IO throttling. It is recommended to set the value for this parameter to be 75% of network bandwidth

> * **Type:** `uint32_t`
> * **Default value:** `0`
> * Liveness: `True`

<a id="confprop-backup-io-throughput-mb-per-sec"></a>

### backup_io_throughput_mb_per_sec

> Throttles backup I/O to the specified total throughput (in MiBs/s) across the entire system

> * **Type:** `uint32_t`
> * **Default value:** `0`
> * Liveness: `True`

<a id="confprop-default-log-level"></a>

### default_log_level

> Default log level for log messages

> * **Type:** `seastar::log_level`
> * **Default value:** `seastar::log_level::info`
> * Liveness: `False`

<a id="confprop-logger-log-level"></a>

### logger_log_level

> Map of logger name to log level. Valid log levels are ‘error’, ‘warn’, ‘info’, ‘debug’ and ‘trace’

> * **Type:** `std::unordered_map<sstring, seastar::log_level>`
> * **Default value:** `{}`
> * Liveness: `False`

<a id="confprop-log-to-stdout"></a>

### log_to_stdout

> Send log output to stdout

> * **Type:** `bool`
> * **Default value:** `true`
> * Liveness: `False`

<a id="confprop-log-to-syslog"></a>

### log_to_syslog

> Send log output to syslog

> * **Type:** `bool`
> * **Default value:** `false`
> * Liveness: `False`
