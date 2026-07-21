# MCP Toolbox for Databases

![MCP Toolbox for Databases logo](_static/img/integrations/mcp-toolbox-logo.png)

[MCP Toolbox for Databases](https://github.com/googleapis/mcp-toolbox) is an
open source MCP server that exposes database operations as tools consumable by
AI agents and LLMs. The ScyllaDB integration lets agents execute pre-defined CQL
statements against a ScyllaDB cluster via the `scylladb-cql` tool type.

## Prerequisites

Install MCP Toolbox for Databases following the
[official installation guide](https://mcp-toolbox.dev/documentation/getting-started/introduction/).

## Configure a ScyllaDB Source

A *source* tells MCP Toolbox how to connect to your ScyllaDB cluster. Create a
`tools.yaml` file and add a source block of `type: scylladb`.

Self-hosted ScyllaDB:

```yaml
kind: source
name: my-scylladb-source
type: scylladb
hosts:
  - 127.0.0.1
keyspace: my_keyspace
protoVersion: 4
username: ${USER_NAME}
password: ${PASSWORD}
```

ScyllaDB Cloud:

When connecting to ScyllaDB Cloud, set `localDC` to the datacenter name shown
on the **Connect** tab of your cluster in the
[ScyllaDB Cloud Console](https://cloud.scylladb.com/). This enables
DC-aware, token-aware load balancing, which is required for ScyllaDB Cloud
connections.

```yaml
kind: source
name: my-scylladb-cloud-source
type: scylladb
hosts:
  - node-0.your-cluster.us-east-1.cloud.scylladb.com
  - node-1.your-cluster.us-east-1.cloud.scylladb.com
  - node-2.your-cluster.us-east-1.cloud.scylladb.com
keyspace: my_keyspace
username: ${USER_NAME}
password: ${PASSWORD}
localDC: AWS_US_EAST_1
```

### Source Reference

| Field                    | Type     | Required   | Description                                                                                                                                              |
|--------------------------|----------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `type`                   | string   | yes        | Must be `"scylladb"`.                                                                                                                                    |
| `hosts`                  | string[] | yes        | List of contact point addresses (e.g., `["192.168.1.1:9042"]`). The<br/>default port is 9042 if not specified.                                           |
| `keyspace`               | string   | no         | Name of the keyspace to connect to.                                                                                                                      |
| `protoVersion`           | integer  | no         | CQL native protocol version (e.g., `4`).                                                                                                                 |
| `username`               | string   | no         | ScyllaDB username.                                                                                                                                       |
| `password`               | string   | no         | ScyllaDB password.                                                                                                                                       |
| `localDC`                | string   | no         | Datacenter name for DC-aware load balancing (e.g.,<br/>`"AWS_US_EAST_1"`). Required for ScyllaDB Cloud connections.                                      |
| `caPath`                 | string   | no         | Path to a CA certificate file. Use when connecting to a self-hosted<br/>ScyllaDB cluster with a private or custom CA. Not needed for<br/>ScyllaDB Cloud. |
| `certPath`               | string   | no         | Path to the client certificate file for mutual TLS (mTLS).                                                                                               |
| `keyPath`                | string   | no         | Path to the client private key file for mutual TLS (mTLS). Required<br/>together with `certPath`.                                                        |
| `enableHostVerification` | bool     | no         | Whether to verify the server hostname against its TLS certificate.<br/>Defaults to `false`.                                                              |

## Define a `scylladb-cql` Tool

A `scylladb-cql` tool executes a pre-defined CQL statement against the
configured source. The statement is executed as a prepared statement;
positional placeholders use `?`.

Basic parameters:

```yaml
kind: tool
name: search_users_by_email
type: scylladb-cql
source: my-scylladb-source
statement: |
  SELECT user_id, email, first_name, last_name, created_at
  FROM users
  WHERE email = ?
description: |
  Use this tool to retrieve user information by email address.
  Returns user ID, email, first name, last name, and creation timestamp.
  Example:
  {{
      "email": "user@example.com",
  }}
parameters:
  - name: email
    type: string
    description: User's email address
```

Template parameters allow dynamic identifiers such as keyspace or table names.
Because template parameters are interpolated before the statement is prepared,
they are more vulnerable to CQL injection. Use basic parameters whenever
possible.

```yaml
kind: tool
name: list_keyspace_table
type: scylladb-cql
source: my-scylladb-source
statement: |
  SELECT * FROM {{.keyspace}}.{{.tableName}};
description: |
  Use this tool to list all rows from a table in a keyspace.
  Example:
  {{
      "keyspace": "my_keyspace",
      "tableName": "users",
  }}
templateParameters:
  - name: keyspace
    type: string
    description: Keyspace containing the table
  - name: tableName
    type: string
    description: Table to select from
```

### Tool Reference

| Field                | Type               | Required   | Description                                                                                                                        |
|----------------------|--------------------|------------|------------------------------------------------------------------------------------------------------------------------------------|
| `type`               | string             | yes        | Must be `"scylladb-cql"`.                                                                                                          |
| `source`             | string             | yes        | Name of the ScyllaDB source to execute the statement on.                                                                           |
| `description`        | string             | yes        | Description of the tool passed to the LLM.                                                                                         |
| `statement`          | string             | yes        | CQL statement to execute.                                                                                                          |
| `authRequired`       | []string           | no         | List of authentication requirements for the source.                                                                                |
| `parameters`         | parameters         | no         | Positional parameters inserted into the prepared CQL statement.                                                                    |
| `templateParameters` | templateParameters | no         | Template parameters interpolated into the CQL statement before<br/>it is prepared. Use only when dynamic identifiers are required. |

## Additional Resources

* [MCP Toolbox ScyllaDB source reference](https://mcp-toolbox.dev/integrations/scylladb/source/)
* [scylladb-cql tool reference](https://mcp-toolbox.dev/integrations/scylladb/tools/scylladb-cql/)
* [MCP Toolbox documentation](https://mcp-toolbox.dev/documentation/)
* [ScyllaDB Cloud](https://cloud.scylladb.com/)
