---
title: "Use Generic Array Types"
whenToRead: "Before choosing array type syntax for new TypeScript declarations."
impact: "LOW"
impactDescription: "keeps mutable and readonly array annotations in one consistent syntax"
tags: "typescript, arrays, readonlyarray, style"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Use Generic Array Types

**Related automated rule:** Array types should be defined using generic syntax [Reference](https://typescript-eslint.io/rules/array-type/#generic)

```js
'@typescript-eslint/array-type': ['error', { default: 'generic' }]
```
**Note:**

Since there is no functional difference between the 'generic' and 'array' definitions, feel free to choose the one
  that your team finds most readable.

```ts
// Avoid
const x: string[] = ['foo', 'bar'];
const y: readonly string[] = ['foo', 'bar'];

// Use
const x: Array<string> = ['foo', 'bar'];
const y: ReadonlyArray<string> = ['foo', 'bar'];
```
