# Metrics Update Between 2024.x and 2025.1

ScyllaDB Enterprise 2025.1 Dashboards are available as part of the latest [Scylla Monitoring Stack](https://monitoring.docs.scylladb.com).

## New Metrics

The following metrics are new in ScyllaDB 2025.1 compared to 2024.x:

| Metric                                                  | Description                                                 |
|---------------------------------------------------------|-------------------------------------------------------------|
| scylla_alternator_batch_item_count                      | The total number of items processed across all batches.     |
| scylla_hints_for_views_manager_sent_bytes_total         | The total size of the sent hints (in bytes).                |
| scylla_hints_manager_sent_bytes_total                   | The total size of the sent hints (in bytes).                |
| scylla_io_queue_activations                             | The number of times the class was woken up from idle.       |
| scylla_raft_apply_index                                 | The applied index.                                          |
| scylla_raft_commit_index                                | The commit index.                                           |
| scylla_raft_log_last_index                              | The index of the last log entry.                            |
| scylla_raft_log_last_term                               | The term of the last log entry.                             |
| scylla_raft_snapshot_last_index                         | The index of the snapshot.                                  |
| scylla_raft_snapshot_last_term                          | The term of the snapshot.                                   |
| scylla_raft_state                                       | The current state: 0 - follower, 1 - candidate, 2 - leader  |
| scylla_rpc_client_delay_samples                         | The total number of delay samples.                          |
| scylla_rpc_client_delay_total                           | The total delay in seconds.                                 |
| scylla_storage_proxy_replica_received_hints_bytes_total | The total size of hints and MV hints received by this node. |
| scylla_storage_proxy_replica_received_hints_total       | The number of hints and MV hints received by this node.     |

## Renamed Metrics

The following metrics are renamed in ScyllaDB 2025.1 compared to 2024.x:

| 2024.2                                                    | 2025.1                                                      |
|-----------------------------------------------------------|-------------------------------------------------------------|
| scylla_hints_for_views_manager_sent                       | scylla_hints_for_views_manager_sent_total                   |
| scylla_hints_manager_sent                                 | scylla_hints_manager_sent_total                             |
| scylla_forward_service_requests_dispatched_to_other_nodes | scylla_mapreduce_service_requests_dispatched_to_other_nodes |
| scylla_forward_service_requests_dispatched_to_own_shards  | scylla_mapreduce_service_requests_dispatched_to_own_shards  |
| scylla_forward_service_requests_executed                  | scylla_mapreduce_service_requests_executed                  |
