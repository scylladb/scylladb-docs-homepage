# ScyllaDB Auditing Guide

Auditing allows the administrator to monitor activities on a Scylla cluster, including queries and data changes.
The information is stored in a Syslog or a Scylla table.

## Prerequisite

Enable ScyllaDB [Authentication](https://docs.scylladb.com/manual/branch-2025.4/operating-scylla/security/authentication.md) and [Authorization](https://docs.scylladb.com/manual/branch-2025.4/operating-scylla/security/enable-authorization.md).

## Enabling Audit

By default, auditing is **disabled**. Enabling auditing is controlled by the `audit:` parameter in the `scylla.yaml` file.
You can set the following options:

* `none` - Audit is disabled (default).
* `table` - Audit is enabled, and messages are stored in a Scylla table.
* `syslog` - Audit is enabled, and messages are sent to Syslog.

Configuring any other value results in an error at Scylla startup.

## Configuring Audit

The audit can be tuned using the following flags or `scylla.yaml` entries:

| Flag             | Default Value        | Description                                                                                                                                                        |
|------------------|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| audit_categories | “DCL,DDL,AUTH,ADMIN” | Comma-separated list of statement categories that should be audited                                                                                                |
| audit_tables     | “”                   | Comma-separated list of table names that should be audited, in the format of <keyspacename>.<tablename>                                                            |
| audit_keyspaces  | “”                   | Comma-separated list of keyspaces that should be audited. You must specify at least one keyspace.<br/>If you leave this option empty, no keyspace will be audited. |

To audit all the tables in a keyspace, set the `audit_keyspaces` with the keyspace you want to audit and leave `audit_tables` empty.

You can use DCL, AUTH, and ADMIN audit categories without including any keyspace or table.

### audit_categories parameter description

| Parameter   | Logs Description                                                                                                                                                                                                                                   |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AUTH        | Logs login events                                                                                                                                                                                                                                  |
| DML         | Logs insert, update, delete, and other data manipulation language (DML) events                                                                                                                                                                     |
| DDL         | Logs object and role create, alter, drop, and other data definition language (DDL) events                                                                                                                                                          |
| DCL         | Logs grant, revoke, create role, drop role, and list roles events                                                                                                                                                                                  |
| QUERY       | Logs all queries                                                                                                                                                                                                                                   |
| ADMIN       | Logs service level operations: create, alter, drop, attach, detach, list.<br/>For [service level](https://docs.scylladb.com/manual/branch-2025.4/features/workload-prioritization.md#workload-priorization-service-level-management)<br/>auditing. |

Note that audit for every DML or QUERY might impact performance and consume a lot of storage.

## Configuring Audit Storage

Auditing messages can be sent to [Syslog](#auditing-syslog-storage) or stored in a Scylla [table](#auditing-table-storage).
Currently, auditing messages can only be saved to one location at a time. You cannot log into both a table and the Syslog.

<a id="auditing-syslog-storage"></a>

### Storing Audit Messages in Syslog

**Procedure**

1. Set the `audit` parameter in the `scylla.yaml` file to `syslog`.

   For example:
   ```shell
   # audit setting
   # by default, Scylla does not audit anything.
   # It is possible to enable auditing to the following places:
   #   - audit.audit_log column family by setting the flag to "table"
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
2. Restart the Scylla node.

Supported OS

```shell
sudo systemctl restart scylla-server
```

Docker

```shell
docker exec -it some-scylla supervisorctl restart scylla
```

(without restarting *some-scylla* container)

By default, audit messages are written to the same destination as Scylla [logging](https://docs.scylladb.com/manual/branch-2025.4/getting-started/logging.md), with `scylla-audit` as the process name.

Logging output example (drop table):

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

Messages are stored in a Scylla table named `audit.audit_log`.

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
   # by default, Scylla does not audit anything.
   # It is possible to enable auditing to the following places:
   #   - audit.audit_log column family by setting the flag to "table"
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
2. Restart Scylla node.

   Supported OS
   ```shell
   sudo systemctl restart scylla-server
   ```

   Docker
   ```shell
   docker exec -it some-scylla supervisorctl restart scylla
   ```

   (without restarting *some-scylla* container)

   Table output example (drop table):
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

## Handling Audit Failures

In some cases, auditing may not be possible, for example, when:

* A table is used as the audit’s backend, and the audit partition where the audit row is saved is not available because the node that holds this partition is down.
* Syslog is used as the audit’s backend, and the Syslog sink (a regular unix socket) is unresponsive/unavailable.

If the audit fails and audit messages are not stored in the configured audit’s backend, you can still review the audit log in the regular ScyllaDB logs.

The following example shows audit information in the regular ScyllaDB logs in the case when the Syslog backend is broken (for example, because the socket was closed) and you tried to connect to a node with incorrect credentials:

> ```shell
> ERROR 2024-01-15 14:09:41,516 [shard 0:sl:d] audit - Unexpected exception when writing login log with: node_ip <IP:port> client_ip <IP:port> username <username> error true exception audit::audit_exception (Starting syslog audit backend failed (sending a message to <socket_path> resulted in sendto: No such file or directory).)
> ```

## Additional Resources

* [Authorization](https://docs.scylladb.com/manual/branch-2025.4/operating-scylla/security/authorization.md)
* [Authentication](https://docs.scylladb.com/manual/branch-2025.4/operating-scylla/security/authentication.md)
