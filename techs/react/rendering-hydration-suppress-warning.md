---
title: "Suppress only expected hydration mismatches"
whenToRead: "Before writing, changing, reviewing, or diagnosing server-rendered React output that intentionally differs between server and client, such as timestamps or locale-formatted text, or when a hydration warning appears."
impact: "LOW-MEDIUM"
impactDescription: "Unexplained hydration warnings hide real mismatches, while suppressing them broadly hides real bugs."
tags: "react, ssr, hydration"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-hydration-suppress-warning.md
    description: "Adapted from the Vercel Agent Skills rule rendering-hydration-suppress-warning: restructured to the rule template, added the one-level scope and two-pass alternative."
---

## Suppress only expected hydration mismatches

When an element's text or attribute intentionally differs between server and client, add `suppressHydrationWarning` to that element only.
Fix every other mismatch at its source.

### Implementation

- Use `suppressHydrationWarning` for values that cannot match, such as the current time or the client's time zone.
- Put it on the element whose own text or attributes differ; it applies only one level deep, not to descendants.
- React does not patch suppressed text, so the server value stays until the component re-renders.
  When the client value must appear, render it on the client after hydration, such as with a state flag set in an Effect.
- Do not use it to silence mismatches caused by bugs, such as reading `window` or random values during render.

### Rationale

Hydration expects the client's first render to match the server HTML, and it warns when they differ because a mismatch usually means a bug.
Some differences are inherent, and suppressing those keeps the warning meaningful for the rest.

### Examples

**Incorrect (counterexample):**

```tsx
function Timestamp() {
  return <span>{new Date().toLocaleString()}</span>;
}
```

The server and client format different times, so every page load warns.

**Correct:**

```tsx
function Timestamp() {
  return <span suppressHydrationWarning>{new Date().toLocaleString()}</span>;
}
```

### Validation

For each `suppressHydrationWarning`, check that the difference is inherent to the value, not a bug, and that it sits on the element whose own content differs.

A suppression on a timestamp or locale-formatted value is not a violation.
