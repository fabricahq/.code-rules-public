---
title: "Memoize deliberately"
whenToRead: "Before writing, changing, or reviewing useMemo, useCallback, or memo in React code, or diagnosing unnecessary re-renders or slow renders, in projects that do not use React Compiler."
impact: "MEDIUM"
impactDescription: "Memoization in the wrong place costs more than it saves, and small mistakes silently disable the memoization that matters."
tags: "react, memo, useMemo, performance"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-memo.md
    description: "Adapted from the Vercel Agent Skills rule rerender-memo: merged four memoization rules into one rule with applications, restructured to the rule template, and scoped it to projects without React Compiler."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-memo-with-default-value.md
    description: "Adapted from the Vercel Agent Skills rule rerender-memo-with-default-value: merged four memoization rules into one rule with applications, restructured to the rule template, and scoped it to projects without React Compiler."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-simple-expression-in-memo.md
    description: "Adapted from the Vercel Agent Skills rule rerender-simple-expression-in-memo: merged four memoization rules into one rule with applications, restructured to the rule template, and scoped it to projects without React Compiler."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-split-combined-hooks.md
    description: "Adapted from the Vercel Agent Skills rule rerender-split-combined-hooks: merged four memoization rules into one rule with applications, restructured to the rule template, and scoped it to projects without React Compiler."
---

## Memoize deliberately

Use `useMemo`, `useCallback`, and `memo` where measurement shows expensive work or wasted re-renders, and structure the code so that memoization actually takes effect.

### Implementation

- Do not memoize cheap expressions with primitive results, such as `a || b` or `count * 2`; the Hook's bookkeeping costs more than the expression.
- Give each memoized computation only the dependencies it uses.
  Split a `useMemo` or `useEffect` that combines independent work with different dependencies.
- Keep the props of a `memo` component referentially stable.
  Define default values for object, array, and function props as module-level constants rather than inline defaults.
- To skip expensive work when an early return makes it unnecessary, move the work into a child component and render the child only when needed.
- When the project uses React Compiler, let it handle memoization and do not add manual memoization for performance.

### Rationale

Memoization trades memory and comparison work for skipped computation.
It pays off only when the skipped work is expensive and the dependencies rarely change.
A new object or function created on every render, such as an inline default prop, changes a dependency every time and quietly disables the memoization.

### Examples

#### Application: A cheap expression

**Incorrect (counterexample):**

```tsx
const isLoading = useMemo(() => user.isLoading || notifications.isLoading, [user.isLoading, notifications.isLoading]);
```

**Correct:**

```tsx
const isLoading = user.isLoading || notifications.isLoading;
```

#### Application: A default prop on a memoized component

**Incorrect (counterexample):**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: { onClick?: () => void }) {
  // ...
});
```

When callers omit `onClick`, each render creates a new default function, so `memo` never skips a render.

**Correct:**

```tsx
const noop = () => {};

const UserAvatar = memo(function UserAvatar({ onClick = noop }: { onClick?: () => void }) {
  // ...
});
```

#### Application: Independent work in one Hook

**Incorrect (counterexample):**

```tsx
const sortedProducts = useMemo(() => {
  const filtered = products.filter((product) => product.category === category);
  return filtered.toSorted((a, b) => (sortOrder === 'asc' ? a.price - b.price : b.price - a.price));
}, [products, category, sortOrder]);
```

Changing the sort order also repeats the filtering.

**Correct:**

```tsx
const filteredProducts = useMemo(
  () => products.filter((product) => product.category === category),
  [products, category],
);

const sortedProducts = useMemo(
  () => filteredProducts.toSorted((a, b) => (sortOrder === 'asc' ? a.price - b.price : b.price - a.price)),
  [filteredProducts, sortOrder],
);
```

### Validation

Profile with the React DevTools Profiler before and after adding memoization, and keep it only where it reduces render time or re-renders.
Check that props passed to `memo` components do not change identity on every render.

Missing memoization in a project that uses React Compiler is not a violation.
