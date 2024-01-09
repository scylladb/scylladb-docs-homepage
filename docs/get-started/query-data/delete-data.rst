=======================
Deleting Data
=======================

Delete data with the ``DELETE`` statement. Be specific with your conditions to 
avoid accidental deletions. For example:

.. code::

    DELETE FROM my_keyspace.users 
     WHERE user_id = 123e4567-e89b-12d3-a456-426655440000;

Let's break down the components of this ``DELETE`` statement:

**Keyspace and Table**

``my_keyspace.users``: This specifies the keyspace and table from which you 
want to delete data. In this example, you are deleting data from a table named 
``my_table`` within the ``my_keyspace`` keyspace.

**WHERE Clause**
``WHERE user_id = 123e4567-e89b-12d3-a456-426655440000``: This part of 
the statement specifies a condition for filtering the rows to be deleted.

Including the ``WHERE`` clause with a specific condition is essential to ensure 
that only the rows meeting the condition will be deleted. This is done to 
prevent accidental deletions of all data in the table.

In summary, the ``DELETE`` statement in ScyllaDB is used to remove existing 
data from a table. Always use a ``WHERE`` clause with a suitable condition to 
target the specific rows you want to delete, and ensure that the condition is 
specific enough to avoid unintended data loss. This approach helps maintain 
data integrity in your ScyllaDB tables.

See the details about the `DELETE statement <https://opensource.docs.scylladb.com/stable/cql/dml/delete.html>`_ 
in the ScyllaDB documentation.


