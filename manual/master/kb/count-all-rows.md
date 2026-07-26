# Counting all rows in a table is slow

**Audience: ScyllaDB users**

Trying to count all rows in a table using

```cql
SELECT COUNT(1) FROM ks.table;
```

may fail with the **ReadTimeout** error.

COUNT() runs a full-scan query on all nodes, which might take a long time to finish. As a result, the count time may be greater than the ScyllaDB query timeout.
One way to prevent that issue is to increase the timeout for the query using the [USING TIMEOUT](https://docs.scylladb.com/manual/master/cql/dml/select.md#using-timeout) directive, for example:

```cql
SELECT COUNT(1) FROM ks.table USING TIMEOUT 120s;
```

You can also get an *estimation* of the number **of partitions** (not rows) with [nodetool tablestats](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/tablestats.md).
