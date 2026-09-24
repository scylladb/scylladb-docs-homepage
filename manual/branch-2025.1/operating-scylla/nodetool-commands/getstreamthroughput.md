# Nodetool getstreamthroughput

**getstreamthroughput** - Print the throughput cap for SSTables streaming in the system

If zero is printed, it means throughput is uncapped

## Syntax

```console
nodetool [options] getstreamthroughput [--mib]
```

## Options

* `--mib` - Print the value in MiB rather than megabits per second

See also

* [setstreamthroughput](https://docs.scylladb.com/manual/branch-2025.1/operating-scylla/nodetool-commands/setstreamthroughput.md)

[Nodetool Reference](https://docs.scylladb.com/manual/branch-2025.1/operating-scylla/nodetool.md)
