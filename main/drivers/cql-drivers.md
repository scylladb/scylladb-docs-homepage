# ScyllaDB CQL Drivers

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
  [Install a Driver](https://docs.scylladb.com/stable/get-started/develop-with-scylladb/install-drivers.md)
  section in the Get Started guide.
* We support the **two most recent minor releases** of each driver. Stay up to
  date with driver releases to maintain compatibility with your ScyllaDB version.
  See [Driver Support](https://docs.scylladb.com/stable/versioning/driver-support.md) for the support policy
  and the list of currently supported versions.

## Available ScyllaDB Drivers

The following table shows the available ScyllaDB drivers.
Click the documentation link to view the documentation for each driver.

| ScyllaDB Driver   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Python Driver     | A native Python client for interacting with ScyllaDB and Cassandra<br/>clusters, implementing the CQL binary protocol. It supports<br/>asynchronous query execution, automatic connection pooling, and<br/>adaptive load balancing to optimize throughput and latency in<br/>Python applications.<br/><br/><br/><br/>[Python Driver documentation](https://python-driver.docs.scylladb.com/)                                                                                                                                                                                                             |
| Java Driver       | A native Java client for interacting with ScyllaDB and Cassandra<br/>clusters, implementing the CQL binary protocol. It provides full<br/>asynchronous support, automatic query paging, and advanced load<br/>balancing policies.<br/><br/><br/>There are two driver families, 4.x and 3.x, and the support policy<br/>applies separately to each family, covering the two latest minor<br/>versions within 4.x and the two latest minor versions within 3.x.<br/><br/><br/><br/>[Java Driver documentation](https://java-driver.docs.scylladb.com/)                                                     |
| Go Driver         | A native Go client for interacting with ScyllaDB and Cassandra<br/>clusters, implementing the CQL binary protocol. It features a fully<br/>asynchronous, non-blocking API with shard‑aware host selection and<br/>optimized connection management for high-performance Go applications.<br/><br/><br/>An extension, **gocqlx**, adds higher‑level abstractions, such as<br/>query builders and struct binding, to improve developer productivity.<br/><br/><br/>* [Go Driver documentation](https://github.com/scylladb/gocql)<br/>* [Gocql extension documentation](https://github.com/scylladb/gocqlx) |
| Rust Driver       | A native Rust client for interacting with ScyllaDB and Cassandra<br/>clusters, implementing the CQL binary protocol. Delivers memory-safe,<br/>fully asynchronous operations with zero-cost abstractions for<br/>low-latency, high-throughput Rust applications.<br/><br/><br/><br/>[Rust Driver documentation](https://rust-driver.docs.scylladb.com/)                                                                                                                                                                                                                                                  |
| C# Driver         | A native C# client for interacting with ScyllaDB and Cassandra<br/>clusters, implementing the CQL binary protocol. It integrates with<br/>.NET asynchronous programming patterns, supports connection pooling<br/>and retry policies, and is optimized for enterprise-grade .NET<br/>applications.<br/><br/><br/><br/>[C# Driver documentation](https://csharp-driver.docs.scylladb.com/)                                                                                                                                                                                                                |
| CPP RS Driver     | A native C++ client built on a Rust core for interacting with<br/>ScyllaDB and Cassandra clusters, implementing the CQL binary<br/>protocol. It combines Rust’s memory safety and concurrency features<br/>with C++ usability, providing safer and more reliable<br/>high-performance database access.<br/><br/><br/><br/>[CPP RS Driver documentation](https://cpp-rs-driver.docs.scylladb.com/)                                                                                                                                                                                                        |
| Node.js RS Driver | A native Node.js client for interacting with ScyllaDB and Cassandra<br/>clusters, implementing the CQL binary protocol. Built on a Rust core,<br/>it provides fully asynchronous operations, efficient resource usage,<br/>and high-throughput, low-latency database access for Node.js applications.<br/><br/><br/><br/>[Node.js RS Driver documentation](https://nodejs-rs-driver.docs.scylladb.com/)                                                                                                                                                                                                  |
| C++ Driver        | This driver is no longer actively maintained. We recommend using<br/>the CPP RS Driver for improved performance and full support<br/>for the latest ScyllaDB features.<br/><br/><br/><br/>[C++ Driver documentation](https://cpp-driver.docs.scylladb.com/)                                                                                                                                                                                                                                                                                                                                              |

## Support for Tablets

The following table specifies which ScyllaDB drivers support
[tablets](https://docs.scylladb.com/manual/stable/architecture/tablets.html)
and since which version.

| ScyllaDB Driver                                             | Support for Tablets                                        | Since Version                                                |
|-------------------------------------------------------------|------------------------------------------------------------|--------------------------------------------------------------|
| [Python](https://python-driver.docs.scylladb.com/)          | <i class="inline-icon icon-check" aria-hidden="true"></i>  | 3.26.5                                                       |
| [Java](https://java-driver.docs.scylladb.com/)              | <i class="inline-icon icon-check" aria-hidden="true"></i>  | 4.18.0 (Java Driver 4.x)<br/><br/>3.11.5.2 (Java Driver 3.x) |
| [Go](https://github.com/scylladb/gocql)                     | <i class="inline-icon icon-check" aria-hidden="true"></i>  | 1.13.0                                                       |
| [Gocql extension](https://github.com/scylladb/gocqlx)       | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | N/A                                                          |
| [Rust](https://rust-driver.docs.scylladb.com/)              | <i class="inline-icon icon-check" aria-hidden="true"></i>  | 0.13.0                                                       |
| [C#](https://csharp-driver.docs.scylladb.com/)              | <i class="inline-icon icon-check" aria-hidden="true"></i>  | All versions                                                 |
| [CPP RS](https://cpp-rs-driver.docs.scylladb.com/)          | <i class="inline-icon icon-check" aria-hidden="true"></i>  | All versions                                                 |
| [Node.js RS](https://github.com/scylladb/nodejs-rs-driver/) | <i class="inline-icon icon-check" aria-hidden="true"></i>  | All versions                                                 |
| [C++](https://cpp-driver.docs.scylladb.com/)                | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | N/A. This driver is no longer actively maintained.           |

<a id="cql-drivers-vector-support"></a>

## Support for Vector Search

The [Vector Search](https://cloud.docs.scylladb.com/stable/vector-search/index.html)
feature requires drivers to support the `vector` CQL type.
The following table specifies which ScyllaDB drivers support the `vector` type
and since which version.

| ScyllaDB Driver                                             | Support for the `vector` type                              | Since Version                                                                                 |
|-------------------------------------------------------------|------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| [Python](https://python-driver.docs.scylladb.com/)          | <i class="inline-icon icon-check" aria-hidden="true"></i>  | 3.28.0                                                                                        |
| [Java](https://java-driver.docs.scylladb.com/)              | <i class="inline-icon icon-check" aria-hidden="true"></i>  | Java Driver 4.x: 4.16.0 (recommended 4.19.0 or later)<br/><br/>Java Driver 3.x: not supported |
| [Go](https://github.com/scylladb/gocql)                     | <i class="inline-icon icon-check" aria-hidden="true"></i>  | 1.17.0                                                                                        |
| [Gocql extension](https://github.com/scylladb/gocqlx)       | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | To be supported in a future release                                                           |
| [Rust](https://rust-driver.docs.scylladb.com/)              | <i class="inline-icon icon-check" aria-hidden="true"></i>  | 1.2.0                                                                                         |
| [C#](https://csharp-driver.docs.scylladb.com/)              | <i class="inline-icon icon-check" aria-hidden="true"></i>  | All versions                                                                                  |
| [CPP RS](https://cpp-rs-driver.docs.scylladb.com/)          | <i class="inline-icon icon-check" aria-hidden="true"></i>  | 0.5.1                                                                                         |
| [Node.js RS](https://github.com/scylladb/nodejs-rs-driver/) | <i class="inline-icon icon-check" aria-hidden="true"></i>  | All versions                                                                                  |
| [C++](https://cpp-driver.docs.scylladb.com/)                | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | N/A. This driver is no longer actively maintained.                                            |

## CDC Integration with ScyllaDB Drivers

The following table specifies which ScyllaDB drivers include a library for
[CDC](https://docs.scylladb.com/manual/stable/features/cdc/index.html).

| ScyllaDB Driver                                             | CDC Connector                                              |
|-------------------------------------------------------------|------------------------------------------------------------|
| [Python](https://python-driver.docs.scylladb.com/)          | <i class="inline-icon icon-cancel" aria-hidden="true"></i> |
| [Java](https://java-driver.docs.scylladb.com/)              | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| [Go](https://github.com/scylladb/gocql)                     | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| [Gocql extension](https://github.com/scylladb/gocqlx)       | <i class="inline-icon icon-cancel" aria-hidden="true"></i> |
| [Rust](https://rust-driver.docs.scylladb.com/)              | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| [C#](https://csharp-driver.docs.scylladb.com/)              | <i class="inline-icon icon-cancel" aria-hidden="true"></i> |
| [CPP RS Driver](https://cpp-rust-driver.docs.scylladb.com/) | <i class="inline-icon icon-cancel" aria-hidden="true"></i> |
| [Node.js RS](https://github.com/scylladb/nodejs-rs-driver/) | <i class="inline-icon icon-cancel" aria-hidden="true"></i> |
| [C++](https://cpp-driver.docs.scylladb.com/)                | <i class="inline-icon icon-cancel" aria-hidden="true"></i> |
