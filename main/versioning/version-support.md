# ScyllaDB Version Support

## Supported Versions

| Version                                                                                                 | Released       | Status        | End of Life (EOL)                                                                  |
|---------------------------------------------------------------------------------------------------------|----------------|---------------|------------------------------------------------------------------------------------|
| [ScyllaDB 2026.3](https://docs.scylladb.com/manual/branch-2026.3/getting-started/install-scylla/)       | September 2026 | Supported     | After 2027.1 is released   (see [Version Support Policy](#version-support-policy)) |
| [ScyllaDB 2026.2](https://docs.scylladb.com/manual/branch-2026.2/getting-started/install-scylla/)       | June 2026      | Supported     | After 2026.4 is released   (see [Version Support Policy](#version-support-policy)) |
| [ScyllaDB 2026.1 (LTS)](https://docs.scylladb.com/manual/branch-2026.1/getting-started/install-scylla/) | March 2026     | Supported     | After 2028.1 is released   (see [Version Support Policy](#version-support-policy)) |
| ScyllaDB 2025.4                                                                                         | December 2025  | Not supported | June 2026                                                                          |
| ScyllaDB 2025.3                                                                                         | September 2025 | Not supported | March 2026                                                                         |
| ScyllaDB 2025.2                                                                                         | July 2025      | Not supported | December 2025                                                                      |
| [ScyllaDB 2025.1 (LTS)](https://docs.scylladb.com/manual/branch-2025.1/getting-started/install-scylla/) | April 2025     | Supported     | After 2027.1 is released   (see [Version Support Policy](#version-support-policy)) |
| Enterprise 2024.2                                                                                       | November 2024  | Not supported | July 2025                                                                          |
| Enterprise 2024.1 (LTS)                                                                                 | February 2024  | Not supported | March 2026                                                                         |
| Enterprise 2023.1 (LTS)                                                                                 | August 2023    | Not supported | April 2025                                                                         |
| Enterprise 2022.2                                                                                       | January 2023   | Not supported | June 2024                                                                          |
| Enterprise 2022.1 (LTS)                                                                                 | August 2022    | Not supported | June 2024                                                                          |

## Version Numbering

ScyllaDB follows the MAJOR.MINOR.PATCH [semantic versioning](https://semver.org/):

* `MAJOR` versions contain significant changes in the product and may
  introduce incompatible API changes.
* `MINOR` versions introduce new features and improvements in a backward-compatible manner.
* `PATCH` versions have backward-compatible bug fixes.

![image](versioning/images/versioning.png)

## LTS vs. Feature Releases

Long-Term Support (LTS)

* Released approximately once a year.
* Two last LTS versions are supported.

Feature releases:

* 2-4 feature releases per year.

You can only use LTS releases (upgrading to the latest patch release for
the greatest stability) or follow the feature and LTS releases for the latest
feature set.

<a id="version-support-policy"></a>

## Version Support Policy

* The last two LTS versions are supported.
* The last two *major.minor* versions (Feature or LTS release) are supported.

**Example**

* When 2024.2 (Feature) is released, the following are supported:
  * 2024.1 and 2023.1 (the last two LTS)
  * 2024.2 (Feature) and 2024.1 (LTS)
* When 2025.1 (LTS) is released, the following are supported:
  * 2025.1 and 2024.1 (the last two LTS)
  * 2024.2 (Feature)
* When 2025.2 (Feature) is released, the following are supported:
  * 2025.1 and 2024.1 (the last two LTS)
  * 2025.2 (Feature)

### Patch Versions

All supported versions (major and minor, LTS and Feature) will get patch
releases when required.

We recommend upgrading to the latest patch version. You should especially
upgrade to the latest patch of your current version before upgrading to
a new major or minor version.

## Upgrade Policy

To learn about the upgrade policy, see the [About Upgrade](https://docs.scylladb.com/manual/stable/upgrade/about-upgrade.html)
section in the ScyllaDB documentation.
