# Nodetool scrub

## NAME

**scrub** - Help identify and fix corrupted SSTable. Not all kinds of corruption can be skipped or fixed by scrub.
Remove faulty data, eliminate tombstoned rows that have surpassed the table’s gc_grace period, and fix out-of-order rows and partitions.

## SYNOPSIS

```shell
           nodetool [(-h <host> | --host <host>)] [(-p <port> | --port <port>)]
                [(-pp | --print-port)] [(-pw <password> | --password <password>)]
                [(-pwf <passwordFilePath> | --password-file <passwordFilePath>)]
                [(-ns | --no-snapshot)]
                [(-s | --skip-corrupted)]
                [(-m <scrub_mode> | --mode <scrub_mode>)]
                [(-q <quarantine_mode> | --quarantine-mode <quarantine_mode>)]
                [--drop-unfixable-sstables]
                [--] <keyspace> [<table...>]

Supported scrub modes: VALIDATE, ABORT, SKIP, SEGREGATE
Supported quarantine modes: INCLUDE, EXCLUDE, ONLY
```

## OPTIONS

| Parameter                                                      | Description                                                                                                                 |
|----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| `-ns` / `--no-snapshot`                                        | Do not take a snapshot of all scrubbed tables before starting scrub (default false).                                        |
| `-s` / `--skip-corrupted`                                      | Skip corrupted rows or partitions even when scrubbing counter tables.<br/>(Deprecated, use `--mode` instead. default false) |
| `-m <scrub_mode>` / `--mode <scrub_mode>`                      | How to handle corrupt data (one of: VALIDATE|ABORT|SKIP|SEGREGATE, default VALIDATE; overrides `--skip-corrupted`)          |
| `-q <quarantine_mode>` / `--quarantine-mode <quarantine_mode>` | How to handle quarantined SSTables (one of: INCLUDE|EXCLUDE|ONLY, default INCLUDE)                                          |
| `--drop-unfixable-sstables`                                    | Drop unfixable SSTables instead of aborting the entire scrub (only valid with `--mode=SEGREGATE`)                           |
| `--quarantine-invalid-sstables <true|false>`                   | Should corrupt sstables be quarantined (default true, only valid with `--mode=VALIDATE`)                                    |

`--` This option can be used to separate command-line options from the list of argument, (useful when arguments might be mistaken for command-line options.

`<keyspace>` The keyspace to scrub.

`[<table...>]` Optional. One or more tables to scrub.  By default, all tables in the keyspace are scrubbed.

## SCRUB MODES

| Scrub mode   | Description                                                                                                                                                                                                                                                                                                          |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| VALIDATE     | Read-only mode: report any corruptions found while scrubbing but do not fix them.<br/>Additionally, validate component integrity by verifying the stored digests if available.<br/>By default, corrupt SSTables are moved into a “quarantine” subdirectory so they will not be subject to compaction.<br/>(default). |
| ABORT        | Abort scrubbing when the first validation error occurs.                                                                                                                                                                                                                                                              |
| SKIP         | Skip corrupted rows or partitions. (equivalent to the legacy –skip-corrupted option).<br/>**Warning**: This mode can cause data loss by removing invalid data portions or entire<br/>SSTables if severely corrupted (e.g., digest mismatch detected).                                                                |
| SEGREGATE    | Sort out-of-order rows or partitions by segregating them into additional SSTables.                                                                                                                                                                                                                                   |

## QUARANTINE MODES

| Quarantine mode   | Description                                              |
|-------------------|----------------------------------------------------------|
| INCLUDE           | Process both regular and quarantined SSTables (default). |
| EXCLUDE           | Process only regular (non-quarantined) SSTables.         |
| ONLY              | Process only quarantined SSTables.                       |

## Examples

Scrub **all** tables in a keyspace (mykeyspace)

```shell
> nodetool scrub mykeyspace
```

Scrub **a** specific table (mytable) in a keyspace (mykeyspace)

```shell
> nodetool scrub mykeyspace mytable
```

Scrub **a** specific table (mytable) in a keyspace (mykeyspace) in SEGREGATE mode

```shell
> nodetool scrub -m SEGREGATE mykeyspace mytable
```

Scrub **a** specific table (mytable) in a keyspace (mykeyspace) in VALIDATE mode without taking a preliminary snapshot

```shell
> nodetool scrub --no-snapshot mykeyspace mytable
```

Scrub **a** specific table (mytable) in a keyspace (mykeyspace) in SEGREGATE mode dropping unfixable SSTables

```shell
> nodetool scrub -m SEGREGATE --drop-unfixable-sstables mykeyspace mytable
```

## Procedures for Removing Bad SSTables

### Method 1: Quarantine and Drop

**Step 1**: Run scrub in VALIDATE mode to identify and quarantine corrupted SSTables:

```shell
> nodetool scrub keyspace_name table_name
```

This will move corrupted SSTables to a `quarantine` directory.
The `quarantine` directory is a sub-directory of the table’s respective data directory.
Quarantined SSTables are handled distinctly:

* They participate in reads.
* They participate in streaming and data migration.
* They participate in repairs.
* They do not participate in compaction, but participate in overlap checks for
  the purpose of tombstone-gc.

The purpose of the quarantine is to keep corrupt SSTables out of compaction, which can spread the compaction or can get in a fail-retry loop. It also makes corrupt SSTables easy to find and retrieve for investigation.

It is possible to opt-out from quarantining SSTables by passing `--quarantine-invalid-sstables=false` to nodetool.

**Step 2** (Optional): Preserve quarantined SSTables for analysis:

Before permanently dropping the corrupted SSTables, consider copying some or all of them aside,
somewhere outside of the ScyllaDB data directory, so they are preserved for later investigation by the ScyllaDB R&D team,
to determine the root cause of the corruption.

```shell
# Copy quarantined SSTables to a backup location for analysis
> cp -r /path/to/data/keyspace_name/table_dir/quarantine /path/to/backup/location/
```

**Step 3**: Drop the quarantined SSTables using [dropquarantinedsstables](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/dropquarantinedsstables.md):

```shell
> nodetool dropquarantinedsstables keyspace_name table_name
```

This permanently removes the quarantined SSTables from the specified table.

### Method 2: Segregate with Drop Unfixable Flag

This approach attempts to fix what can be fixed and automatically drops SSTables that cannot be fixed.

#### NOTE
This method should be used for the subset of corruption issues where SEGREGATE mode can actually help: where corruption manifests at least partly in reordered partitions or rows.

**Step 1**: Run scrub in SEGREGATE mode with the `--drop-unfixable-sstables` flag:

```shell
> nodetool scrub -m SEGREGATE --drop-unfixable-sstables keyspace_name table_name
```

This will:

- Attempt to segregate and fix out-of-order data where possible
- Remove faulty data
- Automatically drop SSTables that cannot be fixed
- Create new properly ordered SSTables from the recoverable data

Copyright

© 2016, The Apache Software Foundation.

Apache®, Apache Cassandra®, Cassandra®, the Apache feather logo and the Apache Cassandra® Eye logo are either registered trademarks or trademarks of the Apache Software Foundation in the United States and/or other countries. No endorsement by The Apache Software Foundation is implied by the use of these marks.
