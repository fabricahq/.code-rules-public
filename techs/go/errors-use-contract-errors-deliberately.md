---
title: "Use Contract Errors Deliberately"
whenToRead: "Before defining or wrapping a Go error that callers may inspect with errors.Is or errors.As."
impact: "MEDIUM"
impactDescription: "separates caller-visible semantics from diagnostic failures"
tags: "go, errors, wrapping, sentinel, contract, domain, boundary"
---

## Use Contract Errors Deliberately

Define or return a domain/package contract error only when callers should branch
on its identity. Otherwise return a contextual `fmt.Errorf` for diagnostics.

Contract errors are API. Once a package returns `fmt.Errorf("...: %w",
store.ErrNotFound)`, callers may depend on `errors.Is(err, store.ErrNotFound)`.
That is appropriate for stable semantics such as `store.ErrNotFound`,
`store.ErrForbidden`, `store.ErrConflict`, and app validation errors. It is not
appropriate for implementation details such as `pgx.ErrNoRows`,
`pgconn.PgError`, `sql.ErrNoRows`, or `fs.PathError` unless those concrete
errors are intentionally part of the package contract.

**Incorrect:**

```go
if err := q.SaveDocumentDraft(ctx, params); err != nil {
	return fmt.Errorf("save document draft: %w", err)
}
```

This exposes a database driver error as a caller-visible API.

**Correct:**

```go
if errors.Is(err, pgx.ErrNoRows) {
	return fmt.Errorf("load document documentID=%q: %w", documentID, store.ErrNotFound)
}
if err != nil {
	return fmt.Errorf("load document documentID=%q: %v", documentID, err)
}
```

The no-row case is translated into the store contract. The unexpected driver
error keeps diagnostic text without exposing driver identity.

**Guidelines:**

- Add a contract error only when a caller maps it to behavior: HTTP status,
  desktop API shape, UI state, retry/recovery, telemetry, or cross-implementation
  semantics.
- Wrap contract errors with `%w`; do not wrap implementation details with `%w`
  at package boundaries.
- Use `%v` for internal failures where callers can only log, show a generic
  failure, or abort the operation.
- Choose the contract by domain meaning. `ErrNotFound` is for absent or
  intentionally cloaked resources, `ErrForbidden` is for known-but-denied
  access, `ErrConflict` is for uniqueness/state conflicts, and validation
  errors are for bad commands.
