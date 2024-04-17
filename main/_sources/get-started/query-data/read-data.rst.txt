======================
Reading Data
======================

Use the ``SELECT`` statement to read data. You can specify restrictions with 
the ``WHERE`` clause. For example:

.. code::

    SELECT * FROM my_keyspace.users 
      WHERE user_id = 123e4567-e89b-12d3-a456-426655440000;


Let's break down the components of this ``SELECT`` statement:

**Keyspace and Table**

``my_keyspace.users``: This specifies the keyspace and table from which you 
want to retrieve data. In this example, you are selecting data from a table 
named ``users`` within the ``my_keyspace`` keyspace.

**Columns to Retrieve**
In this example, ``*`` is used as a wildcard character to select all columns 
from the specified table. This means that you want to retrieve all columns of 
data for rows that match the specified restriction.

**WHERE Clause**

``WHERE user_id = 123e4567-e89b-12d3-a456-426655440000``: This part of 
the statement specifies a restriction for filtering the rows to retrieve.

When you execute this ``SELECT`` statement, ScyllaDB will retrieve all columns 
for rows that meet the specified restriction from the ``users`` table within 
the ``my_keyspace`` keyspace. You can use more complex restrictions in 
the ``WHERE`` clause to filter data based on various criteria.

In summary, the ``SELECT`` statement in ScyllaDB is used to query data from 
a table within a keyspace. You can specify which columns to retrieve and apply 
filtering restrictions using the ``WHERE`` clause to fetch specific rows that 
match your criteria.

See the details about the `SELECT statement <https://opensource.docs.scylladb.com/stable/cql/dml/select.html>`_ 
in the ScyllaDB documentation.
