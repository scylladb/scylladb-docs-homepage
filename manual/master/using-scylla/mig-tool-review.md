# ScyllaDB Migration Tools: An Overview

The following migration tools are available for migrating to ScyllaDB from compatible databases,
such as Apache Cassandra, or from other ScyllaDB clusters:

* From SSTable to SSTable
  : - Using nodetool refresh, [Load and Stream](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/refresh.md#nodetool-refresh-load-and-stream) option.
    - On a large scale, it requires tooling to upload / transfer files from location to location.
* From CQL to CQL
  : - [Spark Migrator](https://migrator.docs.scylladb.com/).  The Spark migrator allows you to easily transform the data before pushing it to the destination DB.
* From DynamoDB to ScyllaDB Alternator
  : - [Spark Migrator](https://migrator.docs.scylladb.com/).  The Spark migrator allows you to easily transform the data before pushing it to the destination DB.
