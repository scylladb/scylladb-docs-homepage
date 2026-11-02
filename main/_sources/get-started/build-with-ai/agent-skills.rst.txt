=====================
ScyllaDB Agent Skills
=====================

`ScyllaDB Agent Skills <https://github.com/scylladb/agent-skills>`_ is a
collection of skills for AI coding agents (`GitHub Copilot
<https://github.com/copilot>`_, `Cursor <https://cursor.com>`_, `Claude Code
<https://claude.com/product/claude-code>`_, and others) that provide
domain-specific knowledge about ScyllaDB and ScyllaDB Cloud. The skills help
agents write correct CQL queries, design efficient data models, and connect
applications to ScyllaDB Cloud.

Installation
------------

Install the ``scylladb`` skill first. It gives an overview of ScyllaDB and
a map of the other skills:

.. code-block:: bash

   npx skills add scylladb/agent-skills --skill scylladb

To install all skills:

.. code-block:: bash

   npx skills add scylladb/agent-skills

See the `agent-skills repository <https://github.com/scylladb/agent-skills>`_
for available skills and more information.
