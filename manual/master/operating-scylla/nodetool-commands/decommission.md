# nodetool decommission

**decommission** - Deactivate a selected node by streaming its data to the next node in the ring.

For example:

`nodetool decommission`

Use the `nodetool netstats` command to monitor the progress of the token reallocation.

#### NOTE
You cannot decomission a node if any existing node is down.

See [Remove a Node from a ScyllaDB Cluster (Down Scale)](https://docs.scylladb.com/manual/master/operating-scylla/procedures/cluster-management/remove-node.md)
for procedure details.

Before you run `nodetool decommission`:

* Review current disk space utilization on existing nodes and make sure the amount
  of data streamed from the node being removed can fit into the disk space available
  on the remaining nodes. If there is not enough disk space on the remaining nodes,
  the removal of a node will fail. Add more storage to remaining nodes **before**
  starting the removal procedure.
* Make sure that the number of nodes remaining in the DC after you decommission a node
  will be the same or higher than the Replication Factor configured for the keyspace
  in this DC. Please mind that e.g. audit feature, which is enabled by default, may require
  adjusting `audit` keyspace. If the number of remaining nodes is lower than the RF, the decommission
  request may fail.
  In such a case, ALTER the keyspace to reduce the RF before running `nodetool decommission`.

It’s allowed to invoke `nodetool decommission` on multiple nodes in parallel. This will be faster than doing
it sequentially if there is significant amount of data in tablet-based keyspaces, because
tablets are migrated from nodes in parallel. Decommission process first migrates tablets away, and this
part is done in parallel for all nodes being decommissioned. Then it does the vnode-based decommission, and
this part is serialized with other vnode-based operations, including those from other decommission operations.

Decommission which is still in the tablet draining phase can be canceled using Task Manager API.
See [Task manager](https://docs.scylladb.com/manual/master/operating-scylla/admin-tools/task-manager.md).

See also:

* [Remove a Node from a ScyllaDB Cluster (Down Scale)](https://docs.scylladb.com/manual/master/operating-scylla/procedures/cluster-management/remove-node.md)
* [Decommissioning a Data Center](https://docs.scylladb.com/manual/master/operating-scylla/procedures/cluster-management/decommissioning-data-center.md)
* [Replace a Running Node](https://docs.scylladb.com/manual/master/operating-scylla/procedures/cluster-management/replace-running-node.md)
* [Failed Decommission Troubleshooting](https://docs.scylladb.com/manual/master/troubleshooting/failed-decommission.md)

[Nodetool Reference](https://docs.scylladb.com/manual/master/operating-scylla/nodetool.md)
