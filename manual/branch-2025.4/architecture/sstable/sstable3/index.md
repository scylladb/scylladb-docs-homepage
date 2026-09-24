# ScyllaDB SSTable - 3.x

[Sorted Strings Table (SSTable)](https://docs.scylladb.com/manual/branch-2025.4/reference/glossary.md#term-SSTable) is the persistent file format used by ScyllaDB and Apache Cassandra. SSTable is saved as a persistent, ordered, immutable set of files on disk.
Immutable means SSTables are never modified; they are created by a MemTable flush and are deleted by a compaction.
The location of ScyllaDB SSTables is specified in scylla.yaml `data_file_directories` parameter (default location: `/var/lib/scylla/data`).

SSTable 3.x is more efficient and requires less disk space than the SSTable 2.x.

## SSTable Version Support

| SSTable Version   | ScyllaDB Version   |
|-------------------|--------------------|
| 3.x (‘ms’)        | 2025.4 and above   |
| 3.x (‘me’)        | 2022.2 and above   |
| 3.x (‘md’)        | 2021.1             |
* The supported formats are `me` and `ms`.
* The `md` format is used only when upgrading from an existing cluster using
  `md`. The `sstable_format` parameter is ignored if it is set to `md`.
* Note: The `sstable_format` parameter specifies the SSTable format used for
  **writes**. The legacy SSTable formats (`ka`, `la`, `mc`) remain
  supported for reads, which is essential for restoring clusters from existing
  backups.

## Additional Information

For more information on ScyllaDB 3.x SSTable formats, see below:

* [SSTable 3.0 Data File Format](https://docs.scylladb.com/manual/branch-2025.4/architecture/sstable/sstable3/sstables-3-data-file-format.md)
* [SSTable 3.0 Statistics](https://docs.scylladb.com/manual/branch-2025.4/architecture/sstable/sstable3/sstables-3-statistics.md)
* [SSTable 3.0 Summary](https://docs.scylladb.com/manual/branch-2025.4/architecture/sstable/sstable3/sstables-3-summary.md)
* [SSTable 3.0 Index](https://docs.scylladb.com/manual/branch-2025.4/architecture/sstable/sstable3/sstables-3-index.md)
* [SSTable 3.0 Format in ScyllaDB](https://docs.scylladb.com/manual/branch-2025.4/architecture/sstable/sstable3/sstable-format.md)
