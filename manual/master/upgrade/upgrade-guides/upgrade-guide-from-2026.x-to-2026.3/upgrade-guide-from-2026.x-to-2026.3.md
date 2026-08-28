# Upgrade from ScyllaDB 2026.x to ScyllaDB 2026.3

This document describes a step-by-step procedure for upgrading from ScyllaDB 2026.x
to ScyllaDB 2026.3 and rollback to version 2026.x if necessary.

This guide covers upgrading ScyllaDB on Red Hat Enterprise Linux (RHEL), CentOS, Debian,
and Ubuntu. See [OS Support by Platform and Version](https://docs.scylladb.com/stable/versioning/os-support-per-version.html)
for information about supported versions. It also applies when using the ScyllaDB official image on EC2, GCP, or Azure.

See [Upgrade Policy](https://docs.scylladb.com/stable/versioning/upgrade-policy.html) for the ScyllaDB upgrade policy.

## Before You Upgrade ScyllaDB

**Upgrade Your Driver**

If you’re using a [ScyllaDB driver](https://docs.scylladb.com/stable/drivers/index.html),
upgrade the driver before upgrading ScyllaDB. The latest two versions of each driver
are supported. See [Driver Support](https://docs.scylladb.com/stable/versioning/driver-support.html).

**Upgrade ScyllaDB Monitoring Stack**

If you’re using the ScyllaDB Monitoring Stack, verify that your Monitoring Stack
version supports the ScyllaDB version to which you want to upgrade. See
[ScyllaDB Monitoring Stack Support Matrix](https://monitoring.docs.scylladb.com/stable/reference/matrix.html).

We recommend upgrading the Monitoring Stack to the latest version.

**Check Feature Updates**

See the ScyllaDB Release Notes for the latest updates. The Release Notes are published
at the [ScyllaDB Community Forum](https://forum.scylladb.com/c/scylladb-release-notes/).

## Upgrade Procedure

A ScyllaDB upgrade is a rolling procedure that does **not** require full cluster shutdown.
For each of the nodes in the cluster, serially (i.e., one node at a time), you will:

* Check that the cluster’s schema is synchronized
* Drain the node and backup the data
* Backup the configuration file
* Stop ScyllaDB
* Download and install new ScyllaDB packages
* Start ScyllaDB
* Validate that the upgrade was successful

**During** the rolling upgrade, it is highly recommended:

* Not to use the new 2026.3 features.
* Not to run administration functions, such as repairs, refresh, rebuild, or add
  or remove nodes. See [sctool](https://manager.docs.scylladb.com/stable/sctool/) for suspending
  ScyllaDB Manager’s scheduled or running repairs.
* Not to apply schema changes.

## Upgrade Steps

### Check the cluster schema

Make sure that all nodes have the schema synchronized before the upgrade. The upgrade
procedure will fail if there is a schema disagreement between nodes.

```sh
nodetool describecluster
```

### Backup the data

Before any major procedure, like an upgrade, it is recommended to backup all the data
to an external device.
We recommend using [ScyllaDB Manager](https://manager.docs.scylladb.com/stable/backup/index.html)
to create backups.

Alternatively, you can use the `nodetool snapshot` command.
For **each** node in the cluster, run the following:

```sh
nodetool drain
nodetool snapshot
```

Take note of the directory name that nodetool gives you, and copy all the directories
having that name under `/var/lib/scylla` to an external backup device.

When the upgrade is completed on all nodes, remove the snapshot with the
`nodetool clearsnapshot -t <snapshot>` command to prevent running out of space.

### Backup the configuration file

Back up the `scylla.yaml` configuration file and the ScyllaDB packages
in case you need to rollback the upgrade.

Debian/Ubuntu

```sh
sudo cp -a /etc/scylla/scylla.yaml /etc/scylla/scylla.yaml.backup
sudo cp /etc/apt/sources.list.d/scylla.list ~/scylla.list-backup
```

RHEL/CentOS

```sh
sudo cp -a /etc/scylla/scylla.yaml /etc/scylla/scylla.yaml.backup
sudo cp /etc/yum.repos.d/scylla.repo ~/scylla.repo-backup
```

### Gracefully stop the node

```sh
sudo service scylla-server stop
```

### Download and install the new release

Before upgrading, check what version you are running now using `scylla --version`.
You should take note of the current version in case you want to [rollback](#rollback) the upgrade.

Debian/Ubuntu

1. Update the ScyllaDB deb repo to 2026.3.
   > ```console
   > sudo wget -O /etc/apt/sources.list.d/scylla.list https://downloads.scylladb.com/deb/debian/scylla-2026.2.list
   > ```
2. Install the new ScyllaDB version:
   > ```console
   > sudo apt-get clean all
   > sudo apt-get update
   > sudo apt-get dist-upgrade scylla
   > ```

Answer ‘y’ to the first two questions.

RHEL/CentOS

1. Update the ScyllaDB rpm repo to 2026.3.
   > ```console
   > sudo curl -o /etc/yum.repos.d/scylla.repo -L https://downloads.scylladb.com/rpm/centos/scylla-2026.2.repo
   > ```
2. Install the new ScyllaDB version:
   > ```sh
   > sudo yum clean all
   > sudo yum update scylla\* -y
   > ```

EC2/GCP/Azure Ubuntu Image

If you’re using the ScyllaDB official image (recommended), see the **Debian/Ubuntu**
tab for upgrade instructions.

If you’re using your own image and installed ScyllaDB packages for Ubuntu or Debian,
you need to apply an extended upgrade procedure:

1. Update the ScyllaDB deb repo (see the **Debian/Ubuntu** tab).
2. Install the new ScyllaDB version with the additional `scylla-machine-image` package:
   > ```console
   > sudo apt-get clean all
   > sudo apt-get update
   > sudo apt-get dist-upgrade scylla
   > sudo apt-get dist-upgrade scylla-machine-image
   > ```
3. Run `scylla_setup` without `running io_setup`.
4. Run `sudo /opt/scylladb/scylla-machine-image/scylla_cloud_io_setup`.

### Start the node

```sh
sudo service scylla-server start
```

### Validate

1. Check cluster status with `nodetool status` and make sure **all** nodes, including
   the one you just upgraded, are in `UN` status.
2. Use `curl -X GET "http://localhost:10000/storage_service/scylla_release_version"`
   to check the ScyllaDB version. Validate that the version matches the one you upgraded to.
3. Check scylla-server log (by `journalctl _COMM=scylla`) and `/var/log/syslog` to
   validate there are no new errors in the log.
4. Check again after two minutes to validate no new issues are introduced.

Once you are sure the node upgrade was successful, move to the next node in the cluster.

<a id="rollback"></a>

## Rollback Procedure

#### WARNING
The rollback procedure can be applied **only** if some nodes have not been
upgraded to 2026.3 yet. As soon as the last node in the rolling upgrade
procedure is started with 2026.3, rollback becomes impossible. At that
point, the only way to restore a cluster to 2026.x is by restoring it
from backup.

The following procedure describes a rollback from ScyllaDB 2026.3 to
2026.x. Apply this procedure if an upgrade from 2026.x to
2026.3 fails before completing on all nodes.

* Use this procedure only on the nodes you upgraded to 2026.3.
* Execute the following commands one node at a time, moving to the next node
  only after the rollback procedure is completed successfully.

ScyllaDB rollback is a rolling procedure that does **not** require full cluster shutdown.
For each of the nodes you rollback to 2026.x, serially (i.e., one node
at a time), you will:

* Drain the node and stop ScyllaDB
* Retrieve the old ScyllaDB packages
* Restore the configuration file
* Reload systemd configuration
* Restart ScyllaDB
* Validate the rollback success

Apply the procedure **serially** on each node. Do not move to the next node
before validating that the rollback was successful and the node is up and
running the old version.

## Rollback Steps

### Drain and gracefully stop the node

```sh
nodetool drain
sudo service scylla-server stop
```

### Restore and install the old release

Debian/Ubuntu

1. Remove the old repo file.
   > ```sh
   > sudo rm -rf /etc/apt/sources.list.d/scylla.list
   > ```
2. Restore the 2026.x packages backed up during the upgrade.
   > ```sh
   > sudo cp ~/scylla.list-backup /etc/apt/sources.list.d/scylla.list
   > sudo chown root.root /etc/apt/sources.list.d/scylla.list
   > sudo chmod 644 /etc/apt/sources.list.d/scylla.list
   > ```
3. Install:
   > ```default
   > sudo apt-get update
   > sudo apt-get remove scylla\* -y
   > sudo apt-get install scylla
   > ```

Answer ‘y’ to the first two questions.

RHEL/CentOS

1. Remove the old repo file.
   > ```sh
   > sudo rm -rf /etc/yum.repos.d/scylla.repo
   > ```
2. Restore the 2026.x packages backed up during the upgrade procedure.
   > ```sh
   > sudo cp ~/scylla.repo-backup /etc/yum.repos.d/scylla.repo
   > sudo chown root.root /etc/yum.repos.d/scylla.repo
   > sudo chmod 644 /etc/yum.repos.d/scylla.repo
   > ```
3. Install:
   > ```console
   > sudo yum clean all
   > sudo yum remove scylla\*
   > sudo yum install scylla
   > ```

EC2/GCP/Azure Ubuntu Image

If you’re using the ScyllaDB official image (recommended), see the **Debian/Ubuntu**
tab for upgrade instructions.

If you’re using your own image and installed ScyllaDB packages for Ubuntu or Debian,
you need to additionally restore the `scylla-machine-image` package.

1. Restore the 2026.x packages backed up during the upgrade
   (see the **Debian/Ubuntu** tab).
2. Install:
   > ```default
   > sudo apt-get update
   > sudo apt-get remove scylla\* -y
   > sudo apt-get install scylla
   > sudo apt-get install scylla-machine-image
   > ```

> Answer ‘y’ to the first two questions.

### Restore the configuration file

```sh
sudo rm -rf /etc/scylla/scylla.yaml
sudo cp /etc/scylla/scylla.yaml-backup /etc/scylla/scylla.yaml
```

### Reload systemd configuration

You must reload the unit file if the systemd unit file is changed.

```sh
sudo systemctl daemon-reload
```

### Start the node

```sh
sudo service scylla-server start
```

### Validate

Check the upgrade instructions above for validation. Once you are sure the node
rollback is successful, move to the next node in the cluster.
