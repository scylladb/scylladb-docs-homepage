# Launch ScyllaDB 2026.3 on GCP

This article will guide you through self-managed ScyllaDB deployment on GCP. For a fully-managed deployment of ScyllaDB
as-a-service, see [ScyllaDB Cloud documentation](https://cloud.docs.scylladb.com/).

## Prerequisites

* Active GCP account
* [Google SDK](https://cloud.google.com/sdk/docs/install), which includes the `gcloud` command-line tool
* ScyllaDB Image requires at least 2 vCPU servers.

## Launching ScyllaDB on GCP

1. Choose an instance type. See [Cloud Instance Recommendations for GCP](https://docs.scylladb.com/manual/master/getting-started/cloud-instance-recommendations.md#system-requirements-gcp) for the list of recommended instances.

   Other instance types will work, but with lesser performance. If you choose an instance type other than the recommended ones, make sure to run the [scylla_setup](https://docs.scylladb.com/manual/master/getting-started/system-configuration.md#system-configuration-scripts) script.
2. See the following table to obtain image information for the latest patch release.
   For earlier releases, see [GCP Images](https://docs.scylladb.com/manual/master/reference/gcp-images.md)
   <!-- -*- mode: rst -*- -->

   ### 2026.3.0

   | Image Name        |            Image ID |
   |-------------------|---------------------|
   | scylladb-2026-3-0 | 9021025706677946776 |
3. Launch a ScyllaDB instance on GCP with `gcloud` using the information from the previous step. Use the following syntax:
   ```console
   gcloud compute instances create <name of new instance> --image <ScyllaDB image name> --image-project < ScyllaDB project name> --local-ssd interface=nvme --zone=<GCP zone - optional> --machine-type=<machine type>
   ```

   For example:
   ```console
   gcloud compute instances create scylla-node1 --image scylladb-2026-1-11 --image-project scylla-images --local-ssd interface=nvme --machine-type=n1-highmem-8
   ```

   To add more storage to the VM, add multiple `--local-ssd interface=nvme` options to the command. For example, the following
   command will launch a VM with 4 SSD, and 1.5TB of data (4 \* [375 GB](https://cloud.google.com/compute/docs/disks/local-ssd)):
   ```console
   gcloud compute instances create scylla-node1 --image scylladb-2026-1-11 --image-project scylla-images --local-ssd interface=nvme --local-ssd interface=nvme --local-ssd interface=nvme --local-ssd interface=nvme --machine-type=n1-highmem-8
   ```

   For more information about GCP image create see the [Google Cloud SDK documentation](https://cloud.google.com/sdk/gcloud/reference/compute/images/create).

   To customize the ScyllaDB configuration at launch (cluster name, seeds, networking, and more),
   pass cloud-init user data as described in
   [Configuring ScyllaDB with User Data](#launch-on-gcp-user-data).
4. (Optional) Configure firewall rules.

   Ensure that all [ScyllaDB ports](https://docs.scylladb.com/manual/master/operating-scylla/security/security-checklist.md#networking-ports) are open.
5. Connect to the servers:
   > > ```console
   > > gcloud compute ssh <name of the created instance>
   > > ```

   > For example:
   > > ```console
   > > gcloud compute ssh scylla-node1
   > > ```

   To check that the ScyllaDB server is running, run:
   > ```console
   > nodetool status
   > ```

<a id="launch-on-gcp-user-data"></a>

## Configuring ScyllaDB with User Data

You can customize the ScyllaDB configuration at launch time by passing cloud-init
user data to the instance. On GCP, user data is provided through the instance
`user-data` metadata key, for example with `--metadata-from-file`
(replace the image name and machine type with your actual version and instance):

```console
gcloud compute instances create scylla-node1 --image scylladb-2026-1-11 --image-project scylla-images \
    --local-ssd interface=nvme --machine-type=n2-standard-8 \
    --metadata-from-file user-data=./user-data.yaml
```

The user data is a JSON or YAML document. The most commonly used options are:

| Option                              | Type    | Default     | Description                                                                                                                                                                                                                                                                                                                                        |
|-------------------------------------|---------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `scylla_yaml`                       | object  | `{}`        | Settings passed directly to `scylla.yaml` (for example `cluster_name` and `seed_provider`). See [scylla.yaml](https://docs.scylladb.com/manual/master/operating-scylla/admin.md#admin-scylla-yaml).                                                                                                                                                |
| `developer_mode`                    | boolean | `false`     | Enable developer mode (relaxes production checks; not recommended for production).                                                                                                                                                                                                                                                                 |
| `post_configuration_script`         | string  | `""`        | A bash script (optionally base64-encoded) executed after ScyllaDB configuration completes.                                                                                                                                                                                                                                                         |
| `post_configuration_script_timeout` | integer | `600`       | Timeout, in seconds, for `post_configuration_script`.                                                                                                                                                                                                                                                                                              |
| `start_scylla_on_first_boot`        | boolean | `true`      | Start `scylla-server` automatically on the first boot.                                                                                                                                                                                                                                                                                             |
| `tier1_networking`                  | boolean | auto-detect | **GCP only.** Override the network bandwidth tier ScyllaDB assumes when tuning streaming throughput. When omitted, it is auto-detected. Only has an effect on machine types that support Tier 1 networking (N2/N2D with 48 or more vCPUs, and Z3); it is ignored on all other types. See [GCP Tier 1 networking](#launch-on-gcp-tier1-networking). |
| `device_wait_seconds`               | integer | `0`         | Maximum number of seconds to wait for storage devices to appear before configuring them (`300` is recommended).                                                                                                                                                                                                                                    |

For the full list of supported user-data options, see the
[ScyllaDB Machine Image documentation](https://github.com/scylladb/scylla-machine-image).

Example `user-data.yaml`:

```yaml
scylla_yaml:
  cluster_name: my-cluster
  seed_provider:
    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
      parameters:
        - seeds: 10.0.1.1,10.0.1.2
start_scylla_on_first_boot: true
device_wait_seconds: 300
```

<a id="launch-on-gcp-tier1-networking"></a>

### GCP Tier 1 networking

[Tier 1 networking](https://cloud.google.com/compute/docs/networking/configure-vm-with-high-bandwidth-configuration)
provides higher egress bandwidth on supported GCP machine types — up to 100 Gbps
on N2 and N2D instances with 48 or more vCPUs, and up to 200 Gbps on Z3 instances.
ScyllaDB uses the assumed network bandwidth to tune streaming throughput
(`stream_io_throughput_mb_per_sec`), so it needs to know whether the instance
runs with Tier 1 bandwidth.

By default ScyllaDB detects this automatically, in the following order of precedence:

1. The `tier1_networking` user-data option (`true` / `false`), when set.
2. The `scylla_tier1_networking` instance metadata attribute, when set at VM creation time.
3. The NIC link speed reported by the kernel (`/sys/class/net/<iface>/speed`).
4. The Compute Engine API, as a last resort: ScyllaDB reads
   `networkPerformanceConfig.totalEgressBandwidthTier` from the instance
   resource. This query requires the `compute.readonly` scope on the VM
   service account; without it the check is skipped and the default bandwidth
   is assumed.

The first three checks require no additional GCP API permissions and work out of
the box. Set `tier1_networking` explicitly only when you want to override the
detected value — for example, to assume Tier 1 bandwidth on an instance where
detection is not reliable:

```yaml
tier1_networking: true
```

The override applies only to machine types that support Tier 1 networking. On any
other type — such as the `n2-standard-8` instance used in the examples above —
`tier1_networking` is ignored and the default bandwidth is used.

#### NOTE
The `tier1_networking` option only controls the bandwidth ScyllaDB *assumes*
when tuning itself. To actually obtain Tier 1 bandwidth, the instance must be
created with Tier 1 networking enabled — a supported machine type, a gVNIC
network interface, and
`--network-performance-configs=total-egress-bandwidth-tier=TIER_1`. See the
[GCP high-bandwidth configuration documentation](https://cloud.google.com/compute/docs/networking/configure-vm-with-high-bandwidth-configuration).

## Next Steps

* [Configure ScyllaDB](https://docs.scylladb.com/manual/master/getting-started/system-configuration.md)
* Manage your clusters with [ScyllaDB Manager](https://manager.docs.scylladb.com/)
* Monitor your cluster and data with [ScyllaDB Monitoring](https://monitoring.docs.scylladb.com/)
* Get familiar with ScyllaDB’s [command line reference guide](https://docs.scylladb.com/manual/master/operating-scylla/nodetool.md).
