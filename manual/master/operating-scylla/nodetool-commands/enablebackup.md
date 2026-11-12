# Nodetool enablebackup

**enablebackup** - Enables incremental backup.

#### WARNING
Incremental backup is deprecated, and support for it may be removed in a future release.
Use [snapshots](https://docs.scylladb.com/manual/master/operating-scylla/procedures/backup-restore/backup.md) and
[ScyllaDB Manager](https://manager.docs.scylladb.com/stable/backup/) to back up your data instead.

For example:

`nodetool enablebackup`

By default, the incremental backup status is `not running`

See also

* [statusbackup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/statusbackup.md)
* [disablebackup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/disablebackup.md)

[Nodetool Reference](https://docs.scylladb.com/manual/master/operating-scylla/nodetool.md)
