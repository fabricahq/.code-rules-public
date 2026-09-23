---
title: "Avoid Snapshot Tests"
whenToRead: "Before choosing or reviewing a snapshot test for TypeScript application behavior or rendered output."
impact: "MEDIUM"
impactDescription: "avoids fragile broad snapshots that encourage updating outputs without understanding behavior"
tags: "typescript, testing, snapshots, assertions, maintenance"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Avoid Snapshot Tests

Snapshot tests are discouraged to avoid fragility, which leads to a "just update it" mindset to make all tests pass.
Exceptions can be made, with strong rationale behind them, where test output has short and clear intent about what's actually being tested (e.g., design system library critical elements that shouldn't deviate).
