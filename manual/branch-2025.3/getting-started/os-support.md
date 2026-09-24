# OS Support by Linux Distributions and Version

The following matrix shows which Linux distributions, containers, and images
are [supported](#os-support-definition) with which versions of ScyllaDB.

| Linux Distributions           | Ubuntu                                                    |                                                               | Debian                                                    |                                                            | Rocky / CentOS / RHEL                                     |                                                           |                                                            | Amazon Linux                                               |
|-------------------------------|-----------------------------------------------------------|---------------------------------------------------------------|-----------------------------------------------------------|------------------------------------------------------------|-----------------------------------------------------------|-----------------------------------------------------------|------------------------------------------------------------|------------------------------------------------------------|
| ScyllaDB Version / OS Version | 22.04                                                     | 24.04                                                         | 11                                                        | 12                                                         | 8                                                         | 9                                                         | 10                                                         | 2023                                                       |
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

All releases are available as a Docker container, EC2 AMI, GCP, and Azure images.

<a id="os-support-definition"></a>

By *supported*, it is meant that:

- A binary installation package is available to [download](https://www.scylladb.com/download/).
- The download and install procedures are tested as part of the ScyllaDB release process for each version.
- An automated install is included from [ScyllaDB Web Installer for Linux tool](https://docs.scylladb.com/manual/branch-2025.3/getting-started/installation-common/scylla-web-installer.md) (for the latest versions).

You can [build ScyllaDB from source](https://github.com/scylladb/scylladb#build-prerequisites)
on other x86_64 or aarch64 platforms, without any guarantees.
