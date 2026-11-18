# Driver Support

## Support Policy

We support the **two most recent minor releases** of [ScyllaDB drivers](https://docs.scylladb.com/stable/drivers/cql-drivers.md).

* We test and validate the latest two minor versions.
* We typically patch only the latest minor release.

We recommend staying up to date with the latest supported versions to receive
updates and fixes.

At a minimum, upgrade your driver when upgrading to a new ScyllaDB version
to ensure compatibility between the driver and the database.

## Supported Versions

The following table shows the available ScyllaDB drivers and their latest
versions.

| ScyllaDB Driver                                                  | Supported Versions                                                                                                                                                                                                                                                                                                        |
|------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Python Driver](https://python-driver.docs.scylladb.com/)        | * 3.29<br/>* 3.28                                                                                                                                                                                                                                                                                                         |
| [Java Driver](https://java-driver.docs.scylladb.com/)            | Java Driver 4.x<br/><br/>* 4.19<br/>* 4.18<br/><br/>Java Driver 3.x<br/><br/>**Deprecated** - [Migrate to Java Driver 4.x](https://java-driver.docs.scylladb.com/stable/upgrade_guide/from_3x/)<br/><br/><br/>Critical fixes only from January 1, 2027<br/><br/><br/>End of life: Q2 2027<br/><br/><br/>* 3.13<br/>* 3.12 |
| [Go Driver](https://gocql-driver.docs.scylladb.com/)             | * 1.20<br/>* 1.19                                                                                                                                                                                                                                                                                                         |
| [Rust Driver](https://rust-driver.docs.scylladb.com/)            | * 1.10<br/>* 1.9                                                                                                                                                                                                                                                                                                          |
| [C# Driver](https://csharp-driver.docs.scylladb.com/)            | * 3.22                                                                                                                                                                                                                                                                                                                    |
| [CPP RS Driver](https://cpp-rs-driver.docs.scylladb.com/)        | * 1.0<br/>* 1.1                                                                                                                                                                                                                                                                                                           |
| [C++ Driver](https://github.com/scylladb/cpp-driver/)            | Deprecated. Migrate to [CPP RS Driver](https://cpp-rs-driver.docs.scylladb.com/).                                                                                                                                                                                                                                         |
| [Node.js RS Driver](https://nodejs-rs-driver.docs.scylladb.com/) | * 0.7                                                                                                                                                                                                                                                                                                                     |
