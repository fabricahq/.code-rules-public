---
title: "Test observable behavior"
whenToRead: "When designing or reviewing automated tests for application behavior."
impact: "HIGH"
impactDescription: "Keeps tests useful during refactoring and focused on outcomes users depend on."
tags: "testing"
attribution: [{"url":"https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx","description":"Underlying TypeScript Style Guide material by mkosir, adapted under MIT; copyright and permission notice retained in NOTICE.md."}]
---

## Test observable behavior

Test the behavior exposed to callers or users rather than the private steps used to implement it. Arrange a controlled starting state, perform the behavior, and assert the relevant result.

Keep each test independent of execution order and other tests' data. Use stable user-facing selectors for UI tests. Control external services at the boundary so tests can run reliably without depending on another organization's live service.

**Incorrect:** assert that a checkout function calls a private `calculateTotal` helper exactly once. Renaming or inlining the helper breaks the test even if checkout remains correct.

**Correct:** give checkout two items and a discount, then assert the charged total and the returned receipt. Assert an external call when that interaction is itself part of the contract, such as charging only once.

Do not add assertions just to raise coverage or retest a framework. Several assertions are appropriate when they jointly establish one behavior.

### Validation

Ask what incorrect user-visible result the test would catch. Refactoring private helpers while preserving behavior should leave the test valid. Run the test alone and with the suite to check isolation.
