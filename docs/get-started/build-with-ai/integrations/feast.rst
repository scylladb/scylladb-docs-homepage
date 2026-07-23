=======
Feast
=======

.. image:: /_static/img/integrations/feast-logo.png
   :alt: Feast logo
   :width: 400px

`Feast <https://feast.dev/>`_ is an open source feature store framework that 
manages and serves machine learning features for training and inference. 
The ScyllaDB integration provides a Feast online store for low-latency, 
distributed, real-time feature serving, with built-in support for vector search. 
It materializes feature values into a self-hosted ScyllaDB cluster or 
`ScyllaDB Cloud <https://cloud.scylladb.com/>`_.

ScyllaDB is used as an online store only. Feast still requires a separate
offline store for historical feature retrieval.
The ScyllaDB integration does not implement an offline store.

Installation
----------------

Install Feast with the ``scylladb`` extra, which pulls in ``scylla-driver``
automatically:

.. code-block:: bash

   pip install feast[scylladb]

Configuration
----------------

Configure ScyllaDB as the online store in your ``feature_store.yaml``. Set
``online_store.type`` to ``scylladb`` and provide the connection details for
your cluster.

Self-hosted ScyllaDB:

.. code-block:: yaml

   project: scylla_feature_repo
   registry: data/registry.db
   provider: local
   online_store:
     type: scylladb
     hosts:
       - 172.17.0.2
     keyspace: feast
     username: scylla
     password: password

ScyllaDB Cloud:

When connecting to ScyllaDB Cloud, set ``local_dc`` to the datacenter name shown
on the **Connect** tab of your cluster in the
`ScyllaDB Cloud Console <https://cloud.scylladb.com/>`_.

.. code-block:: yaml

   project: scylla_feature_repo
   registry: data/registry.db
   provider: local
   online_store:
     type: scylladb
     hosts:
       - node-0.aws_us_east_1.xxxxxxxx.clusters.scylla.cloud
       - node-1.aws_us_east_1.xxxxxxxx.clusters.scylla.cloud
       - node-2.aws_us_east_1.xxxxxxxx.clusters.scylla.cloud
     keyspace: feast
     username: scylla
     password: xxxxxx
     local_dc: AWS_US_EAST_1

Configuration Options
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 15 15 45
   :header-rows: 1

   * - Parameter
     - Type
     - Default
     - Description
   * - ``hosts``
     - list[str]
     - *(required)*
     - Contact-point host addresses.
   * - ``port``
     - int
     - ``9042``
     - CQL port.
   * - ``keyspace``
     - str
     - ``feast_keyspace``
     - Target ScyllaDB keyspace.
   * - ``username``
     - str
     - ``None``
     - Auth username.
   * - ``password``
     - str
     - ``None``
     - Auth password.
   * - ``local_dc``
     - str
     - ``None``
     - Local datacenter name for DC-aware load balancing.
   * - ``request_timeout``
     - float
     - ``None``
     - Driver request timeout in seconds.
   * - ``read_concurrency``
     - int
     - ``100``
     - ``concurrency`` argument passed to the driver's
       ``execute_concurrent_with_args`` for reads. Controls how many CQL
       statements are in-flight at once.
   * - ``write_concurrency``
     - int
     - ``100``
     - ``concurrency`` argument passed to the driver's
       ``execute_concurrent_with_args`` for writes. Controls how many CQL
       statements are in-flight at once.
   * - ``vector_similarity_function``
     - str
     - ``COSINE``
     - Default similarity function for vector indexes. Supported: ``COSINE``,
       ``DOT_PRODUCT``, ``EUCLIDEAN``. Can be overridden per-feature via the
       ``similarity_function`` Field tag.

Vector Search
----------------

ScyllaDB Cloud supports approximate nearest-neighbour (ANN) vector search. To
enable it for a feature view, tag the embedding ``Field`` with
``vector_index=true`` and specify the number of dimensions:

.. code-block:: python

   from feast import FeatureView, Field
   from feast.types import Array, Float32, String

   documents_fv = FeatureView(
       name="documents",
       entities=[item],
       schema=[
           Field(name="text", dtype=String),
           Field(
               name="embedding",
               dtype=Array(Float32),
               tags={
                   "vector_index": "true",
                   "dimensions": "768",
                   "similarity_function": "COSINE",  # COSINE | DOT_PRODUCT | EUCLIDEAN
               },
           ),
       ],
       online=True,
       source=push_source,
   )

When ``feast apply`` runs, it automatically creates the necessary tables
and ANN index for any feature view with vector-tagged fields.

To query the top-k most similar documents:

.. code-block:: python

   result = store.retrieve_online_documents_v2(
       features=["documents:text", "documents:embedding"],
       query=[0.1, 0.2, ...],   # your query embedding
       top_k=10,
       distance_metric="COSINE",
   )

The ``distance_metric`` accepts the following values:

* ``COSINE``: cosine similarity.
* ``DOT_PRODUCT``: dot-product (inner-product) similarity.
* ``EUCLIDEAN``: Euclidean (L2) distance.

Additional Resources
-----------------------

* `Feast ScyllaDB online store reference <https://docs.feast.dev/master/reference/online-stores/scylladb>`_
* `Feast website <https://feast.dev/>`_
* `Example projects <https://feature-store.scylladb.com/>`_
* `Turbocharge your Feature Store with ScyllaDB <https://www.scylladb.com/solution/feature-store/>`_
