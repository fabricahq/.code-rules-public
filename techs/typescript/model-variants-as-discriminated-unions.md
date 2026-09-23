---
title: "Model distinct states as discriminated unions"
whenToRead: "When a TypeScript value has variants with different required fields."
impact: "MEDIUM"
impactDescription: "Makes impossible field combinations harder to construct and missing cases easier to detect."
tags: "typescript"
attribution: [{"url": "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx", "description": "Underlying TypeScript Style Guide material by mkosir, adapted under MIT; copyright and permission notice retained in NOTICE.md."}]
---

## Model distinct states as discriminated unions

Represent mutually exclusive states as a union with a shared literal discriminator. Keep each state's required data in its own variant rather than making all fields optional.

**Incorrect:** this permits a successful result without data, or both data and an error.

```ts
type Result = { success: boolean; data?: string; error?: string };
```

**Correct:** each state has exactly the fields its contract requires.

```ts
type Result =
  | { kind: 'success'; data: string }
  | { kind: 'failure'; error: string };
```

Narrow on `kind` before accessing variant-specific fields. For a switch that must handle every variant, use an exhaustive check or the project's exhaustive-switch lint rule. A truly independent on/off option can remain a boolean; it does not need a new state model.

### Validation

Try constructing a success without data and a failure without an error: the compiler should reject both. Add a new variant and verify that consumers requiring exhaustive handling report the missing case.
