---
title: "Reset query errors when an error boundary retries"
whenToRead: "Before planning, writing, changing, or reviewing React error boundaries around TanStack Query suspense queries or queries with throwOnError, or a retry button for failed data."
impact: "HIGH"
impactDescription: "An error boundary that resets without resetting the query's error state shows the same error again instead of retrying."
tags: "tanstack-query, error-boundaries, suspense, errors"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/err-error-boundaries.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule err-error-boundaries (MIT, notice retained in NOTICE.md): restructured to the rule template, added when suspense queries throw, and removed the router-specific example."
---

## Reset query errors when an error boundary retries

When query errors are shown by a React error boundary, wire the boundary's reset to TanStack Query's error reset, using `QueryErrorResetBoundary` or `useQueryErrorResetBoundary`.

### Implementation

- Pass the `reset` function from `useQueryErrorResetBoundary`, or from a `QueryErrorResetBoundary` render prop, to the error boundary's `onReset`.
- Place boundaries around independent sections so one failure does not replace the whole page.
- Suspense queries throw to the boundary only when there is no cached data; a failed background refetch leaves the old data and sets the query's `error`.
  Show that error inline where it matters.
- For non-suspense queries, errors reach a boundary only with `throwOnError`; otherwise render the query's `error` state inline.
- In a router with its own error component, also reset the query errors before retrying the route.

### Rationale

After a query fails, TanStack Query keeps it in the error state.
Resetting the error boundary re-renders the children, but without a query error reset the suspense query rethrows the cached error instead of fetching again.
The reset boundary marks those queries for a new fetch on the next render.

### Examples

**Incorrect (counterexample):**

```tsx
<ErrorBoundary
  fallbackRender={({ resetErrorBoundary }) => <button onClick={resetErrorBoundary}>Try again</button>}
>
  <Suspense fallback={<Loading />}>
    <Posts />
  </Suspense>
</ErrorBoundary>
```

Clicking the button re-renders `Posts`, which throws the same cached error again.

**Correct:**

```tsx
function QueryErrorBoundary({ children }: { children: ReactNode }) {
  const { reset } = useQueryErrorResetBoundary();

  return (
    <ErrorBoundary
      onReset={reset}
      fallbackRender={({ resetErrorBoundary }) => (
        <div role="alert">
          <p>Could not load this section.</p>
          <button onClick={resetErrorBoundary}>Try again</button>
        </div>
      )}
    >
      {children}
    </ErrorBoundary>
  );
}
```

### Validation

Make a query fail, click retry, and check in the network panel that a new request is sent.

An inline error state for a query that does not throw is not a violation.
