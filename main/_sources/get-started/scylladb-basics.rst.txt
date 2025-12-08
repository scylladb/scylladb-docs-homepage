============================
ScyllaDB Basics
============================

What is ScyllaDB?
---------------------

ScyllaDB is a high-performance NoSQL database optimized for speed and
scalability. It is designed to efficiently handle large volumes of data with
minimal latency, making it ideal for data-intensive applications. ScyllaDB
uses a shared-nothing architecture, contributing to its excellent performance
and resource utilization.

ScyllaDB comes in two flavors:

* **ScyllaDB Cloud** is a managed NoSQL database-as-a-service (DBaaS) running
  ScyllaDB. It spares you the time and effort of setting up hardware or
  installing software. ScyllaDB Cloud is available on both AWS and Google
  Cloud public clouds, so you can choose your preferred cloud provider
  to run your cluster.
* **ScyllaDB** is a high-performance, distributed NoSQL database designed for
  scalability and low-latency data access, with APIs compatible with Apache
  Cassandra and Amazon DynamoDB API. You can install it on Linux or launch it
  on AWS, GCP, or Azure.

Why ScyllaDB?
--------------

ScyllaDB is favored for its exceptional capability to manage high data volumes
and support rapid read/write operations. It is particularly effective in
environments demanding high throughput, low latency, and the ability to scale.
The database is also known for its robustness and fault tolerance, ensuring
data integrity and availability.

How do I start with ScyllaDB?
-----------------------------------

If you are new to ScyllaDB, start with the :doc:`Develop with ScyllaDB </get-started/develop-with-scylladb/index>`
guide. It will walk you through the basics of running and using ScyllaDB.

How do I interact with a ScyllaDB cluster?
--------------------------------------------

The primary language for communicating with the ScyllaDB database is the `Apache Cassandra Query 
Language (CQL) <https://docs.scylladb.com/manual/stable/cql/>`_.

In addition, ScyllaDB provides drivers in different programming languages, such as Java, Python, Rust,
and more, to help you interact with your clusters more efficiently. The drives ensure that queries are 
distributed evenly and efficiently across the cluster for latencies and the highest overall throughput.

See the `driver documentation <https://docs.scylladb.com/stable/drivers/>`_ and
the `ScyllaDB University course <https://university.scylladb.com/courses/using-scylla-drivers/>`_ 
to learn about the drivers.

How can I monitor my cluster?
------------------------------

On ScyllaDB Cloud, you have access to a set of dashboards that let you monitor your cluster’s state in 
real time. See `Monitoring ScyllaDB Cloud <https://cloud.docs.scylladb.com/stable/monitoring/index.html>`_.

For ScyllaDB, you can use `ScyllaDB Monitoring Stack <https://www.scylladb.com/download/#monitor>`_, 
which allows you to view real-time and historical trend information on ScyllaDB clusters.

How can I learn to use ScyllaDB?
----------------------------------

Join `ScyllaDB University`_, which offers a series of free NoSQL 
database training courses. They were designed as both a ScyllaDB tutorial and a resource for learning 
basic NoSQL concepts. 

Start with the `ScyllaDB Essentials course <https://university.scylladb.com/courses/scylla-essentials-overview/>`_, which 
will help you install and run ScyllaDB and walk you through the key concepts in NoSQL.

Where can I learn more about ScyllaDB?
-----------------------------------------

* Join `ScyllaDB University`_.
* Read the `ScyllaDB documentation <https://docs.scylladb.com/manual/>`_ and
  `ScyllaDB Cloud documentation <https://cloud.docs.scylladb.com/>`_.
* Join the ScyllaDB community:

     * Join the `ScyllaDB Community Forum <https://forum.scylladb.com/>`_.
     * Join our `Slack Channel <https://slack.scylladb.com/>`_.
     * Read our `blog <https://www.scylladb.com/users-blog/>`_.
     * Attend ScyllaDB `workshops, webinars, and conferences <https://www.scylladb.com/events/>`_.








.. _ScyllaDB University: https://university.scylladb.com/