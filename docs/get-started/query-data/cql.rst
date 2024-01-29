=================
CQL
=================

CQL, or Cassandra Query Language, is a query language for interacting with 
ScyllaDB, which is similar in syntax and usage to SQL for relational 
databases. It allows you to define, query, and modify data. CQL is designed 
to be simple and intuitive, making it easier for those familiar with SQL to 
transition to working with ScyllaDB.

Learning and mastering CQL is crucial for designing queries. 
See the `ScyllaDB documentation <https://opensource.docs.scylladb.com/stable/cql/index.html>`_
for CQL reference and CQL-related topics.

Using cqlsh
------------

cqlsh is a command-line shell for interacting with ScyllaDB through CQL. It 
provides an interface to run CQL commands and scripts. cqlsh connects to 
a ScyllaDB node and allows you to execute CQL commands directly. This tool is 
essential for database management tasks and querying data.

You can connect to the node you started earlier in this guide, with cqlsh 
using the following command:

.. code::

    docker exec -it scylla cqlsh

The output of this command will look something like this:

.. code::

    Connected to  at 172.17.0.2:9042.
    [cqlsh 5.0.1 | Cassandra 3.0.8 | CQL spec 3.3.1 | Native protocol v4]
    Use HELP for help.
    cqlsh>

See `CQLSh: the CQL shell <https://opensource.docs.scylladb.com/master/cql/cqlsh.html>`_ 
for details.
