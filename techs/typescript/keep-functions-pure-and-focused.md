---
title: "Keep Functions Pure and Focused"
whenToRead: "Before writing or reviewing a TypeScript data transformation or function with several responsibilities."
impact: "MEDIUM"
impactDescription: "makes behavior easier to test, refactor, and reason about from inputs and outputs"
tags: "typescript, functions, purity, single-responsibility, testing"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Keep Functions Pure and Focused

Give a data transformation one coherent responsibility and make its result
depend on explicit inputs. A pure transformation returns data without mutating
its inputs, reading hidden mutable state, or causing external effects. That
makes it straightforward to exercise with representative values and edge cases.

Keep effects at explicit boundaries such as network requests, storage, and UI
events. Those operations cannot all be pure, and a zero-argument function may
still be appropriate. The useful separation is between a computation that can
be pure and the effectful operation that calls it.

**Incorrect:** a formatting helper reads a global locale variable and mutates
its caller's array before returning labels. Its output depends on hidden state
and changes data its name does not promise to change.

**Correct:** accept the locale and a readonly array, then return a new array of
labels. The caller chooses the locale and owns any later side effect.
