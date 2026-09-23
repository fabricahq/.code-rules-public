---
title: "Include Useful Diagnostic Data"
whenToRead: "Before returning or reviewing a Go error across a package, persistence, transport, filesystem, or network boundary."
impact: "MEDIUM"
impactDescription: "makes boundary failures understandable when logged alone"
tags: "go, errors, diagnostics, context, wrapping, boundary, logging"
---

## Include Useful Diagnostic Data

Errors that cross package, persistence, transport, filesystem, network,
parsing, or serialization boundaries should say what failed and which stable
resource was involved. A bare `return err` or `return store.ErrNotFound` is not
enough once the error may be logged by a caller that lacks local context.

**Incorrect:**

```go
if err := tx.Commit(ctx); err != nil {
	return err
}

if draft.DocumentID != document.ID {
	return store.ErrNotFound
}
```

**Correct:**

```go
if err := tx.Commit(ctx); err != nil {
	return fmt.Errorf("promote document draft documentID=%q versionID=%q: commit transaction: %v", document.ID, version.ID, err)
}

if draft.DocumentID != document.ID {
	return fmt.Errorf("promote document draft documentID=%q draftID=%q: draft belongs to documentID=%q: %w", document.ID, draft.ID, draft.DocumentID, store.ErrNotFound)
}
```

**Guidelines:**

- Name the operation in domain language: `promote document draft`, not
  `call CommitDocumentDraftPromotion`.
- Include stable IDs that narrow the failure: `documentID`, `draftID`,
  `versionID`, `orgID`, `path`, route, or query name.
- Prefer the shape `"<operation> key=%q: <specific failure>: <cause>"`.
- Avoid repeated labels. One clear boundary wrapper is better than
  `promote draft: commit promotion: tx commit: commit: ...`.
- Error strings are log/debug diagnostics, not polished UI copy. Map them to
  product language at the transport or frontend boundary.
- Never include secrets, tokens, credentials, or raw request bodies.
