======================================
OS Support per ScyllaDB Version
======================================

ScyllaDB is designed to run on modern 64-bit Linux operating systems. To ensure
stability, predictable performance, and access to timely fixes, ScyllaDB is
officially supported on a defined set of Linux distributions.

Supported Platforms
---------------------------

The following support matrix lists the Linux distributions, container
platforms, and cloud images officially :ref:`supported <os-support-definition>`
for each ScyllaDB version.

.. datatemplate:json:: /_static/data/os-support.json
  :template: platforms.tmpl

``*`` 2024.1.9 and later

All ScyllaDB releases are available as a Docker container, EC2 AMI, GCP, and Azure images.

.. _os-support-definition:

Definition of Supported Platforms
-----------------------------------

A platform is considered supported when all of the following conditions are
met:

* A binary installation package is available for download.
* The download and installation procedures are tested as part of the ScyllaDB
  release process for each version.
* Automated installation is supported via the
  `ScyllaDB Web Installer for Linux <https://docs.scylladb.com/manual/stable/getting-started/installation-common/scylla-web-installer.html>`_
  (for applicable and recent versions).

Platforms outside the supported list may still be usable. ScyllaDB can be
`built from source <https://github.com/scylladb/scylladb#build-prerequisites>`_
on other x86_64 or aarch64 Linux systems; however, such deployments are not
tested, not validated, and not covered by support guarantees.