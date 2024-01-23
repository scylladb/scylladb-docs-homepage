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
      user_id uuid,
      message_id uuid,
      message_text text,
      created_at timestamp,
      PRIMARY KEY (user_id, message_id)
    );

In this model, the partition key is chosen as ``user_id``, which is a globally
unique identifier for each user. This choice results in poor partition key
selection because it doesn't distribute data evenly across partitions. As 
a result, messages from popular users with many messages will create hot
partitions, as all their messages will be concentrated in a single partition.

A better solution for partition key selection would look like:

.. code::

    CREATE TABLE my_keyspace.messages_good (
      message_id uuid PRIMARY KEY,
      user_id uuid,
      message_text text,
      created_at timestamp
    );

In this improved model, the partition key is chosen as ``message_id``, which is
the unique identifier for each message. This choice results in even data
distribution across partitions because each user's messages are distributed 
across multiple partitions. Popular users with many posts won't create hot partitions,
as their messages are distributed across the cluster. This approach ensures that all
nodes in the cluster are effectively utilized, preventing performance bottlenecks.
