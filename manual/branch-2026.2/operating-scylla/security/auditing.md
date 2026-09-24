# ScyllaDB Auditing Guide

Auditing allows the administrator to monitor activities on a ScyllaDB cluster, including CQL queries and data changes, as well as Alternator (DynamoDB-compatible API) requests.
The information is stored in a Syslog or a ScyllaDB table.

## Prerequisite

Enable ScyllaDB [Authentication](https://docs.scylladb.com/manual/branch-2026.2/operating-scylla/security/authentication.md) and [Authorization](https://docs.scylladb.com/manual/branch-2026.2/operating-scylla/security/enable-authorization.md).

## Enabling Audit

By default, auditing is **enabled** with the `table` backend. Enabling auditing is controlled by the `audit:` parameter in the `scylla.yaml` file.
You can set the following options:

* `none` - Audit is disabled.
* `table` - Audit is enabled, and messages are stored in a ScyllaDB table (default).
* `syslog` - Audit is enabled, and messages are sent to Syslog.
* `syslog,table` - Audit is enabled, and messages are stored in a ScyllaDB table and sent to Syslog.

Configuring any other value results in an error at ScyllaDB startup.

## Configuring Audit

The audit can be tuned using the following flags or `scylla.yaml` entries:

| Flag             | Description                                                                                                                                                                                                                                   |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| audit_categories | Comma-separated list of statement categories that should be audited                                                                                                                                                                           |
| audit_tables     | Comma-separated list of table names that should be audited, in the format `<keyspace_name>.<table_name>`.<br/><br/>For Alternator tables use the `alternator.<table_name>` format (see [Auditing Alternator Requests](#alternator-auditing)). |
| audit_keyspaces  | Comma-separated list of keyspaces that should be audited. You must specify at least one keyspace.<br/>If you leave this option empty, no keyspace will be audited.                                                                            |

The default value and liveness of each option are listed in
[Configuration Parameters](https://docs.scylladb.com/manual/branch-2026.2/reference/configuration-parameters.md): see
[audit_categories](https://docs.scylladb.com/manual/branch-2026.2/reference/configuration-parameters.md#confprop-audit-categories),
[audit_tables](https://docs.scylladb.com/manual/branch-2026.2/reference/configuration-parameters.md#confprop-audit-tables) and
[audit_keyspaces](https://docs.scylladb.com/manual/branch-2026.2/reference/configuration-parameters.md#confprop-audit-keyspaces).

To audit all the tables in a keyspace, set the `audit_keyspaces` with the keyspace you want to audit and leave `audit_tables` empty.

You can use DCL, AUTH, and ADMIN audit categories without including any keyspace or table.

### audit_categories parameter description

| Parameter   | Logs Description                                                                                                                                                                                                                                   | Applies To      |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| AUTH        | Logs login events                                                                                                                                                                                                                                  | CQL             |
| DML         | Logs insert, update, delete, and other data manipulation language (DML) events                                                                                                                                                                     | CQL, Alternator |
| DDL         | Logs object and role create, alter, drop, and other data definition language (DDL) events                                                                                                                                                          | CQL, Alternator |
| DCL         | Logs grant, revoke, create role, drop role, and list roles events                                                                                                                                                                                  | CQL             |
| QUERY       | Logs all queries                                                                                                                                                                                                                                   | CQL, Alternator |
| ADMIN       | Logs service level operations: create, alter, drop, attach, detach, list.<br/>For [service level](https://docs.scylladb.com/manual/branch-2026.2/features/workload-prioritization.md#workload-priorization-service-level-management)<br/>auditing. | CQL             |

For details on auditing Alternator operations, see [Auditing Alternator Requests](#alternator-auditing).

Note that enabling audit may negatively impact performance and audit-to-table may consume extra storage. That’s especially true when auditing DML and QUERY categories, which generate a high volume of audit messages.

<a id="alternator-auditing"></a>

### Auditing Alternator Requests

When auditing is enabled, Alternator (DynamoDB-compatible API) requests are audited using the same
backends and the same filtering configuration (`audit_categories`, `audit_keyspaces`,
`audit_tables`) as CQL operations. No additional configuration is needed.

Both successful and failed Alternator requests are audited.

#### Alternator Operation Categories

Each Alternator API operation is assigned to one of the standard audit categories:

| Category   | Alternator Operations                                                                                                                                                                                                  |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DDL        | CreateTable, DeleteTable, UpdateTable, TagResource, UntagResource, UpdateTimeToLive                                                                                                                                    |
| DML        | PutItem, UpdateItem, DeleteItem, BatchWriteItem                                                                                                                                                                        |
| QUERY      | GetItem, BatchGetItem, Query, Scan, DescribeTable, ListTables, DescribeEndpoints,<br/>ListTagsOfResource, DescribeTimeToLive, DescribeContinuousBackups,<br/>ListStreams, DescribeStream, GetShardIterator, GetRecords |

#### NOTE
AUTH, DCL, and ADMIN categories do not apply to Alternator operations. These categories
are specific to CQL authentication, authorization, and service-level management.

#### Operation Field Format

For CQL operations, the `operation` field in the audit log contains the raw CQL query string.
For Alternator operations, the format is:

```none
<OperationName>|<JSON request body>
```

For example:

```none
PutItem|{"TableName":"my_table","Item":{"p":{"S":"pk_val"},"c":{"S":"ck_val"},"v":{"S":"data"}}}
```

#### NOTE
The full JSON request body is included in the `operation` field. For batch operations
(such as BatchWriteItem), this can be very large (up to 16 MB).

#### Keyspace and Table Filtering for Alternator

The real keyspace name of an Alternator table `T` is `alternator_T`.
The `audit_tables` config flag uses the shorthand format `alternator.T` to refer to such
tables – the parser expands it to the real keyspace name automatically.
For `audit_keyspaces`, use the real keyspace name directly.

For example, to audit an Alternator table called `my_table_name` use either of the below:

```yaml
# Using audit_tables - use 'alternator' as the keyspace name:
audit_tables: "alternator.my_table_name"

# Using audit_keyspaces - use the real keyspace name:
audit_keyspaces: "alternator_my_table_name"
```

**Global and batch operations**: Some Alternator operations are not scoped to a single table:

* `ListTables` and `DescribeEndpoints` have no associated keyspace or table.
* `BatchWriteItem` and `BatchGetItem` may span multiple tables.

These operations are logged whenever their category matches `audit_categories`, regardless of
`audit_keyspaces` or `audit_tables` filters. Their `keyspace_name` field is empty, and for
batch operations the `table_name` field contains a pipe-separated (`|`) list of all involved table names.

**DynamoDB Streams operations**: For streams-related operations (`DescribeStream`, `GetShardIterator`,
`GetRecords`), the `table_name` field contains the base table name and the CDC log table name
separated by a pipe (e.g., `my_table|my_table_scylla_cdc_log`).

#### Alternator Audit Log Examples

Syslog output example (PutItem):

```shell
Mar 18 10:15:03 ip-10-143-2-108 scylla-audit[28387]: node="10.143.2.108", category="DML", cl="LOCAL_QUORUM", error="false", keyspace="alternator_my_table", query="PutItem|{\"TableName\":\"my_table\",\"Item\":{\"p\":{\"S\":\"pk_val\"}}}", client_ip="127.0.0.1", table="my_table", username="anonymous"
```

Table output example (PutItem):

```shell
SELECT * FROM audit.audit_log ;
```

returns:

```none
 date                    | node         | event_time                           | category | consistency  | error | keyspace_name         | operation                                                                        | source    | table_name | username  |
-------------------------+--------------+--------------------------------------+----------+--------------+-------+-----------------------+----------------------------------------------------------------------------------+-----------+------------+-----------+
2026-03-18 00:00:00+0000 | 10.143.2.108 | 3429b1a5-2a94-11e8-8f4e-000000000001 |      DML | LOCAL_QUORUM | False | alternator_my_table   | PutItem|{"TableName":"my_table","Item":{"p":{"S":"pk_val"}}}                     | 127.0.0.1 |   my_table | anonymous |
(1 row)
```

## Configuring Audit Storage

Auditing messages can be sent to [Syslog](#auditing-syslog-storage) or stored in a ScyllaDB [table](#auditing-table-storage) or both.

<a id="auditing-syslog-storage"></a>

### Storing Audit Messages in Syslog

**Procedure**

1. Set the `audit` parameter in the `scylla.yaml` file to `syslog`.

   For example:
   ```shell
   # audit setting
   # 'audit' config option controls if and where to output audited events:
   audit: "syslog"
   #
   # List of statement categories that should be audited.
   audit_categories: "DCL,DDL,AUTH"
   #
   # List of tables that should be audited.
   audit_tables: "mykespace.mytable"
   #
   # List of keyspaces that should be fully audited.
   # All tables in those keyspaces will be audited
   audit_keyspaces: "mykespace"
   ```
2. Restart the ScyllaDB node.

Supported OS

```shell
sudo systemctl restart scylla-server
```

Docker

```shell
docker exec -it some-scylla supervisorctl restart scylla
```

(without restarting *some-scylla* container)

By default, audit messages are written to the same destination as ScyllaDB [logging](https://docs.scylladb.com/manual/branch-2026.2/getting-started/logging.md), with `scylla-audit` as the process name.

Logging output example (CQL drop table):

```shell
Mar 18 09:53:52 ip-10-143-2-108 scylla-audit[28387]: node="10.143.2.108", category="DDL", cl="ONE", error="false", keyspace="nba", query="DROP TABLE nba.team_roster ;", client_ip="127.0.0.1", table="team_roster", username="anonymous"
```

To redirect the Syslog output to a file, follow the steps below (available only for CentOS) :

1. Install rsyslog sudo `dnf install rsyslog`.
2. Edit `/etc/rsyslog.conf` and append the following to the file: `if $programname contains 'scylla-audit' then /var/log/scylla-audit.log`.
3. Start rsyslog `systemctl start rsyslog`.
4. Enable rsyslog `systemctl enable rsyslog`.

<a id="auditing-table-storage"></a>

### Storing Audit Messages in a Table

Messages are stored in a ScyllaDB table named `audit.audit_log`.

For example:

```shell
CREATE TABLE IF NOT EXISTS audit.audit_log (
      date timestamp,
      node inet,
      event_time timeuuid,
      category text,
      consistency text,
      table_name text,
      keyspace_name text,
      operation text,
      source inet,
      username text,
      error boolean,
      PRIMARY KEY ((date, node), event_time));
```

#### NOTE
The schema of `audit.audit_log` has been migrated in the 2024.2 version from `SimpleStrategy RF=1` to `NetworkTopologyStrategy RF=3`:

* By default every DC will contain 3 audit replicas. If a new DC is added, in order for it to also contain audit replicas, audit’s schema has to be manually altered.
* CL for writes is still equal to `1`, which implies that reading audit rows with CL=Quorum may fail, which is especially true for clusters with less than 3 nodes.

**Procedure**

1. Set the `audit` parameter in the `scylla.yaml` file to `table`.

   For example:
   ```shell
   # audit setting
   # 'audit' config option controls if and where to output audited events:
   audit: "table"
   #
   # List of statement categories that should be audited.
   audit_categories: "DCL,DDL,AUTH"
   #
   # List of tables that should be audited.
   audit_tables: "mykespace.mytable"
   #
   # List of keyspaces that should be fully audited.
   # All tables in those keyspaces will be audited
   audit_keyspaces: "mykespace"
   ```
2. Restart the ScyllaDB node.

   Supported OS
   ```shell
   sudo systemctl restart scylla-server
   ```

   Docker
   ```shell
   docker exec -it some-scylla supervisorctl restart scylla
   ```

   (without restarting *some-scylla* container)

   Table output example (CQL drop table):
   ```shell
   SELECT * FROM audit.audit_log ;
   ```

   returns:
   ```none
    date                    | node         | event_time                           | category | consistency | error | keyspace_name | operation                    | source          | table_name  | username |
   -------------------------+--------------+--------------------------------------+----------+-------------+-------+---------------+------------------------------+-----------------+-------------+----------+
   2018-03-18 00:00:00+0000 | 10.143.2.108 | 3429b1a5-2a94-11e8-8f4e-000000000001 |      DDL |         ONE | False |           nba | DROP TABLE nba.team_roster ; | 127.0.0.1       | team_roster | Scylla   |
   (1 row)
   ```

<a id="auditing-table-and-syslog-storage"></a>

### Storing Audit Messages in a Table and Syslog Simultaneously

**Procedure**

1. Follow both procedures from above, and set the `audit` parameter in the `scylla.yaml` file to both `syslog` and `table`. You need to restart ScyllaDB only once.

   To have both syslog and table you need to specify both backends separated by a comma:
   ```shell
   audit: "syslog,table"
   ```

## Handling Audit Failures

In some cases, auditing may not be possible, for example, when:

* A table is used as the audit’s backend, and the partitions where the audit rows are saved are unavailable because the nodes holding those partitions are down or unreachable due to network issues.
* Syslog is used as the audit’s backend, and the Syslog sink (a regular Unix socket) is unresponsive or unavailable.

If the audit fails and audit messages are not stored in the configured audit’s backend, you can still review the audit log in the regular ScyllaDB logs.

The following example shows audit information in the regular ScyllaDB logs in the case when the Syslog backend is broken (for example, because the socket was closed) and you tried to connect to a node with incorrect credentials:

> ```shell
> ERROR 2024-01-15 14:09:41,516 [shard 0:sl:d] audit - Unexpected exception when writing login log with: node_ip <IP:port> client_ip <IP:port> username <username> error true exception audit::audit_exception (Starting syslog audit backend failed (sending a message to <socket_path> resulted in sendto: No such file or directory).)
> ```

## Additional Resources

* [Authorization](https://docs.scylladb.com/manual/branch-2026.2/operating-scylla/security/authorization.md)
* [Authentication](https://docs.scylladb.com/manual/branch-2026.2/operating-scylla/security/authentication.md)
