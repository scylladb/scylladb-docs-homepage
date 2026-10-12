# LibreDB Studio

[LibreDB Studio](https://github.com/libredb/libredb-studio) is an open
source, web-based SQL IDE that you run yourself.

## Prerequisites

* [LibreDB Studio](https://libredb.org/#deploy)
* A self-hosted ScyllaDB cluster or a [ScyllaDB Cloud](https://cloud.scylladb.com/) cluster

## Connect to ScyllaDB

1. Open the connection dialog.
2. Select **Apache Cassandra**.
3. Enter the connection details:
   * **Host** and **Port**: the address of a ScyllaDB node and `9042` by default.
   * **Local Data Center**: required by the driver. Use the datacenter name
     that `nodetool status` shows, for example `datacenter1` on a default
     single-node cluster.
   * **Keyspace**: optional. Without a keyspace, the object browser doesn’t
     show a schema tree.
   * A username and password, if authentication is enabled on the cluster.
4. Click **Test Connection** to verify the connection.
5. Click **Establish Connection**.

You can now run CQL statements in the editor and browse keyspaces, tables,
materialized views, columns, and secondary indexes in the object browser.

## ScyllaDB Cloud

Find the node addresses, datacenter name, and credentials on the **Connect**
tab of your cluster in the [ScyllaDB Cloud Console](https://cloud.scylladb.com/).
Make sure the IP address of the machine running LibreDB Studio is on the
cluster’s allowed IP list.
