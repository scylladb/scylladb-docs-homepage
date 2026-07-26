# SSTable 3.0 Format in ScyllaDB

ScyllaDB supports the same SSTable format as Apache Cassandra 3.0.
You can simply place SSTables from a Cassandra data directory into a ScyllaDB uploads directory
and use the `nodetool refresh` command to ingest their data into the table.

Looking more carefully, you will see that ScyllaDB maintains more,
smaller, SSTables than Cassandra does. On ScyllaDB, each core manages its
own subset of SSTables. This internal sharding allows each core (shard)
to work more efficiently, avoiding the complexity and delays of multiple
cores competing for the same data.

## SSTable Format Variants

ScyllaDB 3.x SSTables come in three format variants, selected via the `sstable_format`
parameter in `scylla.yaml`:

`ms`
: Introduces a trie-based SSTable index.
  For details, see [SSTable ms Index (Trie-Based)](https://docs.scylladb.com/manual/master/architecture/sstable/sstable3/sstable-ms-index.md).

`me`
: The baseline 3.x format, default from ScyllaDB 2022.2 through 2026.1.

`md`
: An earlier 3.x variant. Only used when upgrading from an existing `md` cluster.
  The `sstable_format` parameter is ignored if set to `md`.

Existing SSTables are not rewritten automatically when upgrading to 2026.2.
They are upgraded to the `ms` format on the next compaction.

[ScyllaDB Architecture](https://docs.scylladb.com/manual/master/architecture/index.md)

Copyright

© 2016, The Apache Software Foundation.

Apache®, Apache Cassandra®, Cassandra®, the Apache feather logo and the Apache Cassandra® Eye logo are either registered trademarks or trademarks of the Apache Software Foundation in the United States and/or other countries. No endorsement by The Apache Software Foundation is implied by the use of these marks.
