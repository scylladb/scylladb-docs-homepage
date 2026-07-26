# Install ScyllaDB Without root Privileges

This document covers installing, uninstalling, and upgrading ScyllaDB using Unified Installer.
Unified Installer is recommended when you do not have root privileges to the server.
If you have root privileges, we recommend installing ScyllaDB with
[ScyllaDB Web Installer](https://docs.scylladb.com/manual/master/getting-started/installation-common/scylla-web-installer.md)
or by downloading the OS-specific packages (RPMs and DEBs) and installing them with
the package manager (dnf and apt).

## Prerequisites

Ensure your platform is supported by the ScyllaDB version you want to install.
See [OS Support](https://docs.scylladb.com/stable/versioning/os-support-per-version.html)
for information about supported Linux distributions and versions.

## Download and Install

1. Download the latest tar.gz file for ScyllaDB version (x86 or ARM) from `https://downloads.scylladb.com/downloads/scylla/relocatable/scylladb-<version>/`.

   **Example** for version 2025.1:
   - Go to [https://downloads.scylladb.com/downloads/scylla/relocatable/scylladb-2025.1/](https://downloads.scylladb.com/downloads/scylla/relocatable/scylladb-2025.1/)
   - Download the `scylla-unified` file for the patch version you want to
     install. For example, to install 2025.1.9 (x86), download
     `scylla-unified-2025.1.9-0.20251010.6c539463bbda.x86_64.tar.gz`.
2. Uncompress the downloaded package.

   **Example** for version 2025.1.9 (x86) (downloaded in the previous step):
   ```default
   tar xvfz scylla-unified-2025.1.9-0.20251010.6c539463bbda.x86_64.tar.gz
   ```
3. (Root offline installation only) For root offline installation on Debian-like
   systems, two additional packages, `xfsprogs` and `mdadm`, should be
   installed to be used in RAID setup.
4. Install ScyllaDB as a user with non-root privileges:
   ```console
   ./install.sh --nonroot
   ```

## Configure and Run ScyllaDB

1. Run the ScyllaDB setup script:
   ```console
   ~/scylladb/sbin/scylla_setup
   ```
2. Start ScyllaDB:
   ```console
   systemctl --user start scylla-server
   ```
3. Verify that ScyllaDB is running:
   ```console
   systemctl --user status scylla-server
   ```

Now you can start using ScyllaDB. Here are some tools you may find useful.

Run nodetool:

```console
~/scylladb/bin/nodetool nodetool status
```

Run cqlsh:

```console
~/scylladb/bin/cqlsh
```

#### NOTE
You can avoid adding the extended prefix to the commands by exporting the binary directories to PATH:

`export PATH=$PATH:~/scylladb/python3/bin:~/scylladb/share/cassandra/bin/:~/scylladb/bin:~/scylladb/sbin`

## Upgrade/ Downgrade/ Uninstall

<a id="unified-installed-upgrade"></a>

### Upgrade

The unified package is based on a binary package; it’s not a RPM / DEB packages, so it doesn’t upgrade or downgrade by yum / apt. To upgrade ScyllaDB, run the `install.sh` script.

Root install:

```sh
./install.sh --upgrade
```

Nonroot install

```sh
./install.sh --upgrade --nonroot
```

#### NOTE
The installation script does not upgrade scylla-tools. You will have to upgrade them separately.

### Uninstall

Root uninstall:

```sh
sudo ./uninstall.sh
```

Nonroot uninstall

```sh
./uninstall.sh --nonroot
```

### Downgrade

To downgrade to your original ScyllaDB version, use the [Uninstall]() procedure, then install the original ScyllaDB version.

## Next Steps

* [Configure ScyllaDB](https://docs.scylladb.com/manual/master/getting-started/system-configuration.md)
* Manage your clusters with [ScyllaDB Manager](https://manager.docs.scylladb.com/)
* Monitor your cluster and data with [ScyllaDB Monitoring](https://monitoring.docs.scylladb.com/)
* Get familiar with ScyllaDB’s [command line reference guide](https://docs.scylladb.com/manual/master/operating-scylla/nodetool.md).
* Learn about ScyllaDB at [ScyllaDB University](https://university.scylladb.com/)
