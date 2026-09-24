# OS Support by Linux Distributions and Version

The following matrix shows which Linux distributions, containers, and images
are [supported](#os-support-definition) with which versions of ScyllaDB.

|                               |                                                           |                                                           |                                                               | Linux Distributions                                       | Ubuntu                                                     | Debian                                                    | Rocky / Centos /<br/>RHEL                                 | Amazon Linux                                               |
|-------------------------------|-----------------------------------------------------------|-----------------------------------------------------------|---------------------------------------------------------------|-----------------------------------------------------------|------------------------------------------------------------|-----------------------------------------------------------|-----------------------------------------------------------|------------------------------------------------------------|
| ScyllaDB Version / OS Version | 20.04                                                     | 22.04                                                     | 24.04                                                         | 11                                                        | 12                                                         | 8                                                         | 9                                                         | 2023                                                       |
| ScyllaDB 2025.1               | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>     | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| Enterprise 2024.2             | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>     | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| Enterprise 2024.1             | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> `*` | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-cancel" aria-hidden="true"></i> |
| Open Source 6.2               | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>     | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
> `*` 2024.1.9 and later

All releases are available as a Docker container, EC2 AMI, GCP, and Azure images.

<a id="os-support-definition"></a>

By *supported*, it is meant that:

- A binary installation package is available to [download](https://www.scylladb.com/download/).
- The download and install procedures are tested as part of the ScyllaDB release process for each version.
- An automated install is included from [ScyllaDB Web Installer for Linux tool](https://docs.scylladb.com/manual/branch-2025.1/getting-started/installation-common/scylla-web-installer.md) (for the latest versions).

You can [build ScyllaDB from source](https://github.com/scylladb/scylladb#build-prerequisites)
on other x86_64 or aarch64 platforms, without any guarantees.
