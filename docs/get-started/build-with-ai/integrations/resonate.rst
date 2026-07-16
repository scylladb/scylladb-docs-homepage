========
Resonate
========

.. image:: /_static/img/integrations/resonate-logo.png
   :alt: Resonate logo
   :width: 400px

`Resonate <https://resonatehq.io/>`_ is a durable agent execution engine that
makes long-running, failure-prone workflows reliable by persisting their
state as *durable promises*. Every function call resolves to a promise
written to the database before any work begins. If the process crashes,
a new worker reads the last open promise and resumes from exactly that
point.

`resonate-on-scylladb <https://github.com/resonatehq/resonate-on-scylladb>`_
is a Go implementation of the Resonate server protocol backed by ScyllaDB.
ScyllaDB stores all promise, task, and schedule state; the Resonate server
runs alongside your existing stack as a single binary.

.. note::

   The Resonate server always runs on your own infrastructure. ScyllaDB
   (self-hosted or ScyllaDB Cloud) is the durable storage backend it
   connects to. You are not locked in to a hosted workflow service.

Prerequisites
-------------

* Docker Compose
* Python 3.12+ (for the verification example)

.. _resonate-self-hosted:

Self-hosted ScyllaDB
--------------------

The ``resonate-on-scylladb`` repository ships a ``docker-compose.yaml``
that starts ScyllaDB and the Resonate server together. The ScyllaDB schema
is applied automatically on first startup.

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/resonatehq/resonate-on-scylladb.git
   cd resonate-on-scylladb

2. Start ScyllaDB and the Resonate server:

.. code-block:: bash

   docker compose --profile server up

The Resonate server is now listening on ``http://localhost:8001`` and
ScyllaDB is available on ``localhost:9042``.

.. note::

   The default ``docker-compose.yaml`` starts the server with ``--debug``
   enabled, which recreates the ScyllaDB keyspace on every server restart.
   This is convenient for local development but means durable promises are
   lost when the server container restarts. To disable this behavior, remove
   ``--debug`` from the server's ``command`` in ``docker-compose.yaml``
   before running.

.. _resonate-scylladb-cloud:

ScyllaDB Cloud
--------------

When using ScyllaDB Cloud as the backend, run the Resonate server on your
own infrastructure and point it at your ScyllaDB Cloud cluster. The Resonate 
server is **not** hosted in ScyllaDB Cloud, only the durable storage is.

1. Clone the repository and build the server image:

.. code-block:: bash

   git clone https://github.com/resonatehq/resonate-on-scylladb.git
   cd resonate-on-scylladb
   docker build --target server -t resonate-server .

2. Configure and start the server.

Find your contact points and credentials on the **Connect** tab of your
cluster in the `ScyllaDB Cloud Console <https://cloud.scylladb.com/>`_, then
run:

.. code-block:: bash

   docker run -p 8001:8001 \
     -e SCYLLADB_HOSTS="node-0.your-cluster.datacenter.clusters.scylla.cloud,node-1.your-cluster.datacenter.clusters.scylla.cloud,node-2.your-cluster.datacenter.clusters.scylla.cloud" \
     -e SCYLLADB_USERNAME="<your-username>" \
     -e SCYLLADB_PASSWORD="<your-password>" \
     -e SCYLLADB_KEYSPACE="resonate" \
     resonate-server serve

.. warning::

   Do not pass ``--debug`` to the server when connecting to a production
   ScyllaDB Cloud cluster. Debug mode recreates the keyspace on every server
   restart, deleting all durable promises.

Verify with the Python SDK
--------------------------

With the server running (either self-hosted or Cloud-backed), install the
Resonate Python SDK:

.. code-block:: bash

   pip install resonate-sdk

Write a minimal durable workflow (``hello.py``):

.. code-block:: python

   import asyncio
   from resonate.context import Context
   from resonate.resonate import Resonate


   async def greet(ctx: Context, name: str) -> str:
       return f"Hello, {name}!"


   async def main() -> None:
       resonate = Resonate(url="http://localhost:8001")
       resonate.register(greet)
       try:
           handle = resonate.run("greet.1", greet, "ScyllaDB")
           result = await handle.result()
           print(result)   # Hello, ScyllaDB!
       finally:
           await resonate.stop()


   if __name__ == "__main__":
       asyncio.run(main())

Run the worker:

.. code-block:: bash

   python hello.py

Expected output:

.. code-block:: text

   Hello, ScyllaDB!

.. note::

   The first run may take up to a minute while ScyllaDB initializes the
   schema and the server processes the task. Subsequent runs with the same
   promise ID return immediately from the database.

The durable promise for ``greet.1`` is now persisted in ScyllaDB. Kill and
restart the worker with the same script, the result is served from the
database and the function is not executed again.

Additional Resources
--------------------

* `resonate-on-scylladb repository <https://github.com/resonatehq/resonate-on-scylladb>`_
* `Resonate documentation <https://docs.resonatehq.io/>`_
* `Resonate Python SDK <https://github.com/resonatehq/resonate-sdk-py>`_
* `Resonate TypeScript SDK <https://github.com/resonatehq/resonate-sdk-ts>`_