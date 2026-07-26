# Creating a Superuser

There is no default superuser role in ScyllaDB.
Users with a superuser role have full access to the database and can run
any CQL command on the database resources.

There are two ways you can create a superuser in ScyllaDB:

- [Using the ScyllaDB Maintenance Socket to create a superuser role](#create-superuser-using-maintenance-socket)
- [Using an existing superuser account to create a new superuser role](#create-superuser-using-existing-superuser)

When setting up a new cluster, use the maintenance socket approach to create the first superuser.

<a id="create-superuser-using-maintenance-socket"></a>

## Setting Up a Superuser Using the Maintenance Socket

If no superuser account exists in the cluster, which is the case for new clusters, you can create a superuser using the ScyllaDB Maintenance Socket.
In order to do that, the node must have the maintenance socket enabled.
See [Admin Tools: Maintenance Socket](https://docs.scylladb.com/manual/master/operating-scylla/admin-tools/maintenance-socket.md).

To create a superuser using the maintenance socket, you should:

1. Connect to the node using `cqlsh` over the maintenance socket.

```shell
cqlsh <maintenance_socket_path>
```

Replace `<maintenance_socket_path>` with the socket path configured in `scylla.yaml`.

1. Create new superuser role using `CREATE ROLE` command.

```cql
CREATE ROLE <new_superuser>  WITH SUPERUSER = true AND LOGIN = true and PASSWORD = '<new_superuser_password>';
```

1. Verify that you can log in to your node using `cqlsh` command with the new password.

```shell
cqlsh -u <new_superuser>
Password:
```

#### NOTE
Enter the value of <new_superuser_password> password when prompted. The input is not displayed.

1. Show all the roles to verify that the new superuser was created:

```cql
LIST ROLES;
```

<a id="create-superuser-using-existing-superuser"></a>

## Setting Up a Superuser Using an Existing Superuser Account

To create a superuser using an existing superuser account, you should:

1. Log in to cqlsh using an existing superuser account.

```shell
cqlsh -u <existing_superuser>
Password:
```

#### NOTE
Enter the value of <existing_superuser_password> password when prompted. The input is not displayed.

1. Create a new superuser.

```cql
CREATE ROLE <new_superuser>  WITH SUPERUSER = true AND LOGIN = true and PASSWORD = '<new_superuser_password>';
```

1. Verify that you can log in to your node using `cqlsh` command with the new password.

```shell
cqlsh -u <new_superuser>
Password:
```

#### NOTE
Enter the value of <new_superuser_password> password when prompted. The input is not displayed.

1. Show all the roles to verify that the new superuser was created:

```cql
LIST ROLES;
```
