====================
Query Design
====================

Your data model is heavily influenced by query efficiency. Effective partitioning,
clustering columns and denormalization are key considerations for optimizing data
access patterns.

The way data is partitioned plays a pivotal role in how it’s accessed. An efficient
partitioning strategy ensures that data is evenly distributed across the cluster,
minimizing hotspots. For example:

.. code::

  CREATE TABLE my_keyspace.user_activities_bad (
    user_id uuid,
    activity_date date,
    log_time timestamp,
    activity_details text,
    PRIMARY KEY (user_id, activity_date, log_time)
  );

In this table, ``user_id`` is the partition key, ensuring activities are
grouped by user, and ``activity_date`` is the clustering column, ordering activities
within each user's partition. However, this schema is prone to large partition sizes
over time, given a user with high activity will create an imbalanced cluster.

Clustering columns dictate the order of rows within a partition. They are crucial for
range queries. For example:

.. code::

  CREATE TABLE my_keyspace.user_activities_good (
    user_id uuid,
    activity_date date,
    log_time timestamp,
    log_message text,
    PRIMARY KEY ((user_id, activity_date), log_time)
  );
  
In this table, here the partition is a combination of the ``user_id```
and ``activity_date```, using a technique called "bucketing". This ensures that there
is no unbounded growth within a partition, bucketed to a date. In addition, logs are
ordered by ``log_time``` within each ``(user_id, activity_date)`` partition, making it
efficient to query logs over a time range for a specific user.

Your query design should also be optimized for efficient and effective queries 
to retrieve and manipulate data. Query optimization aims to minimize resource 
usage and latency while achieving maximum throughput.

Indexing is another important aspect of query design. We have already 
introduced the basic concept of primary keys, which can be made up of two 
parts: the partition key and optional clustering columns.

ScyllaDB also supports
`secondary indexes <https://opensource.docs.scylladb.com/stable/using-scylla/secondary-indexes.html>`_
for non-primary key columns. Secondary indexes can improve query flexibility, but it’s
important to consider their impact on performance. For example:

.. code::

  CREATE INDEX ON my_keyspace.user_activities (activity_date);

This index allows querying activities by date regardless of the user. However, secondary
indexes might lead to additional overhead and should be used when necessary.

Secondary indexes are built on top of
`materialized views <https://opensource.docs.scylladb.com/stable/cql/mv.html>`_, which
keep a separate, indexed table based on the base table's data. They can be more performant for reads.

ScyllaDB supports CQL for querying data. Learning and mastering CQL is crucial for designing queries.
For more detailed instructions, please see our `documentation <https://opensource.docs.scylladb.com/stable/cql/>`_.
