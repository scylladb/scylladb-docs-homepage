=========================
Run ScyllaDB
=========================

ScyllaDB offers various deployment options, including Docker and ScyllaDB 
Cloud, making it flexible for different development scenarios.

* :ref:`Run ScyllaDB in Docker <create-database-docker>`
* :ref:`Deploy with ScyllaDB Cloud (SaaS) <create-database-scylladb-cloud>`
* :ref:`Self-deploy in the Cloud or On-premise <create-database-self-deploy>`


.. _create-database-docker:

Run ScyllaDB in Docker
---------------------------
Docker simplifies the deployment and management of ScyllaDB. By using Docker 
containers, you can easily create isolated ScyllaDB instances for development, 
testing, and production. Running ScyllaDB in Docker is the simplest way to 
experiment with ScyllaDB, and we highly recommend it.

If you intend to run ScyllaDB in Docker in production, we recommend using
`ScyllaDB Operator <https://operator.docs.scylladb.com/stable/>`_
which will help you manage ScyllaDB clusters within Kubernetes.

Running a Single Node
=======================

Execute the following command to run a node:

.. code:: sh

    docker run --name scylla -d scylladb/scylla


Docker will start a new container named "scylla" in detached mode using 
the ScyllaDB image, allowing it to run in the background.

It will take a minute or so on a decent internet connection to pull the image 
from Docker hub and start the container. Read on for more details on how to 
check your node logs and status.

Viewing Node Logs
========================

To view the running logs of your node, run the following command:

.. code::

    docker logs -f scylla


The output of this command will look similar to this:

.. code::
    :class: hide-copy-button

    INFO  2023-11-13 04:18:44,449 [shard  0] init - starting the view builder
    INFO  2023-11-13 04:18:44,455 [shard  0] init - starting native transport
    INFO  2023-11-13 04:18:44,456 [shard  0] cql_server_controller - Starting listening for CQL clients on 172.17.0.2:9042 (unencrypted, non-shard-aware)
    INFO  2023-11-13 04:18:44,456 [shard  0] cql_server_controller - Starting listening for CQL clients on 172.17.0.2:19042 (unencrypted, shard-aware)
    INFO  2023-11-13 04:18:44,457 [shard  0] init - serving
    INFO  2023-11-13 04:18:44,457 [shard  0] init - Scylla version 5.2.9-0.20230920.5709d0043978 initialization completed.

Node logs can be useful for troubleshooting and support.

Checking Node Status
======================

You can verify that the cluster is up and running with the following command:

.. code::

    docker exec -it scylla nodetool status

The output of this command will look similar to this:

.. code::
    :class: hide-copy-button

    Datacenter: datacenter1
    =======================
    Status=Up/Down
    |/ State=Normal/Leaving/Joining/Moving
    --  Address     Load       Tokens       Owns    Host ID                               Rack
    UN  172.17.0.2  632 KB     256          ?       8075882e-3b49-42a4-a742-4caf072844ff  rack1

The status "UN" stands for "Up and Normal". It indicates the node is in 
a healthy state and actively participating in the data distribution and 
replication processes.

Connecting to your Node
========================

You can connect to your node with ``cqlsh`` using the following command:

.. code::

     docker exec -it scylla cqlsh

The output of this command will look similar to this:

.. code::
    :class: hide-copy-button

    Connected to  at 172.17.0.2:9042.
    [cqlsh 5.0.1 | Cassandra 3.0.8 | CQL spec 3.3.1 | Native protocol v4]
    Use HELP for help.
    cqlsh>


.. _create-database-scylladb-cloud:

Deploy with ScyllaDB Cloud (SaaS) 
----------------------------------

ScyllaDB Cloud is a fully managed service where the ScyllaDB team handles 
deployment and maintenance of your ScyllaDB clusters. This service is ideal 
if you're seeking a cloud-based, ready-to-use ScyllaDB solution.

The easiest way to get started with ScyllaDB Cloud is to sign up for an 
`account <https://cloud.scylladb.com/account/sign-up>`_.

Follow the `Quick Start Guide to ScyllaDB Cloud <https://cloud.docs.scylladb.com/stable/scylladb-quickstart/>`_
to launch your cluster.

.. _create-database-self-deploy:

Self-deploy in the Cloud or On-premise
---------------------------------------------

You can install ScyllaDB on your Linux machine using a platform-agnostic installation
script we refer to as `ScyllaDB Web Installer for Linux <https://opensource.docs.scylladb.com/master/getting-started/installation-common/scylla-web-installer.html>`_.

Run the following command to install ScyllaDB:

.. code::

    curl -sSf get.scylladb.com/server | sudo bash

By default, running the script installs the latest official version of ScyllaDB Open Source. 

Alternatively, you can install ScyllaDB packages for your platform or launch 
ScyllaDB on AWS, GCP, or Azure. See the `download center <https://www.scylladb.com/download/>`_ 
for a full list of options.
