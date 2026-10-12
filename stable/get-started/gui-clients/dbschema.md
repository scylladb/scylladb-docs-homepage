# DbSchema

[DbSchema](https://dbschema.com/) is a visual database design and management
tool. After connecting, DbSchema shows your keyspaces, tables, columns, and
column types on a diagram, and lets you run CQL queries.

## Prerequisites

* [DbSchema](https://dbschema.com/download.html)
* A self-hosted ScyllaDB cluster or a [ScyllaDB Cloud](https://cloud.scylladb.com/) cluster

## Connect to ScyllaDB

1. Click **Connect to Database**.
2. Search for **ScyllaDB**.
3. Select **ScyllaDB**.
4. Click **Next**.
5. Enter the connection details:
   * The host and port of a ScyllaDB node (`9042` by default).
   * The datacenter name, as shown by `nodetool status`. For example,
     `datacenter1` on a default single-node cluster.
   * A username and password, if authentication is enabled on the cluster.
6. Click **Connect**.
7. Select the keyspaces you want to work with.
8. Click **OK**.

DbSchema shows the tables in the selected keyspaces on a diagram.

## Run CQL queries

1. Click **Editors** > **SQL Editor**.
2. Write a CQL query.
3. Run the query.

The results appear below the query.

## ScyllaDB Cloud

Find the node addresses, datacenter name, and credentials on the **Connect**
tab of your cluster in the [ScyllaDB Cloud Console](https://cloud.scylladb.com/).
Make sure your IP address is on the cluster’s allowed IP list.
