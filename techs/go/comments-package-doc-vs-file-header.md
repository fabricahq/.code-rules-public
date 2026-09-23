---
title: "Separate Package Docs From File Headers"
whenToRead: "Before writing or reviewing a comment immediately above a Go package declaration."
impact: "LOW"
impactDescription: "prevents file-level notes from accidentally becoming package documentation"
tags: "go, comments, package, docs, file-header, spacing"
---

## Separate Package Docs From File Headers

In Go, a top comment immediately followed by `package` is package
documentation. A blank line between the comment and `package` makes the comment
a file header instead. Choose deliberately:

- If the comment documents the package as a whole, attach it directly to
  `package` and start it with `Package <name> ...`.
- If the comment documents why this file exists or what this file owns, leave
  exactly one blank line before `package`.

**Incorrect file header:**

```go
// Projection helpers for mock fixture JSON.
package devseed
```

The comment describes one file, but because it touches `package`, Go treats it
as package documentation.

**Correct file header:**

```go
// Projection helpers for mock fixture JSON.

package devseed
```

Use this form when a source file needs a file-level comment.

**Incorrect package doc:**

```go
// Package devseed owns the canonical local-development sample world.

package devseed
```

The comment describes the whole package, but the blank line detaches it from
the package declaration.

**Correct package doc:**

```go
// Package devseed owns the canonical local-development sample world.
package devseed
```

**Guidelines:**

- Do not start file headers with `Package <name>`; that wording is reserved for
  package docs.
- Do not attach file headers directly to `package`, even if the file is the only
  file in the package.
- Put package docs in the file intended to own package documentation, commonly
  `doc.go` or the package's central source file.
- If there is no package-level documentation to add, prefer a file header with a
  blank line over an accidental package doc.
