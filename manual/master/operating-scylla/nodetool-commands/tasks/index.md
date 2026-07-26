# Nodetool tasks

**tasks** - Nodetool supercommand for managing task manager tasks.

Task manager is an API-based tool for tracking long-running background operations, such as repair or compaction,
which makes them observable and controllable. Task manager operates per node.

## Task Status Retention

* When a task completes, its status is temporarily stored on the executing node
* Status information is retained for up to [`task_ttl_in_seconds`](https://docs.scylladb.com/manual/master/reference/configuration-parameters.md#confval-task_ttl_in_seconds) seconds

## Supported tasks suboperations

* [abort](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/tasks/abort.md) - Aborts the task.
* [drain](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/tasks/drain.md) - Unregisters all finished local tasks.
* [user-ttl](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/tasks/user-ttl.md) - Gets or sets user_task_ttl value.
* [list](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/tasks/list.md) - Lists tasks in the module.
* [modules](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/tasks/modules.md) - Lists supported modules.
* [status](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/tasks/status.md) - Gets status of the task.
* [tree](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/tasks/tree.md) - Gets statuses of the task and all its descendants.
* [ttl](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/tasks/ttl.md) - Gets or sets task_ttl value.
* [wait](https://docs.scylladb.com/manual/master/operating-scylla/nodetool-commands/tasks/wait.md) - Waits for the task and gets its status.
