---
title: "Cover empty inputs and boundaries"
whenToRead: "When adding or changing collection processing, thresholds, ranges, or relationships between items."
impact: "MEDIUM"
impactDescription: "Catches failures hidden by tests that exercise only ordinary inputs."
tags: "testing"
attribution: [{"url": "https://github.com/josh-padnick/code-rules/blob/0621607fae1ed732a2ec90d9bbe906bc5a4ecf78/typescript/testing-cover-degenerate-and-boundary-cases.md", "description": "Adapted for public reuse: added reading guidance, simplified examples, and removed repository-specific assumptions."}]
---

## Cover empty inputs and boundaries

Test the inputs that take distinct branches: empty and single-item collections, first and last positions, exact thresholds, and an item related to itself. State the intended result for each case rather than merely asserting that it does not crash.

**Incomplete:** a function accepts retry counts from one through three, but tests cover only two.

**Complete:** cover zero, one, three, and four, asserting the documented acceptance or error for each. Add the ordinary case when it exercises different behavior.

For a relationship such as “is this folder inside another folder,” include the same folder on both sides and an absent parent. For collection transformations, include empty and single-item inputs.

### Validation

List the branch boundaries in the implementation or contract and match each to a test. Add cases for distinct behavior, not every possible input. Keep a discovered edge-case bug as a permanent regression test.
