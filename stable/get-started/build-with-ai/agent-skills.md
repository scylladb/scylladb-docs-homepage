# ScyllaDB Agent Skills

[ScyllaDB Agent Skills](https://github.com/scylladb/agent-skills) is a
collection of skills for AI coding agents ([GitHub Copilot](https://github.com/copilot), [Cursor](https://cursor.com), [Claude Code](https://claude.com/product/claude-code), and others) that provide
domain-specific knowledge about ScyllaDB and ScyllaDB Cloud. The skills help
agents write correct CQL queries, design efficient data models, and connect
applications to ScyllaDB Cloud.

## Installation

Install the `scylladb` skill first. It gives an overview of ScyllaDB and
a map of the other skills:

```bash
npx skills add scylladb/agent-skills --skill scylladb
```

To install all skills:

```bash
npx skills add scylladb/agent-skills
```

See the [agent-skills repository](https://github.com/scylladb/agent-skills)
for available skills and more information.
