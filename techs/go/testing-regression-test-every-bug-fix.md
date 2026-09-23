---
title: "Land Every Bug Fix With a Failing-First Regression Test"
whenToRead: "Before diagnosing or fixing a reproducible Go bug and choosing a test that demonstrates it."
impact: "HIGH"
impactDescription: "turns each escaped bug into a permanent guard so the same regression cannot ship twice"
tags: "go, testing, regression, bug-fix, reproduce, tdd"
---

## Land Every Bug Fix With a Failing-First Regression Test

A bug that reached a human is proof of a missing test. Before fixing it,
write a test at the lowest layer that reproduces the failure, run it, and
watch it fail for the reported reason. Then fix the bug and keep the test.
Fixing without a regression test leaves the door open for the same bug to
return in a later refactor - and verifying the test fails first proves the
test actually covers the bug rather than passing vacuously.

**Incorrect:**

```go
// Fix lands alone: the off-by-one is corrected, but nothing stops a future
// refactor from reintroducing it.
func latestVersionNumber(versions []DocumentVersion) int {
	if len(versions) == 0 {
		return 0
	}
	return versions[len(versions)-1].Number // was versions[len(versions)-2]
}
```

**Correct:**

```go
// The reproduction lands with the fix, named for the behavior it guards.
func TestLatestVersionNumberUsesFinalVersion(t *testing.T) {
	versions := []DocumentVersion{{Number: 1}, {Number: 2}, {Number: 3}}

	if got := latestVersionNumber(versions); got != 3 {
		t.Fatalf("latest version = %d, want 3", got)
	}
}

func TestLatestVersionNumberZeroWhenNoVersions(t *testing.T) {
	if got := latestVersionNumber(nil); got != 0 {
		t.Fatalf("latest version = %d, want 0", got)
	}
}
```

**Guidelines:**

- Reproduce at the lowest layer that exhibits the bug: domain test for a
  logic bug, store test for a persistence bug, transport test only when the
  bug lives in hand-written transport code.
- Name the test for the behavior it guards, not the incident
  (`TestLatestVersionNumberUsesFinalVersion`, not `TestFixIssue123`).
- Run the test before applying the fix and confirm it fails with the
  reported symptom; a regression test that never failed proves nothing.
- If the bug spans layers and only an end-to-end flow exhibits it, add the
  reproduction to the Playwright suite instead - but first check whether an
  extracted unit seam could express it more cheaply.
