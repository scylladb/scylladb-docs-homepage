# DBeaver

[DBeaver](https://dbeaver.com/) is a universal database manager for SQL and
NoSQL databases. It has a built-in ScyllaDB connection in the paid editions
(DBeaver Lite, Enterprise, and Ultimate), so you can browse tables and run CQL
queries with syntax highlighting.

## Prerequisites

* [DBeaver Lite, Enterprise, or Ultimate](https://dbeaver.com/download/)
* A self-hosted ScyllaDB cluster or a [ScyllaDB Cloud](https://cloud.scylladb.com/) cluster

## Connect to ScyllaDB

1. Click **New Database Connection**.
2. Search for **ScyllaDB**.
3. Select **ScyllaDB**.
4. Click **Next**.
5. Enter the connection details:
   * **Host**: the address of a ScyllaDB node.
   * **Port**: `9042` by default.
   * **Keyspace**: optional.
   * **Username** and **Password**: if authentication is enabled on the cluster.
6. Click **Test Connection** to verify the connection.
7. Click **Finish**.

You can now browse your keyspaces and tables in the **Database Navigator**
and open a SQL editor to run CQL queries. Results appear below the query.

## ScyllaDB Cloud

Find the node addresses and credentials on the **Connect** tab of your cluster
in the [ScyllaDB Cloud Console](https://cloud.scylladb.com/). Make sure your
IP address is on the cluster’s allowed IP list.
