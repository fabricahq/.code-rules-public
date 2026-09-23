---
title: "Use a boolean condition for conditional rendering"
whenToRead: "Before writing, changing, or reviewing JSX that renders content with `&&` based on a number, string, or other value that is not already a boolean."
impact: "LOW-MEDIUM"
impactDescription: "A falsy number such as 0 renders as visible text instead of nothing."
tags: "react, jsx, rendering"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-conditional-render.md
    description: "Adapted from the Vercel Agent Skills rule rendering-conditional-render: restructured to the rule template with a rationale and validation."
---

## Use a boolean condition for conditional rendering

When the left side of `&&` in JSX is not a boolean, turn it into one, such as `count > 0`, or use a ternary that returns `null`.

### Implementation

- Compare numbers explicitly, such as `items.length > 0` instead of `items.length`.
- Convert other values with an explicit check, such as `name !== ''`, or with `Boolean(value)` when truthiness is the intended test.
- `&&` with a value that is already a boolean, such as `isOpen && <Menu />`, is fine.

### Rationale

`a && b` evaluates to `a` when `a` is falsy.
React renders `false`, `null`, and `undefined` as nothing, but it renders `0` and `NaN` as text, so a count of zero shows a stray "0".

### Examples

**Incorrect (counterexample):**

```tsx
function Badge({ count }: { count: number }) {
  return <div>{count && <span className="badge">{count}</span>}</div>;
}
```

When `count` is `0`, the component renders `<div>0</div>`.

**Correct:**

```tsx
function Badge({ count }: { count: number }) {
  return <div>{count > 0 ? <span className="badge">{count}</span> : null}</div>;
}
```

### Validation

Check each `&&` in JSX whose left side has a `number`, `string`, or union type that includes them.
A lint rule that flags non-boolean left operands in JSX can automate this.

`&&` with a boolean left side is not a violation.
