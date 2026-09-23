---
title: "Use Clear should-when Test Descriptions"
whenToRead: "Before naming a TypeScript test for expected behavior under a particular condition."
impact: "LOW"
impactDescription: "makes test intent and triggering condition visible from the title"
tags: "typescript, testing, vitest, test-names, should-when, readability"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Use Clear should-when Test Descriptions

All test descriptions must follow naming convention as `it('should ... when ...')`.

**Related automated rule:** [Reference](https://github.com/vitest-dev/eslint-plugin-vitest/blob/main/docs/rules/valid-title.md#mustmatch)

```js
'vitest/valid-title': [
    'error',
    {
      mustMatch: { it: [/should.*when/u.source, "Test title must include 'should' and 'when'"] },
    },
  ]
```

```ts
// Avoid
it('accepts ISO date format where date is parsed and formatted as YYYY-MM');
it('after title is confirmed user description is rendered');

// Name test description as it('should ... when ...')
it('should return parsed date as YYYY-MM when input is in ISO date format');
it('should render user description when title is confirmed');
```
