---
title: "Use Boolean() for Explicit Boolean Coercion"
whenToRead: "Before writing or reviewing TypeScript code that intentionally coerces a value to boolean."
impact: "MEDIUM"
impactDescription: "makes intentional truthiness conversion searchable and distinguishes coercion from type narrowing"
tags: "typescript, boolean, coercion, truthiness, narrowing, readability"
---

## Use Boolean() for Explicit Boolean Coercion

When code intentionally converts a value to a boolean, use `Boolean(value)`.
Avoid `!!value`; it is terse but less searchable and less explicit for readers
who do not already know the idiom.

**Incorrect (implicit-looking double negation):**

```ts
const hasAccount = !!accountContext;
```

**Correct (explicit coercion):**

```ts
const hasAccount = Boolean(accountContext);
```

**Prefer guards when narrowing matters:**

```ts
const canViewDocument = accountContext !== undefined && document.allowedAccountIds.includes(accountContext.id);
```

`Boolean(value)` is for producing a boolean value from truthiness. It does not
narrow the original variable's type for later code. When the goal is to prove a
value is present, compare against the specific absent value (`undefined`,
`null`, or both) so TypeScript can narrow the type and the reader can see which
cases are intentionally excluded.

Do not replace existing comparisons with `Boolean(...)` when the comparison is
carrying domain meaning. For example, `count > 0`, `name.trim().length > 0`, and
`status === "ready"` are clearer than truthiness coercion because they say which
condition matters.
