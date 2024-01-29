=======================
Schema Design
=======================

When adopting a query-first data model, the same constraints need to be applied 
to the schema design. 
While schema design can evolve to meet your changing application needs, there 
are certain choices you will need to make to get the most value out of ScyllaDB. 
This further reinforces the concept of adopting a query-first data model.

**Data Types**

Selecting the appropriate `data type <https://opensource.docs.scylladb.com/stable/cql/types.html>`_
for your columns is critical to your application semantics in your data model.
You will need to consider factors such as data size, indexing, and sorting.

Let's say you're designing a table to store information about e-commerce 
products, and one of the attributes you want to capture is the product's price. 
The choice of data type for the "price" column is crucial for efficient storage 
and query performance.

.. code::

    CREATE TABLE my_keyspace.products (
      seller_id uuid,
      product_id uuid,
      product_name text,
      price decimal,
      description text
      PRIMARY KEY (seller_id, price, product_id)
    );

In this example, for the ``price``` column, we've chosen the decimal data type.
This data type is suitable for storing precise numerical values, such as prices,
as it preserves decimal precision. Choosing decimal over other numeric data types
like float or double is essential when dealing with financial data to avoid issues
with rounding errors.

You can efficiently index and query prices using the decimal data type, ensuring
fast and precise searches for products within specific price ranges partitioned by
``seller_id``. When you need to sort products by ``price``, the decimal data type
maintains the correct order, even for values with different decimal precision.
