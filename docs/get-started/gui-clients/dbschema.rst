========
DbSchema
========

`DbSchema <https://dbschema.com/>`_ is a visual database design and management
tool. After connecting, DbSchema shows your keyspaces, tables, columns, and
column types on a diagram, and lets you run CQL queries.

Prerequisites
-------------

* `DbSchema <https://dbschema.com/download.html>`_
* A self-hosted ScyllaDB cluster or a `ScyllaDB Cloud <https://cloud.scylladb.com/>`_ cluster

Connect to ScyllaDB
-------------------

#. Click **Connect to Database**.
#. Search for **ScyllaDB**.
#. Select **ScyllaDB**.
#. Click **Next**.
#. Enter the connection details:

   * The host and port of a ScyllaDB node (``9042`` by default).
   * The datacenter name, as shown by ``nodetool status``. For example,
     ``datacenter1`` on a default single-node cluster.
   * A username and password, if authentication is enabled on the cluster.

#. Click **Connect**.
#. Select the keyspaces you want to work with.
#. Click **OK**.

DbSchema shows the tables in the selected keyspaces on a diagram.

Run CQL queries
---------------

#. Click **Editors** > **SQL Editor**.
#. Write a CQL query.
#. Run the query.

The results appear below the query.

ScyllaDB Cloud
--------------

Find the node addresses, datacenter name, and credentials on the **Connect**
tab of your cluster in the `ScyllaDB Cloud Console <https://cloud.scylladb.com/>`_.
Make sure your IP address is on the cluster's allowed IP list.
