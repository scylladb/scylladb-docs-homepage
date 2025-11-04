========================
Driver Support Policy
========================

Driver Support Policy
-------------------------------

We support the **two most recent minor releases** of our drivers.

* We test and validate the latest two minor versions.
* We typically patch only the latest minor release.

We recommend staying up to date with the latest supported versions to receive
updates and fixes.

At a minimum, upgrade your driver when upgrading to a new ScyllaDB version
to ensure compatibility between the driver and the database.

ScyllaDB Drivers
-----------------

The following table shows the available ScyllaDB drivers and their latest
versions. Click the documentation link to view the documentation for each
driver.

.. list-table::
    :widths: 20 20 60
    :header-rows: 1

    * - ScyllaDB Driver
      - Latest version
      - Description
    * - Python Driver
      - 3.28.2
      - | A native Python client for interacting with ScyllaDB and Cassandra
          clusters, implementing the CQL binary protocol. It supports
          asynchronous query execution, automatic connection pooling, and
          adaptive load balancing to optimize throughput and latency in
          Python applications.

        `Python Driver documentation <https://python-driver.docs.scylladb.com/>`_
    * - Java Driver
      - * 4.19.0 (Java Driver 4.x)
        * 3.11.5 (Java Driver 3.x)
      - | A native Java client for interacting with ScyllaDB and Cassandra
          clusters, implementing the CQL binary protocol. It provides full
          asynchronous support, automatic query paging, and advanced load
          balancing policies.
        | There are two driver families, 4.x and 3.x, and the support policy
          applies separately to each family, covering the two latest minor
          versions within 4.x and the two latest minor versions within 3.x.

        `Java Driver documentation <https://java-driver.docs.scylladb.com/>`_
    * - Go Driver
      - 1.16.1
      - | A native Go client for interacting with ScyllaDB and Cassandra
          clusters, implementing the CQL binary protocol. It features a fully
          asynchronous, non-blocking API with shard‑aware host selection and
          optimized connection management for high-performance Go applications.
        | An extension, **gocqlx**, adds higher‑level abstractions, such as
          query builders and struct binding, to improve developer productivity.

        * `Go Driver documentation <https://github.com/scylladb/gocql>`_
        * `Gocql extension documentation <https://github.com/scylladb/gocqlx>`_
    * - Rust Driver
      - 1.3.1
      - | A native Rust client for interacting with ScyllaDB and Cassandra
          clusters, implementing the CQL binary protocol. Delivers memory-safe,
          fully asynchronous operations with zero-cost abstractions for
          low-latency, high-throughput Rust applications.

        `Rust Driver documentation <https://rust-driver.docs.scylladb.com/>`_
    
    * - C# Driver
      - 3.22.0
      - | A native C# client for interacting with ScyllaDB and Cassandra
          clusters, implementing the CQL binary protocol. It integrates with
          .NET asynchronous programming patterns, supports connection pooling
          and retry policies, and is optimized for enterprise-grade .NET
          applications.
        
        `C# Driver documentation <https://csharp-driver.docs.scylladb.com/>`_

    * - CPP RS Driver
      - 0.5.1
      - | A native C++ client built on a Rust core for interacting with
          ScyllaDB and Cassandra clusters, implementing the CQL binary
          protocol. It combines Rust’s memory safety and concurrency features
          with C++ usability, providing safer and more reliable
          high-performance database access.

        `CPP RS Driver <https://cpp-rs-driver.docs.scylladb.com/>`_

    * - C++ Driver
      - 2.16.2
      - | **This driver is no longer actively maintained. We recommend using
          the ScyllaDB CPP RS Driver for improved performance and full support
          for the latest ScyllaDB features.**

        `C++ Driver documentation <https://cpp-driver.docs.scylladb.com/>`_
