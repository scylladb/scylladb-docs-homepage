====================================
Data Modeling Best Practices
====================================

These additional topics provide a broader perspective on data modeling, query 
design, schema design, and best practices when working with ScyllaDB or similar 
distributed NoSQL databases.

**Partition Key Selection**

Choose your partition keys to avoid imbalances in your clusters. Imbalanced 
partitions can lead to performance bottlenecks, which impact overall cluster 
performance. Balancing the distribution of data across partitions is crucial 
to ensure all nodes are effectively utilized in your cluster.

Let's consider a scenario with poor partition key selection:

.. code::

    CREATE TABLE my_keyspace.messages_bad (
        message_id uuid PRIMARY KEY,
        user_id uuid,
        message_text text,
        created_at timestamp
    );

In this model, the partition key is chosen as ``message_id``, which is a globally 
unique identifier for each message. This choice results in poor partition key 
selection because it doesn't distribute data evenly across partitions. As 
a result, messages from popular users with many posts will create hot 
partitions, as all their messages will be concentrated in a single partition.

A better solution for partition key selection would look like:

.. code::

    CREATE TABLE my_keyspace.messages_good (
      user_id uuid,
      message_id uuid,
      message_text text,
      created_at timestamp,
      PRIMARY KEY (user_id, message_id)
    );

In this improved model, the partition key is chosen as ``user_id``, which is 
the unique identifier for each user. This choice results in even data 
distribution across partitions because each user's messages are distributed 
across multiple partitions based on their ``user_id``. Popular users with many 
posts won't create hot partitions, as their messages are distributed across 
the cluster. This approach ensures that all nodes in the cluster are 
effectively utilized, preventing performance bottlenecks.

**Tombstones and Delete Workloads**

If your workload involves frequent deletes, it’s crucial that you understand 
the implications of tombstones on your read path. Tombstones are markers for 
deleted data and can negatively affect query performance if not managed 
effectively.

Let's consider a data model for storing user messages:

.. code::

    CREATE TABLE my_keyspace.user_messages (
        user_id uuid,
        message_id uuid,
        message_text text,
        is_deleted boolean,
        PRIMARY KEY (user_id, message_id)
    );

In this table, each user can have multiple messages, identified by 
``user_id`` and ``message_id``.
The ``is_deleted`` column is used to mark messages as deleted (true) or not 
deleted (false). When a user deletes a message, a tombstone is created to mark 
the message as deleted. Tombstones are necessary for data consistency, but can 
negatively affect query performance, especially when there are frequent delete 
operations.

Adjust your compaction strategy to account for tombstones and optimize query 
performance in scenarios with heavy delete operations.

To optimize query performance in scenarios with heavy delete operations, you 
can `adjust the compaction strategy and use TTL <https://opensource.docs.scylladb.com/stable/kb/ttl-facts.html>`_ 
(Time-to-Live) to handle tombstones more efficiently. ScyllaDB allows you to 
choose different compaction strategies. In scenarios with heavy delete 
workloads, consider using a compaction strategy that efficiently handles 
tombstones, such as the ``TimeWindowCompactionStrategy``.

.. code::

    ALTER TABLE my_keyspace.user_messages 
     WITH default_time_to_live = 2592000 
     AND compaction = {'class': 'TimeWindowCompactionStrategy', 'base_time_seconds': 86400, 'max_sstable_age_days': 14};


This setup, with a 30-day TTL (``default_time_to_live = 2592000``) and 
a 14-day maximum SSTable age ``('max_sstable_age_days': 14)``, is suited for 
time-sensitive data scenarios where keeping data beyond a month is 
unnecessary, and the most relevant data is always from the last two weeks.