---
title: "Name Non-Trivial Hook Callbacks"
whenToRead: "Before passing nontrivial callbacks to React hooks such as useMemo or useCallback."
impact: "MEDIUM"
impactDescription: "named hook callbacks make component logic easier to scan, debug, and extract"
tags: "react, hooks, useMemo, useCallback, naming, readability, custom-hooks, maintainability"
---

## Name Non-Trivial Hook Callbacks

When passing a non-trivial function to a React hook, prefer a named function
expression over an anonymous arrow. The name documents the work at the call
site, improves stack traces, and makes it easier to see when the behavior has
earned its own custom hook.

This applies to derivation and callback hooks such as `useMemo`, `useCallback`,
and library hooks that accept lifecycle or derivation callbacks. `useEffect`
is stricter: give every effect callback a name, even when the effect is short.

**Incorrect (anonymous non-trivial callback):**

```tsx
const visibleRows = useMemo(() => {
  const activeRows = rows.filter((row) => row.status !== "archived");
  return activeRows.toSorted((a, b) => a.name.localeCompare(b.name));
}, [rows]);
```

**Correct (named callback):**

```tsx
const visibleRows = useMemo(function deriveVisibleRows() {
  const activeRows = rows.filter((row) => row.status !== "archived");
  return activeRows.toSorted((a, b) => a.name.localeCompare(b.name));
}, [rows]);
```

**Escalate to a custom hook when the behavior grows its own shape.** Move the
hook and its companion logic into a `useX` hook named for the behavior it owns,
keeping the inner hook callback named:

```tsx
function useVisibleRows(rows: Row[]) {
  return useMemo(function deriveVisibleRows() {
    const activeRows = rows.filter((row) => row.status !== "archived");
    return activeRows.toSorted((a, b) => a.name.localeCompare(b.name));
  }, [rows]);
}
```

**Guidelines:**

- Tiny one-expression callbacks can stay anonymous, except for `useEffect`.
- Name callbacks verb-first for the job they do (`deriveVisibleRows`,
  `buildColumnIndex`, `createSubmitHandler`), not for the dependency that
  changed.
- Extract to a custom hook when the callback gains companion state, refs,
  branching, cleanup, helper functions, or reuse pressure.
- Name the custom hook for the behavior it encapsulates (`useVisibleRows`), not
  for the hook mechanic (`useMemoRows`), and keep any inner non-trivial callback
  named too.
- Do not hide simple local logic inside a hook just to shorten a component. The
  extracted hook should own a coherent behavior that a caller can understand and
  test independently.
