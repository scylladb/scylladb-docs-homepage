# Nodetool excludenode

#### WARNING
You must never use the `nodetool excludenode` on a running node that can be reached by other nodes in the cluster.
Before using the command, make sure the node is permanently down and cannot be recovered.

Running `excludenode` will mark given nodes as permanently down (excluded).
The cluster will no longer attempt to contact excluded nodes, which unblocks
tablet load balancing, replication changes, etc.
The nodes will be permanently banned from the cluster, meaning you won’t be able to bring them back.

Data ownership is not changed, and the nodes are still cluster members,
so have to be eventually removed or replaced.

After nodes are excluded, there is no need to pass them in the list of ignored
nodes to removnenode, replace, or repair.

## Prerequisites

* Using `excludenode` requires at least a quorum of nodes in a cluster to be available.
  If the quorum is lost, it must be restored before you change the cluster topology.
  See [Handling Node Failures](https://docs.scylladb.com/manual/master/troubleshooting/handling-node-failures.md) for details.

## Usage

Provide the Host IDs of the nodes you want to mark as permanently down.

```console
nodetool excludenode  <Host ID> [ ... <Host ID>]
```

Examples:

```console
nodetool excludenode 2d1e1b0a-4ecb-4128-ba45-36ba558f7aee
```

```console
nodetool excludenode 2d1e1b0a-4ecb-4128-ba45-36ba558f7aee 73adf19e-2912-4cf6-b9ab-bbc74297b8de
```

[Nodetool Reference](https://docs.scylladb.com/manual/master/operating-scylla/nodetool.md)
