---
title: "Use Discriminated Unions for Function Args"
whenToRead: "Before designing function arguments with mutually exclusive modes and mode-specific fields."
impact: "MEDIUM"
impactDescription: "expresses distinct function call modes without unrelated optional fields"
tags: "typescript, functions, arguments, discriminated-unions, api-design"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Use Discriminated Unions for Function Args

When applicable use **discriminated union type** to eliminate optional properties, which will decrease complexity on function API and only required properties will be passed depending on its use case.

```ts
// Avoid optional properties as they increase complexity and ambiguity in function APIs
type StatusParams = {
  data?: Products;
  title?: string;
  time?: number;
  error?: string;
};

// Prefer required properties. If optional properties are unavoidable,
// use a discriminated union to represent distinct use cases with required properties.
type StatusSuccessParams = {
  status: 'success';
  data: Products;
  title: string;
};

type StatusLoadingParams = {
  status: 'loading';
  time: number;
};

type StatusErrorParams = {
  status: 'error';
  error: string;
};

// Discriminated union 'StatusParams' ensures predictable function arguments with no optional properties
type StatusParams = StatusSuccessParams | StatusLoadingParams | StatusErrorParams;

export const parseStatus = (params: StatusParams) => {...
```
