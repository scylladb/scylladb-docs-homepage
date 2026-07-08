======================================
LangGraph
======================================

`LangGraph <https://github.com/langchain-ai/langgraph>`_ is a framework for
building AI agents and multi-agent workflows. The ScyllaDB LangGraph integration
provides a checkpointer that persists agent state in ScyllaDB, enabling
short-term memory, human-in-the-loop patterns, time travel, and fault tolerance.

Checkpointer
----------------------------------

The ``ScyllaDBSaver`` checkpointer implements the LangGraph
``CheckpointSaver`` interface on top of ScyllaDB. It persists the full state of
your LangGraph graph after every step, so agents can resume interrupted runs and
support multi-turn conversations across sessions.

Installation
~~~~~~~~~~~~~~

.. code-block:: bash

   pip install langgraph-checkpoint-scylladb

Usage
~~~~~~~

Synchronous
""""""""""""

Create a new session for ``ScyllaDBSaver``:

.. code-block:: python

   from cassandra.auth import PlainTextAuthProvider
   from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
   from cassandra.policies import DCAwareRoundRobinPolicy
   from langgraph.checkpoint.scylladb import ScyllaDBSaver

   profile = ExecutionProfile(
       load_balancing_policy=DCAwareRoundRobinPolicy(local_dc="AWS_US_EAST_1"),
   )
   cluster = Cluster(
       contact_points=["node-0.example.scylla.cloud"],
       port=9042,
       auth_provider=PlainTextAuthProvider("scylla", "secret"),
       execution_profiles={EXEC_PROFILE_DEFAULT: profile},
   )
   session = cluster.connect()

   checkpointer = ScyllaDBSaver(session, keyspace="langgraph")
   checkpointer.setup()

   app = graph.compile(checkpointer=checkpointer)

   write_config = {"configurable": {"thread_id": "1", "checkpoint_ns": ""}}
   read_config  = {"configurable": {"thread_id": "1"}}

   checkpointer.put(write_config, {...}, {}, {})
   checkpointer.get(read_config)
   list(checkpointer.list(read_config))

.. note::

   Call ``checkpointer.setup()`` once to create the required tables in the
   target keyspace before using the checkpointer.

Asynchronous (``from_conn_string``)
""""""""""""""""""""""""""""""""""""

Use the async context manager with a connection string:

.. code-block:: python

   from langgraph.checkpoint.scylladb import ScyllaDBSaver

   SCYLLADB_URI = (
       "scylladb://scylla:secret@node-0.example.scylla.cloud:9042"
       "/langgraph?dc=AWS_US_EAST_1"
   )

   async with ScyllaDBSaver.from_conn_string(SCYLLADB_URI) as checkpointer:
       await checkpointer.aput(write_config, {...}, {}, {})
       await checkpointer.aget(read_config)
       [c async for c in checkpointer.alist(read_config)]

The connection string format is:

.. code-block:: text

   scylladb://<user>:<password>@<host>:<port>/<keyspace>?dc=<datacenter>

The ``dc`` query parameter is required for ScyllaDB Cloud connections.

TTL
""""

Checkpoints can be automatically expired by passing a ``ttl`` value in seconds:

.. code-block:: python

   checkpointer = ScyllaDBSaver(session, keyspace="langgraph", ttl=3600) # seconds

   # or via from_conn_string
   async with ScyllaDBSaver.from_conn_string(SCYLLADB_URI, ttl=3600) as checkpointer:
       ...

Schema
~~~~~~~

``checkpointer.setup()`` creates two tables in the target keyspace:

.. list-table::
   :widths: 30 35 35
   :header-rows: 1

   * - Table
     - Partition key
     - Clustering key
   * - ``checkpoints``
     - ``thread_id``
     - ``checkpoint_ns ASC``, ``checkpoint_id DESC``
   * - ``checkpoint_writes``
     - ``(thread_id, checkpoint_ns, checkpoint_id)``
     - ``task_id``, ``idx``

Every access pattern uses a full partition key, so no ``ALLOW FILTERING`` is
needed.

Additional Resources
-----------------------

* `langgraph-checkpoint-scylladb repository <https://github.com/scylladb/langchain-scylladb/tree/main/libs/langgraph-checkpoint-scylladb>`_
* `LangGraph persistence documentation <https://langchain-ai.github.io/langgraph/concepts/persistence/>`_
* `ScyllaDB Cloud <https://cloud.scylladb.com/>`_
* `ScyllaDB documentation <https://docs.scylladb.com/>`_
