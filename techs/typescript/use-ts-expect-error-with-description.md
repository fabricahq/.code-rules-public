---
title: "Use ts-expect-error With a Description"
whenToRead: "Before suppressing or reviewing an unavoidable TypeScript compiler error."
impact: "MEDIUM"
impactDescription: "keeps unavoidable TypeScript suppressions explicit and self-invalidating when the error disappears"
tags: "typescript, ts-expect-error, ts-ignore, suppressions, lint"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Use ts-expect-error With a Description

When a TypeScript error cannot be mitigated, use `@ts-expect-error` as a last resort to suppress it.

This directive notifies the compiler when the suppressed error no longer exists, ensuring errors are revisited once they're obsolete, unlike `@ts-ignore`, which can silently linger even after the error is resolved.

- Always use `@ts-expect-error` with a clear description explaining why it is necessary.
- Avoid `@ts-ignore`, as it does not track suppressed errors.

**Related automated rule:** [Reference](https://typescript-eslint.io/rules/ban-ts-comment/#allow-with-description)

```js
'@typescript-eslint/ban-ts-comment': [
  'error',
  {
    'ts-expect-error': 'allow-with-description'
  },
]
```

```ts
// Avoid @ts-ignore as it will do nothing if the following line is error-free.
// @ts-ignore
const newUser = createUser('Gabriel');

// Use @ts-expect-error with description.
// @ts-expect-error: This library function has incorrect type definitions - createUser accepts string as an argument.
const newUser = createUser('Gabriel');
```
