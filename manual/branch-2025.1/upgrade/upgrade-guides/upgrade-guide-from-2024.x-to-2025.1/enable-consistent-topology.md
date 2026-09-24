# Enable Consistent Topology Updates

#### NOTE
The following procedure only applies if:

* You’re upgrading **from ScyllaDB Enterprise 2024.1** to ScyllaDB 2025.1.
* You previously upgraded from 2024.1 to 2024.2 without enabling consistent
  topology updates (see the [2024.2 upgrade guide](https://enterprise.docs.scylladb.com/branch-2024.2/upgrade/upgrade-enterprise/upgrade-guide-from-2024.1-to-2024.2/enable-consistent-topology.html)
  for reference).

## Introduction

ScyllaDB 2025.1 has [consistent topology changes based on Raft](https://docs.scylladb.com/manual/branch-2025.1/architecture/raft.md#raft-topology-changes).
Clusters created with version 2025.1 use consistent topology changes right
from the start. However, consistent topology changes are *not* automatically
enabled in clusters upgraded from version 2024.1. In such clusters, you need to
enable consistent topology changes manually by following the procedure described in this article.

Before you start, you **must** check that the cluster meets the prerequisites
and ensure that some administrative procedures will not be run while
the procedure is in progress.

<a id="enable-raft-topology-2025-1-prerequisites"></a>

## Prerequisites

* Make sure that all nodes in the cluster are upgraded to ScyllaDB 2025.1.
* Verify that [schema on raft is enabled](https://docs.scylladb.com/manual/branch-2025.1/architecture/raft.md#schema-on-raft-enabled).
* Make sure that all nodes enabled `SUPPORTS_CONSISTENT_TOPOLOGY_CHANGES` cluster feature.
  One way to verify it is to look for the following message in the log:
  ```none
  features - Feature SUPPORTS_CONSISTENT_TOPOLOGY_CHANGES is enabled
  ```

  Alternatively, it can be verified programmatically by checking whether the `value`
  column under the `enabled_features` key contains the name of the feature in
  the `system.scylla_local` table. One way to do it is with the following bash script:
  ```bash
  until cqlsh -e "select value from system.scylla_local where key = 'enabled_features'" | grep "SUPPORTS_CONSISTENT_TOPOLOGY_CHANGES"
  do
      echo "Upgrade didn't finish yet on the local node, waiting 10 seconds before checking again..."
      sleep 10
  done
  echo "Upgrade completed on the local node"
  ```
* Make sure that all nodes are alive for the duration of the procedure.

<a id="enable-raft-topology-2025-1-forbidden-operations"></a>

## Administrative operations that must not be running during the procedure

Make sure that administrative operations will not be running while
the procedure is in progress. In particular, you must abstain from:

* [Cluster management procedures](https://docs.scylladb.com/manual/branch-2025.1/operating-scylla/procedures/cluster-management/index.md)
  (adding, replacing, removing, decommissioning nodes, etc.).
* Running [nodetool repair](https://docs.scylladb.com/manual/branch-2025.1/operating-scylla/nodetool-commands/repair.md).
* Running [nodetool checkAndRepairCdcStreams](https://docs.scylladb.com/manual/branch-2025.1/operating-scylla/nodetool-commands/checkandrepaircdcstreams.md).
* Any modifications of [authentication](https://docs.scylladb.com/manual/branch-2025.1/operating-scylla/security/authentication.md) and [authorization](https://docs.scylladb.com/manual/branch-2025.1/operating-scylla/security/enable-authorization.md) settings.
* Any change of authorization via [CQL API](https://docs.scylladb.com/manual/branch-2025.1/operating-scylla/security/authorization.md).
* Schema changes.

## Running the procedure

#### WARNING
Before proceeding, make sure that all the [prerequisites](#enable-raft-topology-2025-1-prerequisites) are met
and no [forbidden administrative operations](#enable-raft-topology-2025-1-forbidden-operations) will run
during the procedure. Failing to do so may put the cluster in an inconsistent state.

1. Issue a POST HTTP request to the `/storage_service/raft_topology/upgrade`
   endpoint to any of the nodes in the cluster.
   For example, you can do it with `curl`:
   ```bash
   curl -X POST "http://127.0.0.1:10000/storage_service/raft_topology/upgrade"
   ```
2. Wait until all nodes report that the procedure is complete. You can check
   whether a node finished the procedure in one of two ways:
   * By sending a HTTP `GET` request on the `/storage_service/raft_topology/upgrade`
     endpoint. For example, you can do it with `curl`:
     ```bash
     curl -X GET "http://127.0.0.1:10000/storage_service/raft_topology/upgrade"
     ```

     It will return a JSON string that will be equal to `done` after the procedure is complete on that node.
   * By querying the `upgrade_state` column in the `system.topology` table.
     You can use `cqlsh` to get the value of the column:
     ```bash
     cqlsh -e "select upgrade_state from system.topology"
     ```

     The `upgrade_state` column should be set to `done` after the procedure
     is complete on that node:

After the procedure is complete on all nodes, wait at least one minute before
issuing any topology changes in order to avoid data loss from writes that were
started before the procedure.

## What if the procedure gets stuck?

If the procedure gets stuck at some point, first check the status of your cluster:

- If there are some nodes that are not alive, try to restart them.
- If all nodes are alive, ensure that the network is healthy and every node can reach all other nodes.
- If all nodes are alive and the network is healthy, perform
  a [rolling restart](https://docs.scylladb.com/manual/branch-2025.1/operating-scylla/procedures/config-change/rolling-restart.md) of the cluster.

If none of the above solves the issue, perform [the Raft recovery procedure](https://docs.scylladb.com/manual/branch-2025.1/troubleshooting/handling-node-failures.md#recovery-procedure).
During recovery, the cluster will switch back to the gossip-based topology management mechanism.

After exiting recovery, you should retry enabling consistent topology updates using
the procedure described in this document.
