---
title: "Preserve caller-owned data"
whenToRead: "When transforming arrays or objects received from another caller or shared state."
impact: "MEDIUM"
impactDescription: "Prevents hidden mutation from changing another caller's behavior."
tags: "typescript"
attribution: [{"url":"https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx","description":"Underlying TypeScript Style Guide material by mkosir, adapted under MIT; copyright and permission notice retained in NOTICE.md."}]
---

## Preserve caller-owned data

Prefer readonly inputs and return new values when transforming data owned by a caller. Do not silently mutate shared inputs.

**Incorrect:** removing an item changes the caller's array.

```ts
function withoutFirst(values: Array<string>): Array<string> {
  values.splice(0, 1);
  return values;
}
```

**Correct:** the input contract is readonly and the result is a separate array.

```ts
function withoutFirst(values: ReadonlyArray<string>): Array<string> {
  return values.slice(1);
}
```

Readonly types and shallow copies do not make nested objects immutable. When changing nested data, copy the affected structure or use the project's ownership convention. Mutation is appropriate for newly owned local data or an explicitly mutating API whose callers understand the contract.

### Validation

Test that the original input remains unchanged and the returned value contains the intended transformation. Check nested references when a change reaches nested data. Do not demand a deep clone when no nested mutation occurs.
