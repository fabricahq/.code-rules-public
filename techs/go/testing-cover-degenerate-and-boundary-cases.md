---
title: "Cover the Degenerate and Boundary Cases"
whenToRead: "Before writing or reviewing Go tests for collections, positions, thresholds, or relationships between items."
impact: "MEDIUM"
impactDescription: "collection, positional, and relational logic breaks at the edges, so a suite that only drives the typical case ships empty, single-element, boundary, and self-referential bugs"
tags: "go, testing, edge-cases, boundary, degenerate, empty, single, off-by-one, self-referential, collections"
---

## Cover the Degenerate and Boundary Cases

Bugs in code that walks a collection, computes a position, or relates two items
cluster at the edges, not in the comfortable middle. The empty collection, the
single element, the first and last slot, the exact threshold, and the item
compared against itself each take a different path through the logic. A suite
that only exercises "a few items, somewhere in the middle" is not *wrong* - it
passes and tests real behavior - it is *incomplete*: the edge paths go
unexercised, and that is exactly where the bugs are. When you test such an
operation, enumerate the degenerate inputs as deliberately as the happy path.

The contrast below is not bad-code-versus-good-code; it is the same legitimate
test, first on its own and then with the missing cases added.

The document tree move planner is the cautionary example: reordering three
siblings was tested, but moving the only document in a bucket (the source
empties), dropping into an empty folder (the destination starts empty), and
dropping an item onto itself (the item is removed from its own bucket before the
target is located, so the target lookup misses) were not - and the self-drop
path shipped a confusing "target not in bucket" error that nothing caught.

**Incomplete** - passes, but only proves the typical case:

```go
// A legitimate, passing test. It just never reaches the empty, single-element,
// or self-referential paths the planner branches on.
func TestMoveReordersSibling(t *testing.T) {
	folder := seedDocuments(t, "A", "B", "C")
	moveBefore(t, folder, "C", "B") // C lands between A and B

	assertOrder(t, folder, "A", "C", "B")
}
```

**Complete** - the same test kept, plus the edges where the logic branches:

```go
func TestMoveReordersSibling(t *testing.T)                  { /* the typical N-item case */ }
func TestMoveSingleDocumentIntoEmptyFolder(t *testing.T)    { /* source empties, dest starts empty */ }
func TestMoveRejectsDocumentDroppedOnItself(t *testing.T)   { /* item == target: removed from its own bucket */ }
func TestMovePlacesAtFirstAndLastSlot(t *testing.T)         { /* both boundary positions */ }
```

**Guidelines:**

- For an operation over a collection, cover **zero elements** and **one
  element**, not just "several." Empty often means "append to nothing" or
  "nothing to renumber"; a single element collapses a loop body that two-plus
  elements exercise.
- For **positional** logic (insert before/after, clamp, page or zone
  boundaries), test the operation at the **first and last slot** and at the
  **exact threshold value**, not just clearly-inside values - that is where a
  `<` vs `<=` mistake hides.
- For an operation that **relates two items** (move A relative to B, merge A
  into B, link A to B), test the **identity case** A == B. It frequently takes a
  separate path - here the moved item is excluded from its own sibling bucket,
  so a naive self-target fails late and obscurely. Guard it and assert the
  guard.
- Degenerate inputs tend to reveal one of three things: a crash, a
  misleading-but-not-wrong error, or a silently wrong result. Assert the
  *intended* behavior explicitly so the path stays pinned.
- This rule is about **which inputs** to cover. Choose the lowest test layer that faithfully reproduces each behavior, and keep every discovered edge-case bug as a regression test.
