========
Temporal
========

.. image:: /_static/img/integrations/temporal-logo.png
   :alt: Temporal logo
   :width: 400px

`Temporal <https://github.com/temporalio/temporal>`_ is a durable execution
platform: it runs your application's Workflows and Activities in a way that
survives process crashes, network failures, and timeouts, automatically
retrying and resuming from the last completed step.

The Temporal Server persists all Workflow, Activity, and history state
through a pluggable persistence layer. 


Two back-end store elements
--------------------------------------------
Starting from Temporal `v1.24.0 release notes
<https://github.com/temporalio/temporal/releases/tag/v1.24.0>`_,  back-end is split into two elements:
* **Execution store** (Workflow/Activity/history state) 
* **Visibility store**

Scope of this page is the first, Execution store.
Prerequisites
-------------

* Docker Compose (for the quickstart below)
* A self-hosted ScyllaDB cluster or a `ScyllaDB Cloud <https://cloud.scylladb.com/>`_ cluster

Self-hosted ScyllaDB
---------------------

The following ``docker-compose.yml`` starts ScyllaDB, Elasticsearch, and the
official Temporal Server image configured to use the Cassandra plugin
against ScyllaDB.

Create a ``temporal-config`` directory next to your ``docker-compose.yml``
and fetch the upstream config template into it:

.. code-block:: bash

   mkdir -p temporal-config/config temporal-config/dynamicconfig
   curl -sL -o temporal-config/config/docker.yaml \
     https://raw.githubusercontent.com/temporalio/temporal/v1.31.2/config/docker.yaml
   touch temporal-config/dynamicconfig/docker.yaml

The first command downloads the base server config template that the
``temporal`` container renders at startup. The second creates an empty
dynamic-config file — the template references it by default, and the file
just needs to exist; you can add `dynamic config settings
<https://docs.temporal.io/references/dynamic-configuration>`_ to it later.

.. code-block:: yaml

   services:
     scylladb:
       image: scylladb/scylla:2026.3
       command: >-
         --smp 1 --memory 1G --overprovisioned 1 --api-address 0.0.0.0
       ports:
         - "9042:9042"
       healthcheck:
         test: ["CMD-SHELL", "cqlsh -e 'describe keyspaces'"]
         interval: 5s
         timeout: 5s
         retries: 60
         start_period: 30s

     elasticsearch:
       image: elasticsearch:8.19.19
       environment:
         - discovery.type=single-node
         - xpack.security.enabled=false
         - ES_JAVA_OPTS=-Xms256m -Xmx256m
       ports:
         - "9200:9200"
       healthcheck:
         test: ["CMD-SHELL", "curl -sf 'http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=1s' || exit 1"]
         interval: 5s
         timeout: 5s
         retries: 60
         start_period: 30s

     temporal-admin-tools:
       image: temporalio/admin-tools:1.31.2
       depends_on:
         scylladb:
           condition: service_healthy
         elasticsearch:
           condition: service_healthy
       environment:
         - CASSANDRA_SEEDS=scylladb
         - ES_HOST=elasticsearch
         - ES_PORT=9200
         - ES_SCHEME=http
         - ES_VERSION=v8
         - ES_VISIBILITY_INDEX=temporal_visibility_v1_dev
       entrypoint: ["/bin/sh", "-c"]
       command: >
         "temporal-cassandra-tool --ep scylladb create -k temporal --rf 1 --datacenter datacenter1 &&
          temporal-cassandra-tool --ep scylladb -k temporal setup-schema -v 0.0 &&
          temporal-cassandra-tool --ep scylladb -k temporal update-schema -d /etc/temporal/schema/cassandra/temporal/versioned &&
          temporal-elasticsearch-tool --ep http://elasticsearch:9200 setup-schema &&
          temporal-elasticsearch-tool --ep http://elasticsearch:9200 create-index --index temporal_visibility_v1_dev"

     temporal:
       image: temporalio/server:1.31.2
       depends_on:
         temporal-admin-tools:
           condition: service_completed_successfully
       environment:
         - DB=cassandra
         - CASSANDRA_SEEDS=scylladb
         - KEYSPACE=temporal
         - ENABLE_ES=true
         - ES_SEEDS=elasticsearch
         - ES_VERSION=v8
         - ES_VISIBILITY_INDEX=temporal_visibility_v1_dev
         - BIND_ON_IP=0.0.0.0
         - TEMPORAL_BROADCAST_ADDRESS=0.0.0.0
       volumes:
         - ./temporal-config/config/docker.yaml:/etc/temporal/config/docker.yaml:ro
         - ./temporal-config/dynamicconfig:/etc/temporal/config/dynamicconfig:ro
       entrypoint: ["temporal-server", "--root", "/etc/temporal", "--env", "docker", "start"]
       ports:
         - "7233:7233"

     temporal-ui:
       image: temporalio/ui:2.52.1
       depends_on:
         - temporal
       environment:
         - TEMPORAL_ADDRESS=temporal:7233
       ports:
         - "8080:8080"

.. note::

   By default, ``temporal-cassandra-tool create`` builds its ``temporal``
   keyspace with ``SimpleStrategy``, which isn't recommended for
   ScyllaDB. Passing ``--datacenter datacenter1`` (as in the
   ``command`` above) makes the tool use ``NetworkTopologyStrategy``
   instead.

On first startup, ``temporal-admin-tools`` creates the ``temporal`` keyspace
in ScyllaDB and the ``temporal_visibility_v1_dev`` index in Elasticsearch,
then exits; the ``temporal`` service only starts once that container
completes successfully. Start the stack with:

.. code-block:: bash

   docker compose up -d

Temporal is now listening on ``localhost:7233``, and the Web UI is at
<http://localhost:8080>.

ScyllaDB Cloud
--------------

When using ScyllaDB Cloud as the execution store, run the Temporal Server
on your own infrastructure and point it at your cluster's contact points.
Find them on the **Connect** tab of your cluster in the
`ScyllaDB Cloud Console <https://cloud.scylladb.com/>`_.

As with the self-hosted setup, ``temporalio/server`` needs a rendered
config mounted into the container. Fetch the same upstream template:

.. code-block:: bash

   mkdir -p temporal-config/config temporal-config/dynamicconfig
   curl -sL -o temporal-config/config/docker.yaml \
     https://raw.githubusercontent.com/temporalio/temporal/v1.31.2/config/docker.yaml
   touch temporal-config/dynamicconfig/docker.yaml

Before starting ``temporal-server``, you still need to create the
keyspace and stand up Elasticsearch, covered next.

Creating the keyspace
~~~~~~~~~~~~~~~~~~~~~

On ScyllaDB Cloud you must provide the keyspace yourself rather than let
Temporal create it. Pre-create it once from a CQL client (for example
`cqlsh <https://github.com/scylladb/scylla-cqlsh>`_):

.. code-block:: bash

   docker run --rm -it scylladb/scylla-cqlsh \
     node-0.your-cluster.datacenter.clusters.scylla.cloud 9042 \
     -u "<your-username>" -p "<your-password>"

.. code-block:: text

   CREATE KEYSPACE temporal
   WITH replication = {'class': 'NetworkTopologyStrategy', 'replication_factor': 3};

Then load Temporal's schema into the keyspace yourself with the
``temporal-cassandra-tool`` (it ships inside the ``temporalio/admin-tools``
image). Run ``setup-schema`` followed by ``update-schema``:

.. code-block:: bash

   docker run --rm --entrypoint temporal-cassandra-tool \
     temporalio/admin-tools:1.31.2 \
     --endpoint node-0.your-cluster.datacenter.clusters.scylla.cloud \
     --user "<your-username>" --password "<your-password>" \
     --keyspace temporal --datacenter <your-datacenter> \
     --disable-initial-host-lookup \
     setup-schema -v 0.0

   docker run --rm --entrypoint temporal-cassandra-tool \
     temporalio/admin-tools:1.31.2 \
     --endpoint node-0.your-cluster.datacenter.clusters.scylla.cloud \
     --user "<your-username>" --password "<your-password>" \
     --keyspace temporal --datacenter <your-datacenter> \
     --disable-initial-host-lookup \
     update-schema -d /etc/temporal/schema/cassandra/temporal/versioned

Creating the Elasticsearch visibility index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start Elasticsearch:

.. code-block:: bash

   docker run -d --name elasticsearch -p 9200:9200 \
     -e discovery.type=single-node \
     -e xpack.security.enabled=false \
     -e ES_JAVA_OPTS="-Xms256m -Xmx256m" \
     elasticsearch:8.19.19

Then, before starting ``temporal-server``, load Temporal's index template
into it:

.. code-block:: bash

   docker run --rm --entrypoint temporal-elasticsearch-tool \
     temporalio/admin-tools:1.31.2 \
     --ep http://host.docker.internal:9200 \
     setup-schema

   docker run --rm --entrypoint temporal-elasticsearch-tool \
     temporalio/admin-tools:1.31.2 \
     --ep http://host.docker.internal:9200 \
     create-index --index temporal_visibility_v1_dev

Starting the server
~~~~~~~~~~~~~~~~~~~~

With the keyspace and Elasticsearch index in place, start
``temporal-server``, setting ``ES_SEEDS`` to the Elasticsearch instance
you just created:

.. code-block:: bash

   docker run -p 7233:7233 \
     -e DB=cassandra \
     -e CASSANDRA_SEEDS="node-0.your-cluster.datacenter.clusters.scylla.cloud,node-1.your-cluster.datacenter.clusters.scylla.cloud,node-2.your-cluster.datacenter.clusters.scylla.cloud" \
     -e CASSANDRA_USER="<your-username>" \
     -e CASSANDRA_PASSWORD="<your-password>" \
     -e KEYSPACE=temporal \
     -e ENABLE_ES=true \
     -e ES_SEEDS=host.docker.internal \
     -e ES_VERSION=v8 \
     -e BIND_ON_IP=0.0.0.0 \
     -e TEMPORAL_BROADCAST_ADDRESS=0.0.0.0 \
     -v "$(pwd)/temporal-config/config/docker.yaml:/etc/temporal/config/docker.yaml:ro" \
     -v "$(pwd)/temporal-config/dynamicconfig:/etc/temporal/config/dynamicconfig:ro" \
     --entrypoint temporal-server \
     temporalio/server:1.31.2 \
     --root /etc/temporal --env docker start


Application data alongside Temporal
------------------------------------

Temporal's own ``temporal`` keyspace (Workflow/Activity/history state) and
your application's business-data keyspace can live on the **same ScyllaDB
cluster** as long as they use separate keyspaces. A worker process can use
the `scylla-driver <https://github.com/scylladb/python-driver>`_ (a
drop-in-compatible fork of ``cassandra-driver``) to read/write its own
tables from Activities, independent of Temporal's persistence.

Create the application keyspace and table once, before your Activities
start using them:

.. code-block:: python

   import os
   from cassandra.cluster import Cluster

   cluster = Cluster(os.environ["SCYLLA_HOSTS"].split(","))
   session = cluster.connect()

   session.execute(
       """
       CREATE KEYSPACE IF NOT EXISTS orders_app
       WITH replication = {'class': 'NetworkTopologyStrategy', 'replication_factor': 1}
       """
   )
   session.set_keyspace("orders_app")
   session.execute(
       """
       CREATE TABLE IF NOT EXISTS orders (
           order_id text PRIMARY KEY,
           status text
       )
       """
   )

Then read/write from your Activities as usual:

.. code-block:: python

   session.execute(
       "INSERT INTO orders (order_id, status) VALUES (%s, %s)",
       (order_id, "received"),
   )

This keeps application state fully separate from Temporal's internal
schema while sharing the same cluster.

Additional Resources
---------------------

* `ScyllaDB Cloud docs <https://cloud.docs.scylladb.com/stable/>`_
* `Temporal Server repository <https://github.com/temporalio/temporal>`_
* `Temporal documentation <https://docs.temporal.io/>`_
* `Temporal persistence configuration reference <https://docs.temporal.io/references/configuration>`_
* `Building High Availability for Temporal Workflows — ShareChat Engineering
  <https://sharechat.com/blogs/engineering/Building%20High%20Availability%20for%20Temporal%20Workflows>`_

