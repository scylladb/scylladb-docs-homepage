# ScyllaDB SStable Script API

The script API consists of two parts:

* [ScyllaDB Consume API]()

  <a id="scylla-consume-api"></a>
   - Hook methods implemented by the script to consume a [mutation fragment stream](https://docs.scylladb.com/manual/master/operating-scylla/admin-tools/scylla-sstable.md#scylla-sstable-sstable-content);
* [ScyllaDB Lua API]()

  <a id="scylla-script-lua-api"></a>
   - types and methods exposed to the script to work with ScyllaDB types and values.

<a id="scylla-consume-api"></a>

## ScyllaDB Consume API

These methods represent the glue code between scylla-sstable’s C++ code and the Lua script.
Conceptually a script is an implementation of a consumer interface. The script has to implement only the methods it is interested in. Each method has a default implementation in the interface, which simply drops the respective [mutation fragment](https://docs.scylladb.com/manual/master/operating-scylla/admin-tools/scylla-sstable.md#scylla-sstable-sstable-content).
For example, a script only interested in partitions can define only [consume_partition_start()](#scylla-consume-partition-start-method) and nothing else.
Therefore a completely empty script is also valid, although not very useful.
Below you will find the listing of the API methods.
These methods (if provided by the script) will be called by the scylla-sstable runtime for the appropriate events and fragment types.

<a id="scylla-consume-stream-start-method"></a>

### consume_stream_start(args)

* Part of the Consume API. Called on the very start of the stream.
* Parameter is a Lua table containing command line arguments for the script, passed via `--script-arg`.
* Can be used to initialize global state.

<a id="scylla-consume-sstable-start-method"></a>

### consume_sstable_start(sst)

* Part of the Consume API.
* Called on the start of each stable.
* The parameter is of type [ScyllaDB.sstable]()

  <a id="scylla-sstable-type"></a>
  .
* When SStables are merged (`--merge`), the parameter is `nil`.

Returns whether to stop. If `true`, [consume_sstable_end()]()

<a id="scylla-consume-sstable-end-method"></a>
 is called, skipping the content of the sstable (or that of the entire stream if `--merge` is used). If `false`, consumption follows with the content of the sstable.

<a id="scylla-consume-partition-start-method"></a>

### consume_partition_start(ps)

* Part of the Consume API. Called on the start of each partition.
* The parameter is of type [ScyllaDB.partition_start]()

  <a id="scylla-partition-start-type"></a>
  .
* Returns whether to stop. If `true`, [consume_partition_end()]()

  <a id="scylla-consume-partition-end-method"></a>
   is called, skipping the content of the partition. If `false`, consumption follows with the content of the partition.

### consume_static_row(sr)

* Part of the Consume API.
* Called if the partition has a static row.
* The parameter is of type [ScyllaDB.static_row]()

  <a id="scylla-static-row-type"></a>
  .
* Returns whether to stop. If `true`, [consume_partition_end()]()

  <a id="scylla-consume-partition-end-method"></a>
   is called, and the remaining content of the partition is skipped. If `false`, consumption follows with the remaining content of the partition.

### consume_clustering_row(cr)

* Part of the Consume API.
* Called for each clustering row.
* The parameter is of type [ScyllaDB.clustering_row]()

  <a id="scylla-clustering-row-type"></a>
  .
* Returns whether to stop. If `true`, [consume_partition_end()]()

  <a id="scylla-consume-partition-end-method"></a>
   is called, the remaining content of the partition is skipped. If `false`, consumption follows with the remaining content of the partition.

### consume_range_tombstone_change(crt)

* Part of the Consume API.
* Called for each range tombstone change.
* The parameter is of type [ScyllaDB.range_tombstone_change]()

  <a id="scylla-range-tombstone-change-type"></a>
  .
* Returns whether to stop. If `true`, [consume_partition_end()]()

  <a id="scylla-consume-partition-end-method"></a>
   is called, the remaining content of the partition is skipped. If `false`, consumption follows with the remaining content of the partition.

<a id="scylla-consume-partition-end-method"></a>

### consume_partition_end()

* Part of the Consume API.
* Called at the end of the partition.
* Returns whether to stop. If `true`, [consume_sstable_end()]()

  <a id="scylla-consume-sstable-end-method"></a>
   is called,  the remaining content of the SStable is skipped. If `false`, consumption follows with the remaining content of the SStable.

<a id="scylla-consume-sstable-end-method"></a>

### consume_sstable_end()

* Part of the Consume API.
* Called at the end of the SStable.
* Returns whether to stop. If true, [consume_stream_end()]()

  <a id="scylla-consume-stream-end-method"></a>
   is called, the remaining content of the stream is skipped. If false, consumption follows with the remaining content of the stream.

<a id="scylla-consume-stream-end-method"></a>

### consume_stream_end()

* Part of the Consume API.
* Called at the very end of the stream.

<a id="scylla-script-lua-api"></a>

## ScyllaDB LUA API

In addition to the [ScyllaDB Consume API]()

<a id="scylla-consume-api"></a>
, the Lua bindings expose various types and methods that allow you to work with ScyllaDB types and values.
The listing uses the following terminology:

* Attribute - a simple attribute accessible via `obj.attribute_name`;
* Method - a method operating on an instance of said type, invocable as `obj:method()`;
* Magic method - magic methods defined in the metatable which define behaviour of these objects w.r.t. [Lua operators and more](http://www.lua.org/manual/5.4/manual.html#2.4);

The format of an attribute description is the following:

```none
attribute_name (type) - description
```

and that of a method:

```none
method_name(arg1_type, arg2_type...) (return_type) - description
```

Magic methods have their signature defined by Lua and so that is not described here (these methods are not used directly anyway).

<a id="scylla-atomic-cell-type"></a>

### ScyllaDB.atomic_cell

Attributes:

* timestamp (integer)
* is_live (boolean) - is the cell live?
* type (string) - one of: `regular`, `counter-update`, `counter-shards`, `frozen-collection` or `collection`.
* has_ttl (boolean) - is the cell expiring?
* ttl (integer) - time to live in seconds, `nil` if cell is not expiring.
* expiry ([ScyllaDB.gc_clock_time_point]()

  <a id="scylla-gc-clock-time-point-type"></a>
  ) - time at which cell expires, `nil` if cell is not expiring.
* deletion_time ([ScyllaDB.gc_clock_time_point]()

  <a id="scylla-gc-clock-time-point-type"></a>
  ) - time at which cell was deleted, `nil` unless cell is dead or expiring.
* value:
  > - `nil` if cell is dead.
  > - appropriate Lua native type if type == `regular`.
  > - integer if type == `counter-update`.
  > - [ScyllaDB.counter_shards_value]()

  >   <a id="scylla-counter-shards-value-type"></a>
  >    if type == `counter-shards`.

A counter-shard table has the following keys:

* id (string)
* value (integer)
* clock (integer)

<a id="scylla-clustering-key-type"></a>

### ScyllaDB.clustering_key

Attributes:

* components (table) - the column values ([ScyllaDB.data_value]()

  <a id="scylla-data-value-type"></a>
  ) making up the composite clustering key.

Methods:

* to_hex - convert the key to its serialized format, encoded in hex.

Magic methods:

* \_\_tostring - can be converted to string with tostring(), uses the built-in operator<< in ScyllaDB.

<a id="scylla-clustering-row-type"></a>

### ScyllaDB.clustering_row

Attributes:

* key ($TYPE) - the clustering key’s value as the appropriate Lua native type.
* tombstone ([ScyllaDB.tombstone]()

  <a id="scylla-tombstone-type"></a>
  ) - row tombstone, `nil` if no tombstone.
* shadowable_tombstone ([ScyllaDB.tombstone]()

  <a id="scylla-tombstone-type"></a>
  ) - shadowable tombstone of the row tombstone, `nil` if no tombstone.
* marker ([ScyllaDB.row_marker]()

  <a id="scylla-row-marker-type"></a>
  ) - the row marker, `nil` if row doesn’t have one.
* cells (table) - table of cells, where keys are the column names and the values are either of type [ScyllaDB.atomic_cell]()

  <a id="scylla-atomic-cell-type"></a>
   or [ScyllaDB.collection]()

  <a id="scylla-collection-type"></a>
  .

See also:

* [ScyllaDB.unserialize_clustering_key()]()

  <a id="scylla-unserialize-clustering-key-method"></a>
  .

<a id="scylla-collection-type"></a>

### ScyllaDB.collection

Attributes:

* type (string) - always `collection` for collection.
* tombstone ([ScyllaDB.tombstone]()

  <a id="scylla-tombstone-type"></a>
  ) - `nil` if no tombstone.
* cells (table) - the collection cells, each collection cell is a table, with a `key` and `value` attribute. The key entry is the key of the collection cell for actual collections (list, set and map) and is of type [ScyllaDB.data-value]()

  <a id="scylla-data-value-type"></a>
  . For tuples and UDT this is just an empty string. The value entry is the value of the collection cell and is of type [ScyllaDB.atomic-cell]()

  <a id="scylla-atomic-cell-type"></a>
  .

<a id="scylla-collection-cell-value-type"></a>

### ScyllaDB.collection_cell_value

Attributes:

* key (sstring) - collection cell key in human readable form.
* value ([ScyllaDB.atomic_cell]()

  <a id="scylla-atomic-cell-type"></a>
  ) - collection cell value.

<a id="scylla-column-definition-type"></a>

### ScyllaDB.column_definition

Attributes:

* id (integer) - the id of the column.
* name (string) - the name of the column.
* kind (string) - the kind of the column, one of `partition_key`, `clustering_key`, `static_column` or `regular_column`.

<a id="scylla-counter-shards-value-type"></a>

### ScyllaDB.counter_shards_value

Attributes:

* value (integer) - the total value of the counter (the sum of all the shards).
* shards (table) - the shards making up this counter, a lua list containing tables, representing shards, with the following key/values:
  > - id (string) - the shard’s id (UUID).
  > - value (integer) - the shard’s value.
  > - clock (integer) - the shard’s logical clock.

Magic methods:

* \_\_tostring - can be converted to string with tostring().

<a id="scylla-data-value-type"></a>

### ScyllaDB.data_value

Attributes:

* value - the value represented as the appropriate Lua type

Magic methods:

* \_\_tostring - can be converted to string with tostring().

<a id="scylla-gc-clock-time-point-type"></a>

### ScyllaDB.gc_clock_time_point

A time point belonging to the gc_clock, in UTC.

Attributes:

* year (integer) - [1900, +inf).
* month (integer) - [1, 12].
* day (integer) - [1, 31].
* hour (integer) - [0, 23].
* min (integer) - [0, 59].
* sec (integer) - [0, 59].

Magic methods:

* \_\_eq - can be equal compared.
* \_\_lt - can be less compared.
* \_\_le - can be less-or-equal compared.
* \_\_tostring - can be converted to string with tostring().

See also:

* [ScyllaDB.now()]()

  <a id="scylla-now-method"></a>
  .
* [ScyllaDB.time_point_from_string()]()

  <a id="scylla-time-point-from-string-method"></a>
  .

<a id="scylla-json-writer-type"></a>

### ScyllaDB.json_writer

A JSON writer object, with both low-level and high-level APIs.
The low-level API allows you to write custom JSON and it loosely follows the API of [rapidjson::Writer](https://rapidjson.org/classrapidjson_1_1_writer.html) (upon which it is implemented).
The high-level API is for writing [mutation fragments](https://docs.scylladb.com/manual/master/operating-scylla/admin-tools/scylla-sstable.md#scylla-sstable-sstable-content) as JSON directly, using the built-in JSON conversion logic that is used by [dump-data](https://docs.scylladb.com/manual/master/operating-scylla/admin-tools/scylla-sstable.md#scylla-sstable-dump-data-operation) operation.

Low level API Methods:

* null() - write a null json value.
* bool(boolean) - write a bool json value.
* int(integer) - write an integer json value.
* double(number) - write a double json value.
* string(string) - write a string json value.
* start_object() - start a json object.
* key(string) - write the key of a json object.
* end_object() - write the end of a json object.
* start_array() - write the start of a json array.
* end_array() - write the end of a json array.

High level API Methods:

* start_stream() - start the stream, call at the very beginning.
* start_sstable() - start an sstable.
* start_partition() - start a partition.
* static_row() - write a static row to the stream.
* clustering_row() - write a clustering row to the stream.
* range_tombstone_change() - write a range tombstone change to the stream.
* end_partition() - end the current partition.
* end_sstable() - end the current sstable.
* end_stream() - end the stream, call at the very end.

<a id="scylla-new-json-writer-method"></a>

### ScyllaDB.new_json_writer()

Create a [ScyllaDB.json_writer]()

<a id="scylla-json-writer-type"></a>
 instance.

<a id="scylla-new-position-in-partition-method"></a>

### ScyllaDB.new_position_in_partition()

Creates a [ScyllaDB.position_in_partition]()

<a id="scylla-position-in-partition-type"></a>
 instance.

Arguments:

* weight (integer) - the weight of the key.
* key ([ScyllaDB.clustering_key]()

  <a id="scylla-clustering-key-type"></a>
  ) - the clustering key, optional.

<a id="scylla-new-ring-position-method"></a>

### ScyllaDB.new_ring_position()

Creates a [ScyllaDB.ring_position]()

<a id="scylla-ring-position-type"></a>
 instance.

Has several overloads:

* `ScyllaDB.new_ring_position(weight, key)`.
* `ScyllaDB.new_ring_position(weight, token)`.
* `ScyllaDB.new_ring_position(weight, key, token)`.

Where:

* weight (integer) - the weight of the key.
* key ([ScyllaDB.partition_key]()

  <a id="scylla-partition-key-type"></a>
  ) - the partition key.
* token (integer) - the token (of the key if a key is provided).

<a id="scylla-now-method"></a>

### ScyllaDB.now()

Create a [ScyllaDB.gc_clock_time_point]()

<a id="scylla-gc-clock-time-point-type"></a>
 instance, representing the current time.

<a id="scylla-partition-key-type"></a>

### ScyllaDB.partition_key

Attributes:

* components (table) - the column values ([ScyllaDB.data_value]()

  <a id="scylla-data-value-type"></a>
  ) making up the composite partition key.

Methods:

* to_hex - convert the key to its serialized format, encoded in hex.

Magic methods:

* \_\_tostring - can be converted to string with tostring(), uses the built-in operator<< in ScyllaDB.

See also:

* [ScyllaDB.unserialize_partition_key()](#scylla-unserialize-partition-key-method).
* [ScyllaDB.token_of()](#scylla-token-of-method).

<a id="scylla-partition-start-type"></a>

### ScyllaDB.partition_start

Attributes:

* key - the partition key’s value as the appropriate Lua native type.
* token (integer) - the partition key’s token.
* tombstone ([ScyllaDB.tombstone]()

  <a id="scylla-tombstone-type"></a>
  ) - the partition tombstone, `nil` if no tombstone.

<a id="scylla-position-in-partition-type"></a>

### ScyllaDB.position_in_partition

Currently used only for clustering positions.

Attributes:

* key ([ScyllaDB.clustering_key]()

  <a id="scylla-clustering-key-type"></a>
  ) - the clustering key, `nil` if the position in partition represents the min or max clustering positions.
* weight (integer) - weight of the position, either -1 (before key), 0 (at key) or 1 (after key). If key attribute is `nil`, the weight is never 0.

Methods:

* tri_cmp - compare this position in partition to another position in partition, returns -1 (`<`), 0 (`==`) or 1 (`>`).

See also:

* [ScyllaDB.new_position_in_partition()]()

  <a id="scylla-new-position-in-partition-method"></a>
  .

<a id="scylla-range-tombstone-change-type"></a>

### ScyllaDB.range_tombstone_change

Attributes:

* key ($TYPE) - the clustering key’s value as the appropriate Lua native type.
* key_weight (integer) - weight of the position, either -1 (before key), 0 (at key) or 1 (after key).
* tombstone ([ScyllaDB.tombstone]()

  <a id="scylla-tombstone-type"></a>
  ) - tombstone, `nil` if no tombstone.

<a id="scylla-ring-position-type"></a>

### ScyllaDB.ring_position

Attributes:

* token (integer) - the token, `nil` if the ring position represents the min or max ring positions.
* key ([ScyllaDB.partition_key]()

  <a id="scylla-partition-key-type"></a>
  ) - the partition key, `nil` if the ring position represents a position before/after a token.
* weight (integer) - weight of the position, either -1 (before key/token), 0 (at key) or 1 (after key/token). If key attribute is `nil`, the weight is never 0.

Methods:

* tri_cmp - compare this ring position to another ring position, returns -1 (`<`), 0 (`==`) or 1 (`>`).

See also:

* [ScyllaDB.new_ring_position()]()

  <a id="scylla-new-ring-position-method"></a>
  .

<a id="scylla-row-marker-type"></a>

### ScyllaDB.row_marker

Attributes:

* timestamp (integer).
* is_live (boolean) - is the marker live?
* has_ttl (boolean) - is the marker expiring?
* ttl (integer) - time to live in seconds, `nil` if marker is not expiring.
* expiry ([ScyllaDB.gc_clock_time_point]()

  <a id="scylla-gc-clock-time-point-type"></a>
  ) - time at which marker expires, `nil` if marker is not expiring.
* deletion_time ([ScyllaDB.gc_clock_time_point]()

  <a id="scylla-gc-clock-time-point-type"></a>
  ) - time at which marker was deleted, `nil` unless marker is dead or expiring.

<a id="scylla-schema-type"></a>

### ScyllaDB.schema

Attributes:

* partition_key_columns (table) - list of [ScyllaDB.column_definition]()

  <a id="scylla-column-definition-type"></a>
   of the key columns making up the partition key.
* clustering_key_columns (table) - list of [ScyllaDB.column_definition]()

  <a id="scylla-column-definition-type"></a>
   of the key columns making up the clustering key.
* static_columns (table) - list of [ScyllaDB.column_definition]()

  <a id="scylla-column-definition-type"></a>
   of the static columns.
* regular_columns (table) - list of [ScyllaDB.column_definition]()

  <a id="scylla-column-definition-type"></a>
   of the regular columns.
* all_columns (table) - list of [ScyllaDB.column_definition]()

  <a id="scylla-column-definition-type"></a>
   of all columns.

<a id="scylla-sstable-type"></a>

### ScyllaDB.sstable

Attributes:

* filename (string) - the full path of the sstable Data component file;

<a id="scylla-static-row-type"></a>

### ScyllaDB.static_row

Attributes:

* cells (table) - table of cells, where keys are the column names and the values are either of type [ScyllaDB.atomic_cell]()

  <a id="scylla-atomic-cell-type"></a>
   or [ScyllaDB.collection]()

  <a id="scylla-collection-type"></a>
  .

<a id="scylla-time-point-from-string-method"></a>

### ScyllaDB.time_point_from_string()

Create a [ScyllaDB.gc_clock_time_point]()

<a id="scylla-gc-clock-time-point-type"></a>
 instance from the passed in string.
Argument is string, using the same format as the CQL timestamp type, see [https://en.wikipedia.org/wiki/ISO_8601](https://en.wikipedia.org/wiki/ISO_8601).

<a id="scylla-token-of-method"></a>

### ScyllaDB.token_of()

Compute and return the token (integer) for a [ScyllaDB.partition_key]()

<a id="scylla-partition-key-type"></a>
.

<a id="scylla-tombstone-type"></a>

### ScyllaDB.tombstone

Attributes:

* timestamp (integer)
* deletion_time ([ScyllaDB.gc_clock_time_point]()

  <a id="scylla-gc-clock-time-point-type"></a>
  ) - the point in time at which the tombstone was deleted.

<a id="scylla-unserialize-clustering-key-method"></a>

### ScyllaDB.unserialize_clustering_key()

Create a [ScyllaDB.clustering_key]()

<a id="scylla-clustering-key-type"></a>
 instance.

Argument is a string representing serialized clustering key in hex format.

<a id="scylla-unserialize-partition-key-method"></a>

### ScyllaDB.unserialize_partition_key()

Create a [ScyllaDB.partition_key]()

<a id="scylla-partition-key-type"></a>
 instance.

Argument is a string representing serialized partition key in hex format.
