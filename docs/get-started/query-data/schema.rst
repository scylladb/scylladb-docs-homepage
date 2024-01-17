============
Schema
============

A schema represents the organization of data in ScyllaDB. 

Keyspace
---------------

A ScyllaDB keyspace contains tables and defines settings for replication.
To create a keyspace, use the following syntax:

.. code::

    CREATE KEYSPACE my_keyspace
      WITH replication = {
        'class': 'NetworkTopologyStrategy',
        'replication_factor': 3
    };

Let's break down the key concepts related to keyspace creation and replication in ScyllaDB.

**Keyspace Creation**

To create a keyspace, you use the ``CREATE KEYSPACE`` command followed by
a keyspace name. In the example above, ``my_keyspace`` is the name of 
the keyspace you want to create.

**Replication Strategy**

Replication in ScyllaDB is the process of storing copies of data across multiple 
nodes to ensure fault tolerance and high availability. The replication strategy 
defines how data should be replicated across nodes in the cluster. In the example 
above, the replication strategy is set to ``NetworkTopologyStrategy``.

This is a commonly used replication strategy in ScyllaDB, especially in 
production deployments. It allows you to specify the number of replicas
for each datacenter separately, which provides fine-grained control over data 
distribution in a multi-datacenter environment.
For example, if you have two datacenters, you can set different replication 
factors for each datacenter to handle data distribution and fault tolerance 
according to your specific requirements.

**Replication Factor**

The replication factor specifies how many copies (or replicas) of each piece of 
data should be stored in the cluster. In the example above, the replication 
factor is set to 3. This means that each piece of data will be replicated to 
three different nodes in the cluster.

The replication factor determines how many copies of your data exist across 
the cluster and directly affects fault tolerance and read performance.

Tables
-------------

Tables hold your data. Define them with specific column types and primary 
keys. Here's how to create a table:

.. code::

    CREATE TABLE my_keyspace.users (
      user_id uuid PRIMARY KEY,
      first_name text,
      last_name text,
      age int
    );

Let's break down the components of this ``CREATE TABLE`` statement:

**Keyspace**

The ``users`` table is created within the ``my_keyspace`` keyspace. This means 
that the ``users`` table belongs to the ``my_keyspace`` keyspace, and all data 
stored in this table will be associated with that keyspace.

**Table**

The name of the table being created is ``users``. This name should be unique within the keyspace.

**Columns**

Columns in ScyllaDB are defined within a table and have a specified data type. 
In the above ``users`` table, ``user_id``, ``first_name``, ``last_name``, and 
``age`` are columns which are further explained as follows:

* ``user_id``: This is a column with the data type ``uuid``. It is defined as 
  the ``PRIMARY KEY``. The primary key uniquely identifies each row in 
  the table and is used for efficient data retrieval.
* ``first_name``: This is a column with the data type ``text``. It is used to store 
  the user's first name.
* ``last_name``: This is another column with the data type ``text``, used to store 
  the user's last name.
* ``age``: This is a column with the data type ``int``, used to store the user's age.

In summary, the ``CREATE TABLE`` statement in ScyllaDB allows you to define 
the structure of your table, including column names, data types, and the primary 
key. This definition is essential for organizing and storing your data 
efficiently within the keyspace.

Primary Keys
--------------

The primary key can be made up of two parts: the partition key and optional 
clustering columns. The ``user_id`` column is the partition key in this example. 
It determines how data gets distributed across the cluster.

Additional columns, if present, can be specified as clustering columns, which 
determine the internal sorting of data within a partition.

.. code::

    CREATE TABLE my_keyspace.orders (
      order_id uuid,
      product_id uuid,
      quantity int,
      PRIMARY KEY (order_id, product_id)
    );

In this example, ``order_id`` is the partition key, and ``product_id`` is 
the clustering key.

Partitions are determined by the partition key, a part of the primary key. 
Data is distributed across nodes based on the partition key. In the ``orders`` 
table, ``order_id`` determines the partition.


Learn More
--------------

* See `Data Definition <https://opensource.docs.scylladb.com/stable/cql/ddl>`_ 
  in the ScyllaDB documentation to learn more about defining a schema in ScyllaDB.
