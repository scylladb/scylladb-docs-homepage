=============================
Inserting Data
=============================

To insert data, use the ``INSERT INTO`` statement specifying the table and 
the column values. For example:

.. code::

    INSERT INTO my_keyspace.users (user_id, first_name, last_name, age) 
      VALUES (123e4567-e89b-12d3-a456-426655440000, 'Polly', 'Partition', 77);


Let's break down the components of this ``INSERT INTO`` statement:

**Keyspace and Table**

``my_keyspace.users``: This specifies the keyspace and table into which you 
want to insert data. In this example, it's inserting data into a table named 
``users`` within the ``my_keyspace`` keyspace.

**Column Names**

``(user_id, first_name, last_name, age)``: This part of the statement specifies 
the column names in the table to which you want to insert data. 

**VALUES Clause**

``VALUES (123e4567-e89b-12d3-a456-426655440000, 'Polly', 'Partition', 77)``: 
This part of the statement specifies the values that you want to insert into 
the corresponding columns. ``123e4567-e89b-12d3-a456-426655440000`` is being 
inserted into the ``user_id`` column (without quotes) as it is an ``uuid`` data 
type. ``'Polly', 'Partition'`` (enclosed in single quotes) are being inserted into 
the ``first_name``, ``last_name`` columns. ``77`` is being inserted into 
the ``age`` column (without quotes) as it is an ``int`` data type. 

.. note::

  Unlike in SQL, ``INSERT INTO`` does not check the prior existence of the row by default:
  the row is created if none existed before, and updated otherwise.
  This behavior can be changed by using ScyllaDB's
  `Lightweight Transaction <https://opensource.docs.scylladb.com/stable/using-scylla/lwt.html>`_
  ``IF NOT EXISTS`` or ``IF EXISTS`` clauses.

In summary, the ``INSERT INTO`` statement in ScyllaDB is used to insert a new 
row of data into a specific table within a keyspace. It requires you to specify 
the keyspace, table, column names, and the corresponding values that you want 
to insert into those columns. This allows you to add data to your tables in 
ScyllaDB for subsequent retrieval and querying.

See the details about the `INSERT statement <https://opensource.docs.scylladb.com/stable/cql/dml/insert.html>`_ 
in the ScyllaDB documentation.
