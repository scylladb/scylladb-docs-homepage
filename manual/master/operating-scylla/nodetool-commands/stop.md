# Nodetool stop compaction

Stops a compaction operation. This command is usually used to stop compaction that has a negative impact on the performance of a node.

Usage

```sh
nodetool <options> stop -- <compaction_type>
```

Supported compaction types:

| Type         | Stops                                                                                                                                            |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| `COMPACTION` | Regular (automatic) compactions and major compactions                                                                                            |
| `REGULAR`    | Regular (automatic) compactions only                                                                                                             |
| `MAJOR`      | Major compactions only                                                                                                                           |
| `CLEANUP`    | Cleanup compactions (see [nodetool cleanup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/cleanup.md))              |
| `SCRUB`      | Scrub compactions (see [nodetool scrub](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/scrub.md))                    |
| `UPGRADE`    | SSTable upgrades (see [nodetool upgradesstables](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/upgradesstables.md)) |
| `RESHAPE`    | Reshape compactions                                                                                                                              |
| `SPLIT`      | Tablet split compactions                                                                                                                         |

Stopping a compaction by id (`--id <id>`) is not implemented.

For example:

```sh
nodetool stop COMPACTION

nodetool stop REGULAR

nodetool stop MAJOR

nodetool stop RESHAPE
```

[Nodetool Reference](https://docs.scylladb.com/manual/master/operating-scylla/nodetool.md)
