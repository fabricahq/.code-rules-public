---
title: "Keep SQL Migrations in a Dedicated Directory"
whenToRead: "Before adding files to a project directory that goose uses for SQL migration discovery."
impact: "MEDIUM"
impactDescription: "Keeps the migration layout consistent with a project that discovers SQL migrations from one directory."
tags: "goose, sql, migrations, layout, directory"
---

## Keep SQL Migrations in a Dedicated Directory

When a project chooses a SQL-only directory for goose migration discovery, keep
that directory for numbered `.sql` migrations. Store documentation, helper
programs, and Go migration source elsewhere. This is an organization policy for
projects with a SQL-only migration directory; goose itself also supports Go
migrations through functions registered by application code.

**Incorrect for a SQL-only directory:**

```txt
db/migrations/
├── 001_extensions.sql
├── 002_users.sql
├── README.md
└── embed.go
```

The extra files mix documentation and Go source into a directory intended for
SQL migration files.

**Correct:**

```txt
db/migrations/
├── 001_extensions.sql
└── 002_users.sql
```

Keep migration documentation in a project guide or beside the directory. If a
durable data transformation genuinely needs application logic that SQL cannot
express, put its Go source in a separate package and register it through an
explicit migration command. A one-off tool followed by a SQL migration that
enforces the end state can also keep the migration history SQL-only. Where SQL
and Go migrations coexist, use one version sequence and ensure the project's
status and rollback commands include every registered migration.

### Validation

Inspect the configured SQL migration directory for non-SQL files and run the
project's goose status or migration check through its actual migration command.
