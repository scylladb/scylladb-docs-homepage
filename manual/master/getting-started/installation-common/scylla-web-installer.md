# ScyllaDB Web Installer for Linux

ScyllaDB Web Installer is a platform-agnostic installation script you can run with `curl` to install ScyllaDB on Linux.

See [Install ScyllaDB Linux Packages](https://docs.scylladb.com/manual/master/getting-started/install-scylla/install-on-linux.md) for information on manually installing ScyllaDB with platform-specific installation packages.

## Prerequisites

Ensure that your platform is supported by the ScyllaDB version you want to install.
See [OS Support by Platform and Version](https://docs.scylladb.com/stable/versioning/os-support-per-version.html).

## Install ScyllaDB with Web Installer

To install ScyllaDB with Web Installer, run:

```console
curl -sSf get.scylladb.com/server | sudo bash
```

By default, running the script installs the latest official version of ScyllaDB.

You can run the command with the `-h` or `--help` flag to print information about the script.

## Installing a Non-default Version

You can install a version other than the default. To get the list of supported
release versions, run:

```console
curl -sSf get.scylladb.com/server | sudo bash -s -- --list-active-releases
```

To install a non-default version, run the command with the `--scylla-version`
option to specify the version you want to install.

**Example**

```console
curl -sSf get.scylladb.com/server | sudo bash -s -- --scylla-version 2026.3
```

## Installing via Tarball

The Web Installer supports tarball installation as an alternative
to the default package manager-based installation. This is useful for installing ScyllaDB
on Linux distributions that are not officially supported via packages, or when you prefer
not to use the system package manager or when you do not have superuser privileges.

To install ScyllaDB using the tarball, run:

```console
curl -sSf get.scylladb.com/server | sudo bash -s -- --tarball
```

You can combine `--tarball` with `--scylla-version` to install a specific version:

```console
curl -sSf get.scylladb.com/server | sudo bash -s -- --tarball --scylla-version |CURRENT_VERSION|
```

On Linux distributions not supported via native packages, the Web Installer
automatically falls back to tarball installation.

See [Install ScyllaDB Without root Privileges](https://docs.scylladb.com/manual/master/getting-started/installation-common/unified-installer.md) for more information on the tarball-based (unified) installer.

## Install ScyllaDB Manager with Web Installer

You can use the Web Installer to install [ScyllaDB Manager](https://manager.docs.scylladb.com/), which provides automated backup, repair, and cluster management capabilities.

To install ScyllaDB Manager, run:

```console
curl -sSf get.scylladb.com/manager | sudo bash
```

By default, this installs the latest official version of ScyllaDB Manager, including both
`scylla-manager-server` and `scylla-manager-client` packages.

To install a specific version, use the `--manager-version` option:

```console
curl -sSf get.scylladb.com/manager | sudo bash -s -- --manager-version 3.10
```

Supported platforms for ScyllaDB Manager installation via Web Installer:

* Debian / Ubuntu
* RHEL / CentOS / Rocky Linux / Amazon Linux

For full ScyllaDB Manager documentation, configuration, and usage instructions,
see [ScyllaDB Manager Docs](https://manager.docs.scylladb.com/).

## Configure and Run ScyllaDB

1. Configure the following parameters in the `/etc/scylla/scylla.yaml` configuration file.
   * `cluster_name` - The name of the cluster. All the nodes in the cluster must have the same
     cluster name configured.
   * `seeds` - The IP address of the first node. Other nodes will use it as the first contact
     point to discover the cluster topology when joining the cluster.
   * `listen_address` - The IP address that ScyllaDB uses to connect to other nodes in the cluster.
   * `rpc_address` - The IP address of the interface for CQL client connections.
2. Run the `scylla_setup` script to tune the system settings and determine the optimal configuration.
   ```console
   sudo scylla_setup
   ```

   * The script invokes a set of [scripts](https://docs.scylladb.com/manual/master/getting-started/system-configuration.md#system-configuration-scripts) to configure several operating system settings; for example, it sets
     RAID0 and XFS filesystem.
   * The script runs a short (up to a few minutes) benchmark on your storage and generates the `/etc/scylla.d/io.conf`
     configuration file. When the file is ready, you can start ScyllaDB. ScyllaDB will not run without XFS
     or `io.conf` file.
   * You can bypass this check by running ScyllaDB in [developer mode](https://docs.scylladb.com/manual/master/getting-started/installation-common/dev-mod.md).
     We recommend against enabling developer mode in production environments to ensure ScyllaDB’s maximum performance.
3. Run ScyllaDB as a service (if not already running).
   ```console
   sudo systemctl start scylla-server
   ```

Now you can start using ScyllaDB. Here are some tools you may find useful.

Run nodetool:

```console
nodetool status
```

Run cqlsh:

```console
cqlsh
```
