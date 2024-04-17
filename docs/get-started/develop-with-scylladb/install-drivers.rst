===========================
Install a Driver
===========================

To interact with ScyllaDB, you need to install the appropriate drivers for 
your programming language. These drivers facilitate communication between 
the application and the ScyllaDB database, enabling data manipulation and 
retrieval.

.. tabs::

  .. group-tab:: Rust
    
    Rust developers can use specialized drivers that provide asynchronous, 
    non-blocking access to ScyllaDB. These drivers are designed to leverage 
    Rust's performance and safety features, ensuring efficient and secure 
    database operations.

    The installation typically involves adding the driver as a dependency in your 
    ``Cargo.toml`` file and configuring it to connect to your ScyllaDB instance.

    Run the following Cargo command in the project directory:

    .. code::

        cargo add scylla

    Or add the relevant version to your ``Cargo.toml`` following instructions on
    `crates.io <https://crates.io/>`_.

    * See the `Rust Driver documentation <https://rust-driver.docs.scylladb.com/>`_ for details.
    * Learn how to use the Rust Driver on `ScyllaDB University <https://university.scylladb.com/courses/using-scylla-drivers/lessons/rust-and-scylla-2/>`_.

  .. group-tab:: Python
    
    For Python developers, ScyllaDB has forked the Python client driver for CQL, 
    adding enhanced capabilities that take advantage of ScyllaDB’s architecture.

    ``pip`` is the suggested tool for installing packages. It will install the Python
    driver and all required Python dependencies. Run the following command:

    .. code::

        pip install scylla-driver

    * See the `Python Driver documentation <https://python-driver.docs.scylladb.com/>`_ for details.
    * `Learn how to use Python with ScyllaDB <https://university.scylladb.com/courses/using-scylla-drivers/lessons/coding-with-python/>`_ on ScyllaDB University.

  .. group-tab:: Java
    
    For Java developers, ScyllaDB has forked the Java client driver for CQL, 
    adding enhanced capabilities that take advantage of ScyllaDB’s architecture.

    Maven is the suggested tool for managing dependencies, and the driver 
    artifacts are published in Maven central, under the group id 
    `com.scylladb <http://search.maven.org/#search%7Cga%7C1%7Cg%3A%22com.scylladb%22>`_. 
    You should include the following dependencies:

    .. code:: xml

        <dependency>
          <groupId>com.scylladb</groupId>
          <artifactId>java-driver-core</artifactId>
          <version>${driver.version}</version>
        </dependency>

        <dependency>
          <groupId>com.scylladb</groupId>
          <artifactId>java-driver-query-builder</artifactId>
          <version>${driver.version}</version>
        </dependency>

        <dependency>
          <groupId>com.scylladb</groupId>
          <artifactId>java-driver-mapper-runtime</artifactId>
          <version>${driver.version}</version>
        </dependency>

    * See the `Java Driver documentation <https://java-driver.docs.scylladb.com/>`_ for details.
    * `Learn how to use Java with ScyllaDB <https://university.scylladb.com/courses/using-scylla-drivers/lessons/coding-with-java-part-1/>`_ on ScyllaDB University.

  .. group-tab:: Go
    
    For Golang developers, ScyllaDB has forked the GoCQL client driver for CQL, 
    adding enhanced capabilities that take advantage of ScyllaDB’s architecture.

    This is a drop-in replacement for gocql, and it reuses the 
    ``github.com/gocql/gocql`` import path. 

    To install the driver:

    #. Add the following line to your project ``go.mod`` file:

        .. code::
        
            replace github.com/gocql/gocql => github.com/scylladb/gocql latest

    #. Run:

        .. code::

            go mod tidy

    * See the `Go Driver documentation <https://opensource.docs.scylladb.com/stable/using-scylla/drivers/cql-drivers/scylla-go-driver.html>`_ for details.
    * `Learn how to use Go with ScyllaDB <https://university.scylladb.com/courses/using-scylla-drivers/lessons/golang-and-scylla-part-1/>`_ on ScyllaDB University.

  .. group-tab:: JavaScript

    For JavaScript developers, ScyllaDB can use the Cassandra driver for CQL.
    ``yarn`` is the suggested tool for installing packages and required dependencies.

    Run the following command:

    .. code::

      yarn install cassandra-driver

    * Alternatively, you can use ``npm`` to install packages with the same name.
    * `Learn how to use Node.js with ScyllaDB <https://university.scylladb.com/courses/using-scylla-drivers/lessons/scylla-and-node-js/>`_ on ScyllaDB University.


  .. group-tab:: Other Languages
    
    See `ScyllaDB CQL Drivers <https://opensource.docs.scylladb.com/master/using-scylla/drivers/cql-drivers/index.html>`_ 
    for a full list of drivers supported by ScyllaDB.
