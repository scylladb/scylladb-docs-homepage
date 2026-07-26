# How to Switch Snitches

#### NOTE
Changing the network topology by switching to another type of snitch
is no longer supported. The new snitch must specify the same DC and rack
as the previous one.

This procedure describes the steps that need to be done when switching from one type of snitch to another.
Such a scenario can be when increasing the cluster and adding more data-centers in different locations.
Snitches are responsible for specifying how ScyllaDB distributes the replicas. The procedure is dependent on any changes in the cluster topology.

**Note** - Switching a snitch requires a full cluster shutdown, so It is highly recommended to choose the [right snitch](https://docs.scylladb.com/manual/master/operating-scylla/system-configuration/snitch.md) for your needs at the cluster setup phase.

For example:

Original cluster: three nodes cluster on a single data-center with [Simplesnitch](https://docs.scylladb.com/manual/master/operating-scylla/system-configuration/snitch.md#snitch-simple-snitch) or [Ec2snitch](https://docs.scylladb.com/manual/master/operating-scylla/system-configuration/snitch.md#snitch-ec2-snitch).

Change to: three nodes in one data-center and one rack using a [GossipingPropertyFileSnitch](https://docs.scylladb.com/manual/master/operating-scylla/system-configuration/snitch.md#snitch-gossiping-property-file-snitch) or [Ec2multiregionsnitch](https://docs.scylladb.com/manual/master/operating-scylla/system-configuration/snitch.md#snitch-ec2-multi-region-snitch).

## Procedure

1. Stop all the nodes in the cluster.

Supported OS

```shell
sudo systemctl stop scylla-server
```

Docker

```shell
docker exec -it some-scylla supervisorctl stop scylla
```

(without stopping *some-scylla* container)

1. In the `scylla.yaml` file edit the endpoint_snitch. The file can be found under `/etc/scylla/`. Change the endpoint_snitch to all the nodes in the cluster.

For example:

`endpoint_snitch: GossipingPropertyFileSnitch`

1. In the `cassandra-rackdc.properties` file edit the rack and data-center information.

For example, `Ec2MultiRegionSnitch`:

A node in the `us-east-1` region, us-east is the data center name, and 1 is the rack location.

1. Start all the nodes in the cluster in parallel.

Supported OS

```shell
sudo systemctl start scylla-server
```

Docker

```shell
docker exec -it some-scylla supervisorctl start scylla
```

(with *some-scylla* container already running)

1. Run full repair (consult with the table above if this action is needed).
