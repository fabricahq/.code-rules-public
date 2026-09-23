---
title: "Derive component views of query data with a stable select"
whenToRead: "Before writing, changing, or reviewing components that filter, sort, pick fields from, or compute values from TanStack Query data, or diagnosing components that re-render on unrelated cache updates."
impact: "LOW-MEDIUM"
impactDescription: "Components that read whole query results re-render whenever any part of the data changes, and inline selectors repeat their work on every render."
tags: "tanstack-query, select, rerender, performance"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/perf-select-transform.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule perf-select-transform (MIT, notice retained in NOTICE.md): restructured to the rule template and corrected the claim that select always memoizes: it reuses results only when the data and the selector reference are unchanged."
---

## Derive component views of query data with a stable select

When a component needs only part of a query's data, or a value derived from it, compute it with the query's `select` option, and keep the selector's reference stable.

### Implementation

- Use `select` to filter, sort, pick an item, or compute a summary; the component re-renders only when the selected result changes.
- Define selectors that do not depend on props at module level, or in the query options factory.
- Wrap selectors that depend on props or state in `useCallback`, so the reference changes only when those inputs do.
- An inline arrow selector works, but it runs again on every render because its reference changes; that is fine for cheap selections.
- Keep the cached data in the server's shape; `select` shapes it for one consumer without changing what other consumers see.

### Rationale

`select` runs on the cached data and returns a structurally shared result, so a component that selects `completedCount` does not re-render when an unrelated todo's title changes.
TanStack Query reuses the previous result only when both the data and the selector function are unchanged; a new function on every render repeats the work.

### Examples

**Incorrect (counterexample):**

```tsx
function CompletedCount() {
  const { data: todos } = useQuery(todoQueries.list());
  const completedCount = todos?.filter((todo) => todo.completed).length ?? 0;
  return <span>{completedCount}</span>;
}
```

The component re-renders on every change to any todo, even when the count stays the same.

**Correct:**

```tsx
const selectCompletedCount = (todos: ReadonlyArray<Todo>) => todos.filter((todo) => todo.completed).length;

function CompletedCount() {
  const { data: completedCount = 0 } = useQuery({ ...todoQueries.list(), select: selectCompletedCount });
  return <span>{completedCount}</span>;
}
```

The count re-renders the component only when it changes, and the module-level selector is reused across renders.

### Validation

Use the React DevTools Profiler to check that components using `select` re-render only when their selected value changes.
Check that expensive selectors have stable references.

Deriving a cheap value in the component body is not a violation when re-renders are not a problem.
