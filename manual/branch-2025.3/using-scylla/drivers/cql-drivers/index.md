# ScyllaDB CQL Drivers

## ScyllaDB Drivers

The following ScyllaDB drivers are available:

* Python Driver
* Java Driver
* Go Driver
* Go Extension
* C++ Driver
* [CPP-over-Rust Driver](https://github.com/scylladb/cpp-rust-driver)
* Rust Driver

We recommend using ScyllaDB drivers. All ScyllaDB drivers are shard-aware and provide additional
benefits over third-party drivers.

ScyllaDB supports the CQL binary protocol version 3, so any Apache Cassandra/CQL driver that implements
the same version works with ScyllaDB.

## CDC Integration with ScyllaDB Drivers

The following table specifies which ScyllaDB drivers include a library for
[CDC](https://docs.scylladb.com/manual/branch-2025.3/features/cdc/cdc-intro.md).

| ScyllaDB Driver                                                     | CDC Connector                                              |
|---------------------------------------------------------------------|------------------------------------------------------------|
| Python                                                              | <i class="inline-icon icon-cancel" aria-hidden="true"></i> |
| Java                                                                | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| Go                                                                  | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| Go Extension                                                        | <i class="inline-icon icon-cancel" aria-hidden="true"></i> |
| C++                                                                 | <i class="inline-icon icon-cancel" aria-hidden="true"></i> |
| [CPP-over-Rust Driver](https://github.com/scylladb/cpp-rust-driver) | <i class="inline-icon icon-cancel" aria-hidden="true"></i> |
| Rust                                                                | <i class="inline-icon icon-check" aria-hidden="true"></i>  |

## Support for Tablets

The following table specifies which ScyllaDB drivers support
[tablets](https://docs.scylladb.com/manual/branch-2025.3/architecture/tablets.md) and since which version.

| ScyllaDB Driver                                                     | Support for Tablets                                        | Since Version                                                |
|---------------------------------------------------------------------|------------------------------------------------------------|--------------------------------------------------------------|
| Python                                                              | <i class="inline-icon icon-check" aria-hidden="true"></i>  | 3.26.5                                                       |
| Java                                                                | <i class="inline-icon icon-check" aria-hidden="true"></i>  | 4.18.0 (Java Driver 4.x)<br/><br/>3.11.5.2 (Java Driver 3.x) |
| Go                                                                  | <i class="inline-icon icon-check" aria-hidden="true"></i>  | 1.13.0                                                       |
| Go Extension                                                        | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | N/A                                                          |
| C++                                                                 | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | N/A                                                          |
| [CPP-over-Rust Driver](https://github.com/scylladb/cpp-rust-driver) | <i class="inline-icon icon-check" aria-hidden="true"></i>  | All versions                                                 |
| Rust                                                                | <i class="inline-icon icon-check" aria-hidden="true"></i>  | 0.13.0                                                       |

## Driver Support Policy

We support the **two most recent minor releases** of our drivers.

* We test and validate the latest two minor versions.
* We typically patch only the latest minor release.

We recommend staying up to date with the latest supported versions to receive
updates and fixes.

At a minimum, upgrade your driver when upgrading to a new ScyllaDB version
to ensure compatibility between the driver and the database.

## Third-party Drivers

You can find the third-party driver documentation on the GitHub pages for each driver:

* [DataStax Java Driver](https://github.com/datastax/java-driver/)
* [DataStax Python Driver](https://github.com/datastax/python-driver/)
* [DataStax C# Driver](https://github.com/datastax/csharp-driver/)
* [DataStax Ruby Driver](https://github.com/datastax/ruby-driver/)
* [DataStax Node.js Driver](https://github.com/datastax/nodejs-driver/)
* [DataStax C++ Driver](https://github.com/datastax/cpp-driver/)
* [DataStax PHP Driver (Supported versions: 7.1)](https://github.com/datastax/php-driver)
* [He4rt PHP Driver (Supported versions: 8.1 and 8.2)](https://github.com/he4rt/scylladb-php-driver/)
* [Scala Phantom Project](https://github.com/outworkers/phantom)
* [Xandra Elixir Driver](https://github.com/lexhide/xandra)
* [Exandra Elixir Driver](https://github.com/vinniefranco/exandra)

## Learn about ScyllaDB Drivers on ScyllaDB University

> The free [Using ScyllaDB Drivers course](https://university.scylladb.com/courses/using-scylla-drivers/)
> on ScyllaDB University covers the use of drivers in multiple languages to interact with a ScyllaDB
> cluster. The languages covered include Java, CPP, Rust, Golang, Python, Node.JS, Scala, and others.
