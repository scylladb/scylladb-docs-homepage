# Features

This document highlights ScyllaDB’s key data modeling features.


            <div class="cell my-panel">
                <div class="panel">
                    <h5 class="panel_\_title">ScyllaDB Features</h5>
            * Secondary Indexes and Materialized Views provide efficient search mechanisms
  on non-partition keys by creating an index.
  * [Global Secondary Indexes](https://docs.scylladb.com/manual/branch-2025.3/features/secondary-indexes.md)
  * [Local Secondary Indexes](https://docs.scylladb.com/manual/branch-2025.3/features/local-secondary-indexes.md)
  * [Materialized Views](https://docs.scylladb.com/manual/branch-2025.3/features/materialized-views.md)
* [Lightweight Transactions](https://docs.scylladb.com/manual/branch-2025.3/features/lwt.md) provide conditional updates
  through linearizability.
* [Counters](https://docs.scylladb.com/manual/branch-2025.3/features/counters.md) are columns that only allow their values
  to be incremented, decremented, read, or deleted.
* [Change Data Capture](https://docs.scylladb.com/manual/branch-2025.3/features/cdc/index.md) allows you to query the current
  state and the history of all changes made to tables in the database.
* [Workload Attributes](https://docs.scylladb.com/manual/branch-2025.3/features/workload-attributes.md) assigned to your workloads
  specify how ScyllaDB will handle requests depending on the workload.
* [Backup and Restore](https://docs.scylladb.com/manual/branch-2025.3/features/backup-and-restore.md) allows you to create
  backups of your data and restore it when needed.

</div></div>
