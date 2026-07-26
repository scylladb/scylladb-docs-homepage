# Features

This document highlights ScyllaDB’s key data modeling features.


            <div class="cell my-panel">
                <div class="panel">
                    <h5 class="panel_\_title">ScyllaDB Features</h5>
            * Secondary Indexes and Materialized Views provide efficient search mechanisms
  on non-partition keys by creating an index.
  * [Global Secondary Indexes](https://docs.scylladb.com/manual/master/features/secondary-indexes.md)
  * [Local Secondary Indexes](https://docs.scylladb.com/manual/master/features/local-secondary-indexes.md)
  * [Materialized Views](https://docs.scylladb.com/manual/master/features/materialized-views.md)
* [Lightweight Transactions](https://docs.scylladb.com/manual/master/features/lwt.md) provide conditional updates
  through linearizability.
* [Counters](https://docs.scylladb.com/manual/master/features/counters.md) are columns that only allow their values
  to be incremented, decremented, read, or deleted.
* [Change Data Capture](https://docs.scylladb.com/manual/master/features/cdc/index.md) allows you to query the current
  state and the history of all changes made to tables in the database.
* [Workload Attributes](https://docs.scylladb.com/manual/master/features/workload-attributes.md) assigned to your workloads
  specify how ScyllaDB will handle requests depending on the workload.
* [Backup and Restore](https://docs.scylladb.com/manual/master/features/backup-and-restore.md) allows you to create
  backups of your data and restore it when needed.
* [Incremental Repair](https://docs.scylladb.com/manual/master/features/incremental-repair.md) provides a much more
  efficient and lightweight approach to maintaining data consistency by
  repairing only the data that has changed since the last repair.
* [Automatic Repair](https://docs.scylladb.com/manual/master/features/automatic-repair.md) schedules and runs repairs
  directly in ScyllaDB, without external schedulers.
* [Vector Search in ScyllaDB](https://docs.scylladb.com/manual/master/features/vector-search.md) enables
  similarity-based queries on vector embeddings.
* [Full-Text Search](https://docs.scylladb.com/manual/master/features/fulltext-search.md) lets you search and
  rank text columns by relevance using the BM25 scoring algorithm.

</div></div>
