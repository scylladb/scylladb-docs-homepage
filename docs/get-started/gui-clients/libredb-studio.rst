==============
LibreDB Studio
==============

`LibreDB Studio <https://github.com/libredb/libredb-studio>`_ is an
open-source, web-based SQL IDE that you run yourself.

Prerequisites
-------------

* `LibreDB Studio <https://libredb.org/#deploy>`__
* A self-hosted ScyllaDB cluster or a `ScyllaDB Cloud <https://cloud.scylladb.com/>`_ cluster

Connect to ScyllaDB
-------------------

#. Open the connection dialog.
#. Select **Apache Cassandra**.
#. Enter the connection details:

   * **Host** and **Port**: the address of a ScyllaDB node and ``9042`` by default.
   * **Local Data Center**: required by the driver. Use the datacenter name
     that ``nodetool status`` shows, for example ``datacenter1`` on a default
     single-node cluster.
   * **Keyspace**: optional. Without a keyspace, the object browser doesn't
     show a schema tree.
   * A username and password, if authentication is enabled on the cluster.

#. Click **Test Connection** to verify the connection.
#. Click **Establish Connection**.

You can now run CQL statements in the editor and browse keyspaces, tables,
materialized views, columns, and secondary indexes in the object browser.

ScyllaDB Cloud
--------------

Find the node addresses, datacenter name, and credentials on the **Connect**
tab of your cluster in the `ScyllaDB Cloud Console <https://cloud.scylladb.com/>`_.
Make sure the IP address of the machine running LibreDB Studio is on the
cluster's allowed IP list.
