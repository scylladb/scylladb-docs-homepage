# OS Support per ScyllaDB Version

ScyllaDB is designed to run on modern 64-bit Linux operating systems. To ensure
stability, predictable performance, and access to timely fixes, ScyllaDB is
officially supported on a defined set of Linux distributions.

## Supported Platforms

The following support matrix lists the Linux distributions, container
platforms, and cloud images officially [supported](#os-support-definition)
for each ScyllaDB version.

| Linux Distributions           | Ubuntu                                                    |                                                               | Debian                                                    |                                                            | Rocky / CentOS / RHEL                                     |                                                           |                                                            | Amazon Linux                                               |
|-------------------------------|-----------------------------------------------------------|---------------------------------------------------------------|-----------------------------------------------------------|------------------------------------------------------------|-----------------------------------------------------------|-----------------------------------------------------------|------------------------------------------------------------|------------------------------------------------------------|
| ScyllaDB Version / OS Version | 22.04                                                     | 24.04                                                         | 11                                                        | 12                                                         | 8                                                         | 9                                                         | 10                                                         | 2023                                                       |
| ScyllaDB 2026.2               | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>     | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| ScyllaDB 2026.1               | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>     | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| ScyllaDB 2025.4               | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>     | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| ScyllaDB 2025.3               | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>     | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| ScyllaDB 2025.2               | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>     | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| ScyllaDB 2025.1               | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>     | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| Enterprise 2024.2             | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>     | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i>  |
| Enterprise 2024.1             | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> `*` | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-check" aria-hidden="true"></i> | <i class="inline-icon icon-cancel" aria-hidden="true"></i> | <i class="inline-icon icon-cancel" aria-hidden="true"></i> |
<script>
// Adds colspan support for list-table
document.addEventListener('DOMContentLoaded', () => {
    const firstRow = document.querySelector('.os-support-table thead tr:first-child');
    if (!firstRow) return;

    const cells = Array.from(firstRow.children);
    let currentIndex = 0;

    while (currentIndex < cells.length) {
        const currentCell = cells[currentIndex];
        if (currentCell.textContent.trim()) {
            let colspan = 1;
            while (currentIndex + colspan < cells.length && 
                   !cells[currentIndex + colspan].textContent.trim()) {
                colspan++;
            }
            currentCell.colSpan = colspan;
            for (let i = 1; i < colspan; i++) {
                cells[currentIndex + i].remove();
            }
            currentIndex += colspan;
        } else {
            currentCell.remove();
            cells.splice(currentIndex, 1);
        }
    }
});
</script>

`*` 2024.1.9 and later

All ScyllaDB releases are available as a Docker container, EC2 AMI, GCP, and Azure images.

<a id="os-support-definition"></a>

## Definition of Supported Platforms

A platform is considered supported when all of the following conditions are
met:

* A binary installation package is available for download.
* The download and installation procedures are tested as part of the ScyllaDB
  release process for each version.
* Automated installation is supported via the
  [ScyllaDB Web Installer for Linux](https://docs.scylladb.com/manual/stable/getting-started/installation-common/scylla-web-installer.html)
  (for applicable and recent versions).

Platforms outside the supported list may still be usable. ScyllaDB can be
[built from source](https://github.com/scylladb/scylladb#build-prerequisites)
on other x86_64 or aarch64 Linux systems; however, such deployments are not
tested, not validated, and not covered by support guarantees.
