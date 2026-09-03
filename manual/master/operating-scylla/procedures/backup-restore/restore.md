# Restore from a Backup and Incremental Backup

Restoring a keyspace from a backup requires all snapshot files of the tables, and (if available) incremental backup files taken after the snapshot. Before restoring from backup, the table data must be truncated, making sure that the existing data does not overwrite the restored data.

#### NOTE
For cluster-wide backup and restore, see the [ScyllaDB Manager](https://manager.docs.scylladb.com/stable/restore/) documentation.

## Choosing a restore method

ScyllaDB supports several restore methods. Choose the one that matches where your backup files are and whether the cluster topology changed since the backup was taken:

* [Restore from object storage](#restore-object-storage) - restore SSTables backed up to S3-compatible object storage with [nodetool backup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/backup.md). Runs on a running cluster and works regardless of cluster topology changes since the backup.
* [Restore with load and stream](#restore-load-and-stream) - upload backed-up SSTable files to a running cluster; the data is streamed to the nodes owning it. Works regardless of cluster topology changes since the backup.
* [Restore to an identical cluster](#restore-procedure) - copy snapshot files back in place and restart the nodes. Requires a cluster with the same number of nodes and the same token distribution as at the time of the backup, and each node must be restored from the backup of the **same node**. Suitable for vnode-based keyspaces only.

For cluster-wide backup and restore, use [ScyllaDB Manager](https://manager.docs.scylladb.com/stable/restore/), which orchestrates the process across the cluster.

<a id="restore-prerequisites"></a>

## Prerequisites

The following steps and notes apply to all restore methods.

From **one** of the nodes, recreate the schema.
<br/>

`cqlsh -e "SOURCE '/path_to_schema/<schema_name.cql>'"`

For example:
<br/>

`cqlsh -e "SOURCE 'centos/db_schema.cql'"`

**Only** a superuser should perform it.
<br/>
If the tables you are restoring already exist and contain data, truncate each of them, so that the existing data does not overwrite the restored data. Truncating a base table also truncates its materialized views and secondary indexes, no extra action is needed for them.
<br/>

`cqlsh -e "TRUNCATE <keyspace_name>.<table_name>"`

For example:
<br/>

`cqlsh -e "TRUNCATE mykeyspace.team_players"`

#### NOTE
If you are restoring [encrypted backup files](https://docs.scylladb.com/manual/master/operating-scylla/security/encryption-at-rest.md), make sure ScyllaDB is configured with the same keys that were used to encrypt the data before starting the restore process.

<a id="restore-object-storage"></a>

## Restore from object storage

Use this method to restore SSTables backed up to S3-compatible object storage with [nodetool backup](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/backup.md). The node downloads the SSTables from the bucket and streams their contents to the nodes owning the data (load and stream), so the restore works regardless of cluster topology changes since the backup, and the cluster stays online.

The object storage endpoint must be configured on the nodes, as described in [Configuring Object Storage](https://docs.scylladb.com/manual/master/operating-scylla/admin.md#object-storage-configuration).

#### NOTE
If the table has any [Materialized Views (MV)](https://docs.scylladb.com/manual/master/features/materialized-views.md) or [Secondary Indexes (SI)](https://docs.scylladb.com/manual/master/features/secondary-indexes.md), view updates are generated automatically as the base table data is streamed. Restore the base table SSTables only; restoring MV or SI SSTables is not supported and will fail.

**Procedure**

1. Complete the [prerequisites](#restore-prerequisites).
2. List the backed-up SSTables in the bucket under the prefix used during the backup. The restore command takes the paths of the `TOC.txt` components of the SSTables to restore, **relative to the prefix** – the remainder of each object key after the prefix. Note that listing tools print full object keys, from the bucket root, so the prefix needs to be stripped. For example:
   ```shell
   aws s3 ls --recursive s3://bucket-foo/ks/cf/24601/ | awk '/-TOC.txt$/ { print $4 }' | sed 's|^ks/cf/24601/||'
   ```
3. Run [nodetool restore](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/restore.md), passing the endpoint, bucket, prefix, target keyspace and table, and the list of prefix-relative TOC paths:
   ```shell
   nodetool restore --endpoint s3.us-east-2.amazonaws.com --bucket bucket-foo --prefix ks/cf/24601 \
     --keyspace ks --table cf \
     me-3gdq_0bki_2dy4w2gqj6hoso4mw1-big-TOC.txt \
     me-3gdq_0bki_2dipc1ysb2x2a3btgh-big-TOC.txt
   ```

   Alternatively, put the same prefix-relative TOC paths (newline-separated) in a file and pass it with the `--sstables-file-list` option:
   ```shell
   cat > sstables.list <<EOF
   me-3gdq_0bki_2dy4w2gqj6hoso4mw1-big-TOC.txt
   me-3gdq_0bki_2dipc1ysb2x2a3btgh-big-TOC.txt
   EOF

   nodetool restore --endpoint s3.us-east-2.amazonaws.com --bucket bucket-foo --prefix ks/cf/24601 \
     --keyspace ks --table cf --sstables-file-list sstables.list
   ```
4. Monitor the restore. By default, the command waits for the restore to finish and reports its final status. With the `--nowait` option, it returns a task ID immediately; use the [nodetool tasks](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/tasks/index.md) commands to track progress or cancel the operation.

**Speeding up the restore**

A single `nodetool restore` invocation runs on one node, which downloads and streams all the listed SSTables. To parallelize the work, split the list of SSTables between the nodes and run `nodetool restore` on each of them. The `--scope` option (`node`, `rack`, `dc`, or `all`) constrains where each node streams the data, so that concurrent restores don’t stream the same partition to a replica more than once. See [nodetool restore](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/restore.md) for details on combining `--scope` with per-node SSTable lists.

With the `--primary-replica-only` option, each partition is streamed only to its primary replica. This reduces the amount of streamed data, but you **must** run a full cluster repair after the restore completes to replicate the data to the remaining replicas: for vnode-based keyspaces, run [nodetool repair -pr](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/repair.md) on **every** node; for tablet-based keyspaces, run [nodetool cluster repair](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/cluster/repair.md) on any single node.

<a id="restore-load-and-stream"></a>

## Restore with load and stream

Use this method when the backed-up SSTable files are available on disk (for example, snapshot files copied back from external storage). The SSTables are read and their contents are streamed to the nodes owning the data, so the method works regardless of cluster topology changes since the backup. Each SSTable needs to be uploaded to only **one** node, any node, and the cluster stays online.

#### NOTE
If the table has any [Materialized Views (MV)](https://docs.scylladb.com/manual/master/features/materialized-views.md) or [Secondary Indexes (SI)](https://docs.scylladb.com/manual/master/features/secondary-indexes.md), view updates are generated automatically as the base table data is streamed. Upload the base table SSTables only; uploading MV or SI SSTables is not supported and will fail.

**Procedure**

1. Complete the [prerequisites](#restore-prerequisites).
2. Copy the backed-up SSTable files of a table to that table’s `upload` directory on one of the nodes, and make sure the files are owned by the `scylla` user and group:
   ```shell
   sudo cp /path/to/backup/sstables/* /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000/upload/
   sudo chown -R scylla:scylla /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000/upload/
   ```

   You can distribute the backup files between several nodes to parallelize the restore; make sure each SSTable is uploaded to only one node.
3. Run [nodetool refresh](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/refresh.md) with the `--load-and-stream` option on each node holding uploaded files:
   ```shell
   nodetool refresh mykeyspace team_players --load-and-stream
   ```

   See [Load and Stream](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/refresh.md#nodetool-refresh-load-and-stream) for the `--scope` and `--primary-replica-only` options that constrain the set of target replicas. If `--primary-replica-only` is used, run a full cluster repair after the restore completes to replicate the data to the remaining replicas: for vnode-based keyspaces, run [nodetool repair -pr](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/repair.md) on **every** node; for tablet-based keyspaces, run [nodetool cluster repair](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/cluster/repair.md) on any single node.

<a id="restore-procedure"></a>

## Restore to an identical cluster

This method places the snapshot files directly back into the table directories and restarts the nodes.

#### NOTE
The following procedure assumes data is restored to the same cluster that was backed-up:

- same number of nodes
- same token range per node

The procedure restores each node using the backup file of the **same node**.
If this is not the case, use the [load and stream](#restore-load-and-stream) method described above instead. It works regardless of topology changes, but is slower than restoring to an identical cluster.

This method is suitable for vnode-based keyspaces only. For [tablet-based](https://docs.scylladb.com/manual/master/architecture/tablets.md) keyspaces, use the [object storage](#restore-object-storage) or [load and stream](#restore-load-and-stream) method instead.

Complete the [prerequisites](#restore-prerequisites) first.

#### NOTE
Best practise is **not** to restore [Materialized Views (MV)](https://docs.scylladb.com/manual/master/features/materialized-views.md) and [Secondary Indexes (SI)](https://docs.scylladb.com/manual/master/features/secondary-indexes.md) SSTables.
It is recommended to:

- Drop the MV and SI using DROP MATERIALIZED VIEW or DROP INDEX
- Restore the base table only (see below)
- Recreate the  MV or SI, using the original description from the CQL backup, using CREATE MATERIALIZED VIEW or CREATE INDEX

### Repeat the following steps for each node in the cluster:

1. Run the [nodetool drain](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/drain.md) command to ensure the data is flushed to the SSTables
2. Shut down the node

   Supported OS
   ```shell
   sudo systemctl stop scylla-server
   ```

   Docker
   ```shell
   docker exec -it some-scylla supervisorctl stop scylla
   ```

   (without stopping *some-scylla* container)
3. Delete all the files in the commitlog. Deleting the commitlog will prevent the newer insert from overriding the restored data.

   `sudo rm -rf /var/lib/scylla/commitlog/*`
4. Delete all the files in the keyspace_name_table. Note that by default the snapshots are created under ScyllaDB data directory `/var/lib/scylla/data/keyspace_name/table_name-UUID/`.

   Make sure NOT to delete the existing snapshots in the process.

   For example:
   ```shell
   sudo ll /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000

   -rw-r--r-- 1 scylla   scylla     66 Mar  5 09:19 nba-team_players-ka-1-CompressionInfo.db
   -rw-r--r-- 1 scylla   scylla    669 Mar  5 09:19 nba-team_players-ka-1-Data.db
   -rw-r--r-- 4 scylla   scylla     10 Mar  5 08:46 nba-team_players-ka-1-Digest.sha1
   -rw-r--r-- 1 scylla   scylla     24 Mar  5 09:19 nba-team_players-ka-1-Filter.db
   -rw-r--r-- 1 scylla   scylla    218 Mar  5 09:19 nba-team_players-ka-1-Index.db
   -rw-r--r-- 1 scylla   scylla     38 Mar  5 09:19 nba-team_players-ka-1-ScyllaDB.db
   -rw-r--r-- 1 scylla   scylla   4446 Mar  5 09:19 nba-team_players-ka-1-Statistics.db
   -rw-r--r-- 1 scylla   scylla     89 Mar  5 09:19 nba-team_players-ka-1-Summary.db
   -rw-r--r-- 4 scylla   scylla    101 Mar  5 08:46 nba-team_players-ka-1-TOC.txt
   drwx------ 5 scylla   scylla     69 Mar  6 08:14 snapshots
   drwx------ 2 scylla   scylla      6 Mar  5 08:40 upload

   sudo rm -f  /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000/*

   rm: cannot remove ‘/var/lib/scylla/data/nba/team_roster-c019f8108fda11e8b16a000000000001/snapshots’: Is a directory
   rm: cannot remove ‘/var/lib/scylla/data/nba/team_roster-c019f8108fda11e8b16a000000000001/upload’: Is a directory

   sudo ll /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000/

   drwx------ 5 scylla   scylla     69 Mar  6 08:14 snapshots
   drwx------ 2 scylla   scylla      6 Mar  5 08:40 upload
   ```
5. Select the snapshot you want to restore (usually the most recent one)
   ```shell
   /var/lib/scylla/data/keyspace_name/table_name-UUID/snapshots/<snapshot_name>
   ```

   For example:
   ```shell
   cd /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000/snapshots/1487847672222
   ```
6. Copy the snapshots directory content to the `/var/lib/scylla/data/keyspace_name/table_name-UUID/` directory

   For example:
   ```shell
   sudo cp -r * /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000
   ```

   #### WARNING
   Copying files into the table’s data directory is only allowed while the ScyllaDB service is **stopped**. To load SSTables into a running node, place them in the table’s `upload` directory and use [nodetool refresh](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/refresh.md) instead.
7. If you have incremental backup files, copy them from the **backups** folder `/var/lib/scylla/data/keyspace_name/table_name-UUID/backups` to  the `/var/lib/scylla/data/keyspace_name/table_name-UUID/` directory

   For example:
   ```shell
   sudo cp -r /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000/backups/* /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000
   ```
8. Make sure that all files are owned by the `scylla` user and group:
   ```shell
   sudo chown -R scylla:scylla /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000
   ```
9. Start the node

   Supported OS
   ```shell
   sudo systemctl start scylla-server
   ```

   Docker
   ```shell
   docker exec -it some-scylla supervisorctl start scylla
   ```

   (with *some-scylla* container already running)

After performing the above on all nodes, run a full cluster repair: for vnode-based keyspaces, run [nodetool repair -pr](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/repair.md) on **every** node; for tablet-based keyspaces, run [nodetool cluster repair](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/cluster/repair.md) on any single node; run both if you restored keyspaces of both kinds. This makes sure that the data is consistent on all nodes and between each node.
