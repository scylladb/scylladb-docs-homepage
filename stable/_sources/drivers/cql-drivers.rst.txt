======================
ScyllaDB CQL Drivers
======================

ScyllaDB drivers are specialized client libraries that
enable efficient communication between your application and a ScyllaDB cluster.
They handle core operations such as inserts, queries, and schema modifications
while optimizing performance through shard awareness. Each driver is designed
to recognize ScyllaDB’s shard-per-core architecture, routing requests directly
to the appropriate CPU core and node to minimize latency and maximize throughput.

* To interact with ScyllaDB, you need to install the appropriate driver for
  your programming language. You will find full installation instructions in
  the documentation for each driver (see the table below).
  To perform a basic installation, you can refer to the
  :doc:`Install a Driver </get-started/develop-with-scylladb/install-drivers>`
  section in the Get Started guide.
* We support the **two most recent minor releases** of each driver. Stay up to
  date with driver releases to maintain compatibility with your ScyllaDB version.
  See :doc:`Driver Support </versioning/driver-support>` for the support policy
  and the list of currently supported versions.

Available ScyllaDB Drivers
----------------------------

The following table shows the available ScyllaDB drivers.
Click the documentation link to view the documentation for each driver.

.. list-table::
    :widths: 25 75
    :header-rows: 1

    * - ScyllaDB Driver
      - Description
    * - Python Driver
      - | A native Python client for interacting with ScyllaDB and Cassandra
          clusters, implementing the CQL binary protocol. It supports
          asynchronous query execution, automatic connection pooling, and
          adaptive load balancing to optimize throughput and latency in
          Python applications.

        `Python Driver documentation <https://python-driver.docs.scylladb.com/>`_
    * - Java Driver
      - | A native Java client for interacting with ScyllaDB and Cassandra
          clusters, implementing the CQL binary protocol. It provides full
          asynchronous support, automatic query paging, and advanced load
          balancing policies.
        | There are two driver families, 4.x and 3.x, and the support policy
          applies separately to each family, covering the two latest minor
          versions within 4.x and the two latest minor versions within 3.x.

        `Java Driver documentation <https://java-driver.docs.scylladb.com/>`_
    * - Go Driver
      - | A native Go client for interacting with ScyllaDB and Cassandra
          clusters, implementing the CQL binary protocol. It features a fully
          asynchronous, non-blocking API with shard‑aware host selection and
          optimized connection management for high-performance Go applications.
        | An extension, **gocqlx**, adds higher‑level abstractions, such as
          query builders and struct binding, to improve developer productivity.

        * `Go Driver documentation <https://github.com/scylladb/gocql>`_
        * `Gocql extension documentation <https://github.com/scylladb/gocqlx>`_
    * - Rust Driver
      - | A native Rust client for interacting with ScyllaDB and Cassandra
          clusters, implementing the CQL binary protocol. Delivers memory-safe,
          fully asynchronous operations with zero-cost abstractions for
          low-latency, high-throughput Rust applications.

        `Rust Driver documentation <https://rust-driver.docs.scylladb.com/>`_
    
    * - C# Driver
      - | A native C# client for interacting with ScyllaDB and Cassandra
          clusters, implementing the CQL binary protocol. It integrates with
          .NET asynchronous programming patterns, supports connection pooling
          and retry policies, and is optimized for enterprise-grade .NET
          applications.
        
        `C# Driver documentation <https://csharp-driver.docs.scylladb.com/>`_

    * - CPP RS Driver
      - | A native C++ client built on a Rust core for interacting with
          ScyllaDB and Cassandra clusters, implementing the CQL binary
          protocol. It combines Rust’s memory safety and concurrency features
          with C++ usability, providing safer and more reliable
          high-performance database access.

        `CPP RS Driver documentation <https://cpp-rs-driver.docs.scylladb.com/>`_

    * - C++ Driver
      - | This driver is no longer actively maintained. We recommend using
          the CPP RS Driver for improved performance and full support
          for the latest ScyllaDB features.

        `C++ Driver documentation <https://cpp-driver.docs.scylladb.com/>`_

Support for Tablets
-------------------------

The following table specifies which ScyllaDB drivers support
`tablets <https://docs.scylladb.com/manual/stable/architecture/tablets.html>`_
and since which version.

.. list-table:: 
   :widths: 30 35 35
   :header-rows: 1

   * - ScyllaDB Driver
     - Support for Tablets
     - Since Version
   * - `Python <https://python-driver.docs.scylladb.com/>`_
     - |v| 
     - 3.26.5
   * - `Java <https://java-driver.docs.scylladb.com/>`_
     - |v| 
     - 4.18.0 (Java Driver 4.x)

       3.11.5.2 (Java Driver 3.x)
   * - `Go <https://github.com/scylladb/gocql>`_
     - |v|
     - 1.13.0
   * - `Gocql extension <https://github.com/scylladb/gocqlx>`_
     - |x| 
     - N/A
   * - `Rust <https://rust-driver.docs.scylladb.com/>`_
     - |v| 
     - 0.13.0
   * - `C# <https://csharp-driver.docs.scylladb.com/>`_
     - |v|
     - All versions
   * - `CPP RS <https://cpp-rs-driver.docs.scylladb.com/>`_
     - |v|
     - All versions
   * - `C++ <https://cpp-driver.docs.scylladb.com/>`_
     - |x| 
     - N/A. This driver is no longer actively maintained.

CDC Integration with ScyllaDB Drivers
-------------------------------------------

The following table specifies which ScyllaDB drivers include a library for
`CDC <https://docs.scylladb.com/manual/stable/features/cdc/index.html>`_.

.. list-table:: 
   :widths: 40 60
   :header-rows: 1

   * - ScyllaDB Driver
     - CDC Connector
   * - `Python <https://python-driver.docs.scylladb.com/>`_
     - |x| 
   * - `Java <https://java-driver.docs.scylladb.com/>`_
     - |v|
   * - `Go <https://github.com/scylladb/gocql>`_
     - |v|
   * - `Gocql extension <https://github.com/scylladb/gocqlx>`_
     - |x| 
   * - `Rust <https://rust-driver.docs.scylladb.com/>`_
     - |v|
   * - `C# <https://csharp-driver.docs.scylladb.com/>`_
     - |x|
   * - `CPP RS Driver <https://cpp-rust-driver.docs.scylladb.com/>`_
     - |x|
   * - `C++ <https://cpp-driver.docs.scylladb.com/>`_
     - |x| 