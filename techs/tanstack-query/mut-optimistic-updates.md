---
title: "Make optimistic updates reversible, and decide them once"
whenToRead: "Before planning, writing, changing, or reviewing a TanStack Query mutation that shows its result before the server confirms it, or whose onMutate, onError, and onSettled callbacks share decisions or derived values."
impact: "MEDIUM-HIGH"
impactDescription: "An optimistic update without cancellation, rollback, and a final refetch can be overwritten by stale responses or leave the UI showing a change the server rejected."
tags: "tanstack-query, mutations, optimistic-updates, rollback"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/mut-optimistic-updates.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule mut-optimistic-updates (MIT, notice retained in NOTICE.md): merged with the Fabrica rule on deriving mutation decisions once, reframed from always-optimistic to how to do it safely, restructured to the rule template, and made cache updaters handle missing data."
---

## Make optimistic updates reversible, and decide them once

When a mutation updates the UI before the server responds, cancel in-flight queries for the affected keys, snapshot their data, apply the update, roll back on error, and invalidate when the mutation settles.
Decide in `onMutate` whether the optimistic change applies, and read that decision in later callbacks instead of recomputing it.

### Implementation

- Choose the approach by where the change appears:
  - **Only in the component that triggers the mutation:** render the pending `variables` from `useMutation` while `isPending`, without touching the cache.
  - **In several places:** update the cache in `onMutate`.
- For cache updates, in `onMutate`:
  1. Await `cancelQueries` for the affected keys, so an in-flight fetch cannot overwrite the optimistic value.
  2. Snapshot the current data with `getQueryData`.
  3. Write the optimistic value with `setQueryData`, handling the case where no data is cached yet.
  4. Return the decision, the snapshot, and any derived values.
- In `onError`, restore the snapshot when the update was applied.
- In `onSettled`, invalidate the affected keys and return the promise, so the cache matches the server whether the mutation succeeded or failed.
- In TanStack Query v5, the value returned from `onMutate` reaches later callbacks as `onMutateResult`: the third argument of `onError` and `onSuccess`, and the fourth of `onSettled`.
  The final argument is a separate `MutationFunctionContext`.
- Return a discriminated result, such as `{ applied: false } | { applied: true; previous: Todo | undefined }`, and branch on it in later callbacks.
- `onMutate` cannot cancel the mutation; the request still runs.
  To prevent it, check before calling `mutate` or inside `mutationFn`.
- Skip optimistic updates when the server's result is hard to predict, such as when it assigns values the client cannot know.

### Rationale

An optimistic update shows a result the server has not confirmed.
A refetch already in flight can resolve after the optimistic write and overwrite it, so the change seems to disappear.
If the server rejects the change, the UI must return to the real state.
Deriving the "does this apply?" decision separately in each callback lets rollback and invalidation disagree with the original write.

### Examples

#### Application: A cache update used in several places

**Incorrect (counterexample):**

```tsx
const toggleTodo = useMutation({
  mutationFn: toggleTodoComplete,
  onMutate: (todoId: number) => {
    queryClient.setQueryData<Array<Todo>>(['todos'], (old) =>
      old?.map((todo) => (todo.id === todoId ? { ...todo, completed: !todo.completed } : todo)),
    );
  },
});
```

A refetch in flight can overwrite the toggle, a failure leaves the wrong state on screen, and nothing resynchronizes with the server.

**Correct:**

```tsx
const toggleTodo = useMutation({
  mutationFn: toggleTodoComplete,
  onMutate: async (todoId: number) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] });
    const previous = queryClient.getQueryData<Array<Todo>>(['todos']);
    queryClient.setQueryData<Array<Todo>>(['todos'], (old) =>
      old?.map((todo) => (todo.id === todoId ? { ...todo, completed: !todo.completed } : todo)),
    );
    return { previous };
  },
  onError: (_error, _todoId, onMutateResult) => {
    queryClient.setQueryData(['todos'], onMutateResult?.previous);
  },
  onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
});
```

#### Application: A decision shared by several callbacks

**Incorrect (counterexample):**

```tsx
onMutate: async ({ id, patch }) => {
  const title = normalizedTitle(patch);
  if (!title) return;
  // ...apply the optimistic title and return the snapshot
},
onError: (_error, { patch }, onMutateResult) => {
  if (!normalizedTitle(patch) || !onMutateResult) return;
  queryClient.setQueryData(todoKey, onMutateResult.previous);
},
onSettled: (_data, _error, { patch }) => {
  if (!normalizedTitle(patch)) return;
  return queryClient.invalidateQueries({ queryKey: todoKey });
},
```

The same decision is recomputed in three places, and any difference between the copies makes rollback or invalidation disagree with the write.

**Correct:**

```tsx
type RenameResult = { applied: false } | { applied: true; previous: Todo | undefined };

onMutate: async ({ patch }): Promise<RenameResult> => {
  const title = normalizedTitle(patch);
  if (!title) return { applied: false };
  await queryClient.cancelQueries({ queryKey: todoKey });
  const previous = queryClient.getQueryData<Todo>(todoKey);
  queryClient.setQueryData<Todo>(todoKey, (todo) => (todo ? { ...todo, title } : todo));
  return { applied: true, previous };
},
onError: (_error, _variables, onMutateResult) => {
  if (onMutateResult?.applied) queryClient.setQueryData(todoKey, onMutateResult.previous);
},
onSettled: (_data, _error, _variables, onMutateResult) => {
  if (onMutateResult?.applied) return queryClient.invalidateQueries({ queryKey: todoKey });
},
```

`todoKey` is defined once in the hook body, and later callbacks read the decision from `onMutateResult`.

### Validation

Make the mutation fail, such as by blocking the request in the browser, and check that the UI returns to the previous state.
Trigger a refetch while the mutation is pending and check that the optimistic value is not overwritten.
Check that later callbacks read `onMutateResult` rather than re-deriving decisions from the variables.

A mutation without an optimistic update is not a violation of this rule.
