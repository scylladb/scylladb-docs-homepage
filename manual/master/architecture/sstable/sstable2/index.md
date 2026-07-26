# ScyllaDB SSTable - 2.x

[Sorted Strings Table (SSTable)](https://docs.scylladb.com/manual/master/reference/glossary.md#term-SSTable) is the persistent file format used by ScyllaDB and Apache Cassandra. SSTable is saved as a persistent, ordered, immutable set of files on disk.
Immutable means SSTables are never modified; they are created by a MemTable flush and are deleted by a compaction.
The location of ScyllaDB SSTables is specified in scylla.yaml `data_file_directories` parameter (default location: `/var/lib/scylla/data`).

SSTable 3.x is more efficient and requires less disk space than the SSTable 2.x.

For more information on each of the SSTable formats, see below:

* [SSTable 2.x](https://docs.scylladb.com/manual/master/architecture/sstable/sstable2/index.md)
* [SSTable 3.x](https://docs.scylladb.com/manual/master/architecture/sstable/sstable3/index.md)

## SSTable Version Support

| SSTable Version   | ScyllaDB Version   |
|-------------------|--------------------|
| 3.x (‘mt’)        | 2026.2 and above   |
| 3.x (‘ms’)        | 2025.4 and above   |
| 3.x (`me`)        | 2022.2 and above   |
| 3.x (`md`)        | 2021.1             |
* The supported formats are `me` and `mt`.
* The `md` format is used only when upgrading from an existing cluster using
  `md`. The `sstable_format` parameter is ignored if it is set to `md`.
* The `ms` format has been superseded by `mt`, and is used only when upgrading
  from an existing cluster using `ms`. If the `sstable_format` parameter is
  set to `ms`, `mt` files will be written.
* Note: The `sstable_format` parameter specifies the SSTable format used for
  **writes**. The legacy SSTable formats (`ka`, `la`, `mc`) remain
  supported for reads, which is essential for restoring clusters from existing
  backups.

## The ms Format: Trie-Based SSTable Index

The `ms` format introduces a *trie-based* SSTable index.

For a detailed description of the trie index format, see [SSTable ms Index](https://docs.scylladb.com/manual/master/architecture/sstable/sstable3/sstable-ms-index.md).

For more information about ScyllaDB 2.x SSTable formats, see below:

* [SSTable Compression](https://docs.scylladb.com/manual/master/architecture/sstable/sstable2/sstable-compression.md) - Deep dive into ScyllaDB/Apache Cassandra SSTable Compression
* [SSTable Data File](https://docs.scylladb.com/manual/master/architecture/sstable/sstable2/sstable-data-file.md) - Deep dive into ScyllaDB/Apache Cassandra SSTable format
* [SSTable format in ScyllaDB](https://docs.scylladb.com/manual/master/architecture/sstable/sstable2/sstable-format.md) - ScyllaDB SSTables are compatible to those in Apache Cassandra 2.1.8, but why there are more of them?
* [SSTable Interpretation](https://docs.scylladb.com/manual/master/architecture/sstable/sstable2/sstable-interpretation.md) - Deep dive into ScyllaDB/Apache Cassandra SSTable Interpretation in ScyllaDB
* [SSTable Summary File](https://docs.scylladb.com/manual/master/architecture/sstable/sstable2/sstable-summary-file.md) - Deep dive into ScyllaDB/Apache Cassandra SSTable Summary file format

Copyright

© 2016, The Apache Software Foundation.

Apache®, Apache Cassandra®, Cassandra®, the Apache feather logo and the Apache Cassandra® Eye logo are either registered trademarks or trademarks of the Apache Software Foundation in the United States and/or other countries. No endorsement by The Apache Software Foundation is implied by the use of these marks.
