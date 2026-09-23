---
title: "Comment Non-Obvious Struct Fields"
whenToRead: "Before writing or reviewing Go struct fields whose zero values, ownership, or lifecycle carry a hidden invariant."
impact: "MEDIUM"
impactDescription: "keeps invariants, nil semantics, and field lifecycles discoverable at the definition"
tags: "go, comments, struct, fields, domain, invariants, nil, lifecycle"
---

## Comment Non-Obvious Struct Fields

Comment a struct field when the comment states a durable fact the type system
cannot express. The field's name and type already say what it is; the comment
exists to say what a value of the field *means* to the rest of the system.
Conversely, do not comment fields whose meaning is fully carried by their name
and type - filler comments train readers to skip all comments.

Describe properties, not operations. A field comment should stay true as long
as the domain understanding of the field holds, even while app services and
stores around it change. "Nil while the document has no saved versions" is a
property; "moves on save-version and restore" narrates the operations that
happen to write it today and goes stale when call flows change. Operation
behavior belongs in a comment on the operation.

Comment a field when at least one of these applies:

- **Nil/zero semantics** - a nil pointer or zero value means something beyond
  "absent" (`ParentFolderID == nil` is reserved for the hidden system root
  folder, not just "no parent yet").
- **Invariants and ownership** - the field participates in a rule enforced
  elsewhere ("the folder owns the document's workspace scope"; "at
  most one draft row per document").
- **Cross-context references** - the field holds a published ID into another
  bounded context, under an explicit cross-context contract, and must not
  become a casual import of that context's internals.
- **Role of a dependency** - for service structs, what the dependency is used
  for in this context, not what its type already says.

**Incorrect:**

```go
type Document struct {
	ID              string           `json:"id"`
	FolderID        string           `json:"folderId"`
	LatestVersion   *DocumentVersion `json:"latestVersion,omitempty"`
	LatestVersionID *string          `json:"latestVersionId,omitempty"`
	// CreatedAt is the creation timestamp.
	CreatedAt time.Time `json:"createdAt"`
}
```

`FolderID` and `LatestVersionID` carry invariants the reader cannot recover
from the types, while the one comment present restates its field name.

**Correct:**

```go
type Document struct {
	ID string `json:"id"`
	// FolderID is required; the folder owns the document's workspace scope, and
	// root-level documents point at the scope's hidden system root folder.
	FolderID string `json:"folderId"`
	// LatestVersion is the hydrated version row for LatestVersionID; it is
	// nil exactly when LatestVersionID is nil.
	LatestVersion *DocumentVersion `json:"latestVersion,omitempty"`
	// LatestVersionID is nil while the document has no saved versions.
	LatestVersionID *string          `json:"latestVersionId,omitempty"`
	CreatedAt       time.Time        `json:"createdAt"`
}
```

**Guidelines:**

- Apply to domain structs, store contracts, and service/Options structs -
  anywhere a field encodes an assumption another package relies on.
- Skip self-describing fields: `Name`, `CreatedAt`, `UpdatedAt`, and similar
  need no comment, and adding one is noise.
- If the fact is about the whole type rather than one field (e.g. "versions
  are immutable checkpoints"), put it in the type's doc comment instead.
- Staleness test: if an app or store method could change while the field's
  domain meaning stays the same, and that change would falsify the comment,
  the comment is describing behavior - move it to the method or delete it.
  ("Resend returns an invitation to pending" fails this test; "pending is the
  initial state" passes.)
- When a comment would just restate the name, either delete the comment or
  realize the field needs a better name.
