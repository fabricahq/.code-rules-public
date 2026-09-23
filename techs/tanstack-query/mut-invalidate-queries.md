---
title: "Invalidate or update every query a mutation changes"
whenToRead: "Before planning, writing, changing, or reviewing a TanStack Query mutation, or diagnosing UI that shows outdated data after a save."
impact: "HIGH"
impactDescription: "Cached queries that a mutation changed but did not invalidate keep showing outdated data until something else refetches them."
tags: "tanstack-query, mutations, invalidation, cache"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/mut-invalidate-queries.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule mut-invalidate-queries (MIT, notice retained in NOTICE.md): merged the targeted-invalidation rule, restructured to the rule template, and corrected when invalidation refetches."
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/cache-invalidation.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule cache-invalidation (MIT, notice retained in NOTICE.md): merged the targeted-invalidation rule, restructured to the rule template, and corrected when invalidation refetches."
---

## Invalidate or update every query a mutation changes

After a mutation succeeds, invalidate every cached query whose data it may have changed, or write the server's response into the cache when it contains the complete new value.
Use the narrowest key prefix that still covers every affected query.

### Implementation

- List what the mutation changes: the entity itself, lists and filtered views that contain it, counts and summaries, and related entities.
- Invalidate them in `onSuccess`, or in `onSettled` when an optimistic update must be reconciled after failure too.
- Return or await the `invalidateQueries` promise, so the mutation stays pending until the refetch finishes and the UI does not flash outdated data.
- When the response contains the full updated entity, write it with `setQueryData` for that entity's key, and invalidate lists and aggregates that may also have changed.
- Prefer a prefix that covers what changed, such as `todoQueries.lists()`.
  When unsure, invalidate a slightly broader prefix; an extra refetch of an active query costs less than outdated data.
- Do not call `invalidateQueries()` with no filter; it refetches every active query in the app.

### Rationale

Invalidation marks matching queries stale and immediately refetches the active ones, the queries currently used by a mounted component.
Inactive queries refetch the next time a component uses them.
A query left out keeps its cached value, so the UI contradicts what the user just saved.

### Examples

**Incorrect (counterexample):**

```tsx
const deleteTodo = useMutation({
  mutationFn: (todoId: number) => api.deleteTodo(todoId),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['todos', 'list'] });
  },
});
```

The todo count shown in the header, cached under `['todos', 'count']`, still includes the deleted todo.

**Correct:**

```tsx
const deleteTodo = useMutation({
  mutationFn: (todoId: number) => api.deleteTodo(todoId),
  onSuccess: (_data, todoId) => {
    queryClient.removeQueries({ queryKey: todoQueries.detail(todoId).queryKey });
    return queryClient.invalidateQueries({ queryKey: todoQueries.all() });
  },
});
```

`todoQueries` is the entity's query options factory.
The deleted todo's detail entry is removed, every list and count under `['todos']` refetches, and the mutation stays pending until they do.

### Validation

For each mutation, list the screens that display data it changes, and check that each of their query keys is invalidated or updated.
After running the mutation in the app, check that every such screen shows the new data without a manual reload.

Updating the cache directly from a complete server response instead of invalidating is not a violation.
