# Upgrade - ScyllaDB 2026.x.y to 2026.x.z (Patch Upgrades)

This document describes a step-by-step procedure for upgrading from
ScyllaDB 2026.x.y  to ScyllaDB 2026.x.z (where “z” is
the latest available version), and rolling back to version 2026.x.y
if necessary.

This guide covers upgrading ScyllaDB on Red Hat Enterprise Linux (RHEL),
CentOS, Debian, and Ubuntu.
See [OS Support by Platform and Version](https://docs.scylladb.com/stable/versioning/os-support-per-version.html)
for information about supported versions.

It also applies to the ScyllaDB official image on EC2, GCP, or Azure.

See [Upgrade Policy](https://docs.scylladb.com/stable/versioning/upgrade-policy.html) for the ScyllaDB upgrade policy.

## Upgrade Procedure

#### NOTE
Apply the following procedure **serially** on each node. Do not move to the next
node before validating that the node is up and running the new version.

A ScyllaDB upgrade is a rolling procedure that does **not** require a full cluster
shutdown. For each of the nodes in the cluster, you will:

1. Drain the node and back up the data.
2. Backup configuration file.
3. Stop ScyllaDB.
4. Download and install new ScyllaDB packages.
5. Start ScyllaDB.
6. Validate that the upgrade was successful.

**Before** upgrading, check which version you are running now using
`scylla --version`. Note the current version in case you want to roll back
the upgrade.

**During** the rolling upgrade it is highly recommended:

* Not to use new 2026.x.z features.
* Not to run administration functions, like repairs, refresh, rebuild or add
  or remove nodes. See
  [sctool](https://manager.docs.scylladb.com/stable/sctool/) for suspending
  ScyllaDB Manager’s scheduled or running repairs.
* Not to apply schema changes.

## Upgrade Steps

### Back up the data

Back up all the data to an external device. We recommend using
[ScyllaDB Manager](https://manager.docs.scylladb.com/stable/backup/index.html)
to create backups.

Alternatively, you can use the `nodetool snapshot` command.
For **each** node in the cluster, run the following:

```sh
nodetool drain
nodetool snapshot
```

Take note of the directory name that nodetool gives you, and copy all
the directories with this name under `/var/lib/scylla` to a backup device.

When the upgrade is completed on all nodes, remove the snapshot with the
`nodetool clearsnapshot -t <snapshot>` command to prevent running out of
space.

### Back up the configuration file

Back up the `scylla.yaml` configuration file and the ScyllaDB packages
in case you need to roll back the upgrade.

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

You don’t need to update the ScyllaDB DEB or RPM repo when you upgrade to
a patch release.

Debian/Ubuntu

To install a patch version on Debian or Ubuntu, run:

```sh
sudo apt-get clean all
sudo apt-get update
sudo apt-get dist-upgrade scylla
```

Answer ‘y’ to the first two questions.

RHEL/CentOS

To install a patch version on RHEL or CentOS, run:

```sh
sudo yum clean all
sudo yum update scylla\* -y
```

EC2/GCP/Azure Ubuntu Image

If you’re using the ScyllaDB official image (recommended), see
the **Debian/Ubuntu** tab for upgrade instructions.

If you’re using your own image and have installed ScyllaDB packages for
Ubuntu or Debian, you need to apply an extended upgrade procedure:

1. Install the new ScyllaDB version with the additional
   `scylla-machine-image` package:
   > ```console
   > sudo apt-get clean all
   > sudo apt-get update
   > sudo apt-get dist-upgrade scylla
   > sudo apt-get dist-upgrade scylla-machine-image
   > ```
2. Run `scylla_setup` without `running io_setup`.
3. Run `sudo /opt/scylladb/scylla-machine-image/scylla_cloud_io_setup`.

### Start the node

```sh
sudo service start scylla-server
```

### Validate

1. Check cluster status with `nodetool status` and make sure **all** nodes,
   including the one you just upgraded, are in UN status.
2. Use `curl -X GET "http://localhost:10000/storage_service/scylla_release_version"`
   to check the ScyllaDB version.
3. Use `journalctl _COMM=scylla` to check there are no new errors in the log.
4. Check again after 2 minutes to validate that no new issues are introduced.

Once you are sure the node upgrade is successful, move to the next node in
the cluster.

## Rollback Procedure

The following procedure describes a rollback from ScyllaDB release
2026.x.z to 2026.x.y. Apply this procedure if an upgrade from
2026.x.y to 2026.x.z failed before completing on all nodes.

* Use this procedure only on nodes you upgraded to 2026.x.z.
* Execute the following commands one node at a time, moving to the next node only
  after the rollback procedure is completed successfully.

ScyllaDB rollback is a rolling procedure that does **not** require a full
cluster shutdown. For each of the nodes to roll back to 2026.x.y, you will:

1. Drain the node and stop ScyllaDB.
2. Downgrade to the previous release.
3. Restore the configuration file.
4. Restart ScyllaDB.
5. Validate the rollback success.

## Rollback Steps

### Gracefully shutdown ScyllaDB

```sh
nodetool drain
sudo service stop scylla-server
```

### Downgrade to the previous release

Debian/Ubuntu

To downgrade to 2026.x.y on Debian or Ubuntu, run:

```console
sudo apt-get install scylla=2026.x.y\* scylla-server=2026.x.y\* scylla-tools=2026.x.y\* scylla-tools-core=2026.x.y\* scylla-kernel-conf=2026.x.y\* scylla-conf=2026.x.y\*
```

Answer ‘y’ to the first two questions.

RHEL/CentOS

To downgrade to 2026.x.y on RHEL or CentOS, run:

```console
sudo yum downgrade scylla\*-2026.x.y-\* -y
```

EC2/GCP/Azure Ubuntu Image

If you’re using the ScyllaDB official image (recommended), see
the **Debian/Ubuntu** tab for upgrade instructions.

If you’re using your own image and have installed ScyllaDB packages for
Ubuntu or Debian, you need to additionally downgrade
the `scylla-machine-image` package.

```console
sudo apt-get install scylla=2026.x.y\* scylla-server=2026.x.y\* scylla-tools=2026.x.y\* scylla-tools-core=2026.x.y\* scylla-kernel-conf=2026.x.y\* scylla-conf=2026.x.y\*
sudo apt-get install scylla-machine-image=2026.x.y\*
```

Answer ‘y’ to the first two questions.

### Restore the configuration file

```sh
sudo rm -rf /etc/scylla/scylla.yaml
sudo cp -a /etc/scylla/scylla.yaml.backup /etc/scylla/scylla.yaml
```

### Start the node

```sh
sudo service scylla-server start
```

### Validate

Check upgrade instruction above for validation. Once you are sure the node
rollback is successful, move to the next node in the cluster.
