# Metrics Update Between 2025.x and 2026.1

ScyllaDB 2026.1 Dashboards are available as part of the latest [Scylla Monitoring Stack](https://monitoring.docs.scylladb.com).

## New Metrics in 2026.1

The following metrics are new in ScyllaDB 2026.1 compared to 2025.4.

| Metric                                                   | Description                                                                            |
|----------------------------------------------------------|----------------------------------------------------------------------------------------|
| scylla_alternator_operation_size_kb                      | Histogram of item sizes involved in a request.                                         |
| scylla_column_family_total_disk_space_before_compression | Hypothetical total disk space used if data files weren’t compressed                    |
| scylla_group_name_auto_repair_enabled_nr                 | Number of tablets with auto repair enabled.                                            |
| scylla_group_name_auto_repair_needs_repair_nr            | Number of tablets with auto repair enabled that currently need repair.                 |
| scylla_lsa_compact_time_ms                               | Total time spent on segment compaction that was not accounted under `reclaim_time_ms`. |
| scylla_lsa_evict_time_ms                                 | Total time spent on evicting objects that was not accounted under `reclaim_time_ms`,   |
| scylla_lsa_reclaim_time_ms                               | Total time spent in reclaiming LSA memory back to std allocator.                       |
| scylla_object_storage_memory_usage                       | Total number of bytes consumed by the object storage client.                           |
| scylla_tablet_ops_failed                                 | Number of failed tablet auto repair attempts.                                          |
| scylla_tablet_ops_succeeded                              | Number of successful tablet auto repair attempts.                                      |

## Renamed Metrics in 2026.1

The following metrics are renamed in ScyllaDB 2026.1 compared to 2025.4.

| Metric Name in 2025.4   | Metric Name in 2026.1              |
|-------------------------|------------------------------------|
| scylla_s3_memory_usage  | scylla_object_storage_memory_usage |

## Removed Metrics in 2026.1

The following metrics are removed in ScyllaDB 2026.1.

* scylla_redis_current_connections
* scylla_redis_op_latency
* scylla_redis_operation
* scylla_redis_operation
* scylla_redis_requests_latency
* scylla_redis_requests_served
* scylla_redis_requests_serving

## New and Updated Metrics in Previous Releases

* [Metrics Update Between 2025.3 and 2025.4](https://docs.scylladb.com/manual/branch-2025.4/upgrade/upgrade-guides/upgrade-guide-from-2025.x-to-2025.4/metric-update-2025.x-to-2025.4.html)
* [Metrics Update Between 2025.2 and 2025.3](https://docs.scylladb.com/manual/branch-2025.3/upgrade/upgrade-guides/upgrade-guide-from-2025.2-to-2025.3/metric-update-2025.2-to-2025.3.html)
* [Metrics Update Between 2025.1 and 2025.2](https://docs.scylladb.com/manual/branch-2025.2/upgrade/upgrade-guides/upgrade-guide-from-2025.1-to-2025.2/metric-update-2025.1-to-2025.2.html)
