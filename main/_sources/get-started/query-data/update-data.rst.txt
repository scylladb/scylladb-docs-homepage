===================
Updating Data
===================

Update data using the ``UPDATE`` statement. For example:

.. code::

    UPDATE my_keyspace.users SET age = 78 
      WHERE user_id = 123e4567-e89b-12d3-a456-426655440000;

Let's break down the components of this ``UPDATE`` statement:

**Keyspace and Table**

``my_keyspace.users``: This specifies the keyspace and table from which you 
want to update data. In this example, you are updating data in a table named 
``my_table`` within the ``my_keyspace`` keyspace.

**Column Update**

``SET age = 78``: This part of the statement specifies the update operation. 
You are setting the value of the age column to ``78`` for rows that match 
the specified restriction.

**WHERE Clause**

``WHERE user_id = 123e4567-e89b-12d3-a456-426655440000``: This part of 
the statement specifies the affected partition key, which is mandatory.

.. note::

  Unlike in SQL, ``UPDATE`` does not check the prior existence of the row by default:
  the row is created if none existed before, and updated otherwise.
  This behavior can be changed by using ScyllaDB's
  `Lightweight Transaction <https://opensource.docs.scylladb.com/stable/using-scylla/lwt.html>`_
  ``IF NOT EXISTS`` or ``IF EXISTS`` clauses.

In summary, the ``UPDATE`` statement in ScyllaDB is used to modify existing 
data in a table. Always include a ``WHERE`` clause with a suitable restriction 
to target the specific rows you want to update, and specify the changes you 
want to make using the SET clause. This helps you ensure the accuracy and 
precision of your updates.

See the details about the `UPDATE statement <https://opensource.docs.scylladb.com/stable/cql/dml/update.html>`_ 
in the ScyllaDB documentation.
