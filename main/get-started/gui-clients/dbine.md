# DBine

[DBine](https://dbine.com) is a free, open source (Apache 2.0) desktop database
manager for Windows, macOS, and Linux.

## Prerequisites

* [DBine](https://github.com/addlayer-io/dbine/releases)
* A self-hosted ScyllaDB cluster or a [ScyllaDB Cloud](https://cloud.scylladb.com/) cluster

## Connect to ScyllaDB

1. Create a new connection.
2. Search for **ScyllaDB** and select it.
3. Enter the connection details:
   * **Host** and **Port**: one or more ScyllaDB nodes, separated by commas,
     and `9042` by default.
   * **Keyspace**: optional.
   * **User** and **Password**, if authentication is enabled on the cluster.
   * **Encrypt the connection (TLS)**, if client encryption is enabled on the
     cluster.
   * **Local datacenter**: optional, on the **Advanced** tab. Use the
     datacenter name that `nodetool status` shows, for example
     `datacenter1` on a default single-node cluster.
4. Click **Test connection** to verify the connection.
5. Click **Save and connect**.

You can now browse keyspaces, tables, materialized views, and columns in the
explorer, and run CQL statements in the editor, with autocompletion.

## ScyllaDB Cloud

Find the node addresses, datacenter name, and credentials on the **Connect**
tab of your cluster in the [ScyllaDB Cloud Console](https://cloud.scylladb.com/).
Make sure the IP address of the machine running DBine is on the cluster’s
allowed IP list.
