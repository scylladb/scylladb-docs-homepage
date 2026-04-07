==================
Upgrade Policy
==================

ScyllaDB upgrade is a rolling procedure - it does not require a full cluster
shutdown and is performed without any downtime or disruption of service.

Rules and Guidelines
-------------------------

* To ensure a successful upgrade, follow the `documented upgrade procedures <https://docs.scylladb.com/manual/stable/upgrade/>`_ 
  tested by ScyllaDB.
* You should upgrade to a supported version of ScyllaDB.
  See :doc:`ScyllaDB Version Support </versioning/version-support/>`.
* All nodes in the cluster must be on the same version before advancing to
  the next version.

Upgrade Paths
--------------------

Major Releases (LTS)
=====================

* You can upgrade from the a major version to the next major version, skipping
  intermediate minor releases.
* You cannot skip major versions. Upgrades must proceed from one major version
  to the next.
* Example: 2025.1 → 2026.1

Minor Releases (Feature Releases)
======================================

In version 2025.4, we updated the upgrade policy to allow non-consecutive minor
upgrades. You can upgrade to:

* Any minor version within the same major release. Examples: 2025.1 → 2025.4,
  2026.x → 2026.y
* The next major (LTS) version. Example: 2025.x → 2026.1

For **versions earlier than 2025.4**, minor upgrades must be performed
consecutively — each successive X.Y version must be installed in order,
without skipping any major or minor version.

Patch Releases
===============

Upgrading to each patch version by following the *Maintenance Release Upgrade
Guide* is optional. However, we recommend upgrading to the latest patch release
for your version before upgrading to a new version.

Downgrade
---------------

Downgrade is not available as a standard operation. Reverting to a previous
version is only possible during the rolling upgrade process, where it is
referred to as a rollback.

Rollback is possible only while some nodes in the cluster have not yet been
upgraded. Once the final node is started with the new version, rollback is no
longer possible. After that, the only way to return to a previous version is
to restore the cluster from backup.

In cases where a downgrade is necessary, please contact ScyllaDB support for
assistance.

