# Nodetool statusbackup

**statusbackup** - Displays the incremental backup status.

#### WARNING
Incremental backup is deprecated, and support for it may be removed in a future release.
Use [snapshots](https://docs.scylladb.com/manual/master/operating-scylla/procedures/backup-restore/backup.md) and
[ScyllaDB Manager](https://manager.docs.scylladb.com/stable/backup/) to back up your data instead.

For example:

`nodetool statusbackup`

Results can be one of the following:`running` Or `not running`

By default, the incremental backup status is `not running`

See also

* [disablebackup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/disablebackup.md)
* [enablebackup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/enablebackup.md)

[Nodetool Reference](https://docs.scylladb.com/manual/master/operating-scylla/nodetool.md)
