# Nodetool status

**status** - This command prints the cluster information for a single keyspace or all keyspaces.

The keyspace argument is required to calculate effective ownership information (`Owns` column).
For tablet keyspaces, a table is also required for effective ownership.

For example:

```default
nodetool status my_keyspace
```

Example output:

```console
Datacenter: datacenter1
=======================
Status=Up/Down/eXcluded
|/ State=Normal/Leaving/Joining/Moving
--  Address    Load       Tokens  Owns (effective)  Host ID                               Rack
UN  127.0.0.1  394.97 MB  256     33.4%             292a6c7f-2063-484c-b54d-9015216f1750  rack1
UN  127.0.0.2  151.07 MB  256     34.3%             102b6ecd-2081-4073-8172-bf818c35e27b  rack1
UN  127.0.0.3  249.07 MB  256     32.3%             20db6ecd-2981-447s-l172-jf118c17o27y  rack1
XN  127.0.0.4  149.07 MB  256     32.3%             dd961642-c7c6-4962-9f5a-ea774dbaed77  rack1
```

| Parameter   | Description                                                                                                                                                                                                                                      |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Datacenter  | The data center that holds<br/>the information.                                                                                                                                                                                                  |
| Status      | `U` - The node is up.<br/><br/>`D` - The node is down.<br/><br/>`X` - The node is [excluded](#status-excluded).                                                                                                                                  |
| State       | `N` - Normal<br/><br/>`L` - Leaving<br/><br/>`J` - Joining<br/><br/>`M` - Moving                                                                                                                                                                 |
| Address     | The IP address of the node.                                                                                                                                                                                                                      |
| Load        | The size on disk the ScyllaDB data<br/>: takes up (updates every 60 seconds).                                                                                                                                                                    |
| Tokens      | The number of tokens per node.                                                                                                                                                                                                                   |
| Owns        | The percentage of data owned by<br/>the node (per datacenter) multiplied by<br/>the replication factor you are using.<br/><br/>For example, if the node owns 25% of<br/>the data and the replication factor<br/>is 4, the value will equal 100%. |
| Host ID     | The unique identifier (UUID)<br/>automatically assigned to the node.                                                                                                                                                                             |
| Rack        | The name of the rack.                                                                                                                                                                                                                            |

<a id="status-excluded"></a>

Nodes in the excluded status (`X`) are down nodes which were marked as excluded
by `removenode`, `excludenode`` or node replace, and means that they are considered permanently lost.
See [nodetool excludenode](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/excludenode.md) for more information.

[Nodetool Reference](https://docs.scylladb.com/manual/master/operating-scylla/nodetool.md)
