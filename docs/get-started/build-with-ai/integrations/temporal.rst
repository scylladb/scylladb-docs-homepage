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
through a pluggable persistence layer. Temporal ships a generic **Cassandra**
persistence plugin, and because ScyllaDB is Cassandra-compatible, that plugin
works against a self-hosted ScyllaDB cluster or
`ScyllaDB Cloud <https://cloud.scylladb.com/>`_ without any custom code,
as long as you run the Temporal Server yourself.

.. note::

   There is ongoing work in the `Temporal project
   <https://github.com/temporalio/temporal/pulls?q=is%3Apr+is%3Aopen+scylladb>`_ to strengthen native
   ScyllaDB support. This page documents the integration as it works
   today, via the stable generic Cassandra plugin.

Visibility requires Elasticsearch
----------------------------------

Temporal Server **removed the Cassandra/ScyllaDB Visibility store in
v1.24** (it was deprecated in v1.21). Visibility powers ``ListWorkflows``
queries and the Temporal Web UI's workflow list, so a ScyllaDB-only setup
can no longer serve them.

The supported way to run Temporal against ScyllaDB is a split backend:

* **Execution store** (Workflow/Activity/history state) → ScyllaDB, via the
  Cassandra persistence plugin.
* **Visibility store** → Elasticsearch.

This is a limitation of Temporal's persistence layer, not of ScyllaDB.

Prerequisites
-------------

* Docker Compose (for the quickstart below)
* A self-hosted ScyllaDB cluster or a `ScyllaDB Cloud <https://cloud.scylladb.com/>`_ cluster

Self-hosted ScyllaDB
---------------------

The following ``docker-compose.yml`` starts ScyllaDB, Elasticsearch, and the
official Temporal Server image configured to use the Cassandra plugin
against ScyllaDB:

.. code-block:: yaml

   services:
     scylladb:
       image: scylladb/scylla:2026.2
       command: >-
         --smp 1 --memory 1G --overprovisioned 1 --api-address 0.0.0.0
         --tablets-mode-for-new-keyspaces disabled
       ports:
         - "9042:9042"

     elasticsearch:
       image: elasticsearch:8.19.19
       environment:
         - discovery.type=single-node
         - xpack.security.enabled=false
         - ES_JAVA_OPTS=-Xms256m -Xmx256m
       ports:
         - "9200:9200"

     temporal:
       image: temporalio/auto-setup:1.29.7
       depends_on:
         - scylladb
         - elasticsearch
       environment:
         - DB=cassandra
         - CASSANDRA_SEEDS=scylladb
         - KEYSPACE=temporal
         - ENABLE_ES=true
         - ES_SEEDS=elasticsearch
         - ES_VERSION=v8
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

.. important::

   Temporal's schema tool creates its ``temporal`` keyspace with
   ``SimpleStrategy``, which is **incompatible with ScyllaDB tablets**. 
   Modern ScyllaDB enables tablets for new keyspaces by
   default, so the ScyllaDB container above is started with
   ``--tablets-mode-for-new-keyspaces disabled``.

On first startup, ``temporalio/auto-setup`` creates the ``temporal`` keyspace
in ScyllaDB and the ``temporal_visibility`` index in
Elasticsearch. Start the stack with:

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

.. code-block:: bash

   docker run -p 7233:7233 \
     -e DB=cassandra \
     -e CASSANDRA_SEEDS="node-0.your-cluster.datacenter.clusters.scylla.cloud,node-1.your-cluster.datacenter.clusters.scylla.cloud,node-2.your-cluster.datacenter.clusters.scylla.cloud" \
     -e CASSANDRA_USER="<your-username>" \
     -e CASSANDRA_PASSWORD="<your-password>" \
     -e KEYSPACE=temporal \
     -e SKIP_SCHEMA_SETUP=true \
     -e ENABLE_ES=true \
     -e ES_SEEDS="<your-elasticsearch-host>" \
     -e ES_VERSION=v8 \
     temporalio/auto-setup:1.29.7

.. important::

   On ScyllaDB Cloud you
   must provide a keyspace that already has tablets disabled rather than let
   ``auto-setup`` create it. Pre-create it once from a CQL client:

   .. code-block:: sql

      CREATE KEYSPACE temporal
      WITH replication = {'class': 'NetworkTopologyStrategy', 'replication_factor': 3}
      AND tablets = {'enabled': false};

   Then load Temporal's schema into the keyspace yourself with the
   ``temporal-cassandra-tool`` (it ships inside the ``auto-setup`` image).
   Run ``setup-schema`` followed by ``update-schema``:

   .. code-block:: bash

      docker run --rm --entrypoint temporal-cassandra-tool \
        temporalio/auto-setup:1.29.7 \
        --endpoint node-0.your-cluster.datacenter.clusters.scylla.cloud \
        --user "<your-username>" --password "<your-password>" \
        --keyspace temporal --datacenter <your-datacenter> \
        --disable-initial-host-lookup \
        setup-schema -v 0.0

      docker run --rm --entrypoint temporal-cassandra-tool \
        temporalio/auto-setup:1.29.7 \
        --endpoint node-0.your-cluster.datacenter.clusters.scylla.cloud \
        --user "<your-username>" --password "<your-password>" \
        --keyspace temporal --datacenter <your-datacenter> \
        --disable-initial-host-lookup \
        update-schema -d /etc/temporal/schema/cassandra/temporal/versioned

    Finally start the
   server with ``SKIP_SCHEMA_SETUP=true`` (as shown in the ``docker run``
   above) so ``auto-setup`` does not try to recreate the keyspace.

.. note::

   The Cloud path still needs an Elasticsearch Visibility store. Point
   ``ES_SEEDS`` at your own Elasticsearch, or run one locally with the same
   ``elasticsearch`` service shown in the self-hosted Compose file above.


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
       WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
       AND tablets = {'enabled': false}
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

Limitations
-----------

* Visibility (``ListWorkflows``, the Web UI's workflow list) requires
  Elasticsearch; ScyllaDB cannot serve it, since Temporal Server dropped the
  Cassandra Visibility store in v1.24.
* Temporal's schema tool creates keyspaces with ``SimpleStrategy``, which is
  incompatible with ScyllaDB tablets. New keyspaces must have tablets disabled
  (``--tablets-mode-for-new-keyspaces disabled`` when self-hosting, or a
  pre-created keyspace with ``tablets = {'enabled': false}`` on ScyllaDB
  Cloud).
* Only the generic Cassandra persistence plugin is currently supported.
  There is no ScyllaDB-native persistence driver merged into
  ``temporalio/temporal`` yet.

Additional Resources
---------------------

* `ScyllaDB Cloud docs <https://cloud.docs.scylladb.com/stable/>`_
* `Temporal Server repository <https://github.com/temporalio/temporal>`_
* `Temporal documentation <https://docs.temporal.io/>`_
* `Temporal persistence configuration reference <https://docs.temporal.io/references/configuration>`_
