---
title: "Derive Mutation Decisions Once, Then Read Them From `onMutateResult`"
whenToRead: "Before implementing a TanStack Query mutation whose onMutate, onError, or onSettled callbacks share optimistic-update decisions or derived values."
impact: "MEDIUM"
impactDescription: "stops onMutate/onError/onSettled from recomputing the same decision and drifting apart"
tags: "tanstack-query, mutations, optimistic-updates, onMutate, onMutateResult, rollback, readability"
---

## Derive Mutation Decisions Once, Then Read Them From `onMutateResult`

A mutation's `onMutate`, `onError`, and `onSettled` callbacks run at different
times but often need the same facts: whether the optimistic/cache side effects
should apply, a derived value, or the query keys involved. Computing those facts
separately in each callback duplicates the logic three ways and lets the copies
drift - for example, rollback and invalidation deciding "should this apply?"
differently from the optimistic write.

Decide once in `onMutate`, return the decision (plus rollback snapshots and any
derived values) as the `onMutate` result, and have `onError`/`onSettled` branch
on that result instead of re-deriving from the variables. Hoist values that
depend only on stable hook inputs - query keys, predicates - to the hook body so
every callback references one definition.

In TanStack Query v5, the value you return from `onMutate` is passed to the later
callbacks as the **`onMutateResult`** argument: the third argument of
`onError(error, variables, onMutateResult, context)` and the fourth of
`onSettled(data, error, variables, onMutateResult, context)`. It is **not** the
final argument - v5 appends a trailing `MutationFunctionContext` (the query
client, `meta`, etc.) that is distinct from your returned result. Read your
decision from `onMutateResult`, not from that trailing context.

`onMutate` **cannot veto the mutation.** Returning early or `{ applied: false }`
only skips your optimistic/cache side effects; the `mutationFn` still runs. If
the mutation itself should not happen, guard before calling `mutate(...)` or
inside `mutationFn`.

**Incorrect (same decision recomputed in every callback):**

```ts
function useRenameTodo(todoId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: renameTodo,
    onMutate: async ([id, patch]) => {
      const title = renameTitle(id, todoId, patch)   // decision #1
      if (!title) return
      await queryClient.cancelQueries({ queryKey: ["todos", todoId] })
      const previous = queryClient.getQueryData(["todos", todoId])
      queryClient.setQueryData(["todos", todoId], (t) => ({ ...t, title }))
      return { previous }
    },
    onError: (_err, [id, patch], result) => {
      const title = renameTitle(id, todoId, patch)   // decision #2, recomputed
      if (!title || !result) return
      queryClient.setQueryData(["todos", todoId], result.previous)
    },
    onSettled: (_data, _err, [id, patch]) => {
      const title = renameTitle(id, todoId, patch)   // decision #3, recomputed
      if (!title) return
      queryClient.invalidateQueries({ queryKey: ["todos", todoId] })
    },
  })
}
```

**Correct (decide once, return a discriminated result, hoist stable values):**

```ts
type RenameTodoMutationResult =
  | { applied: false }
  | { applied: true; previous: Todo | undefined; title: string }

function useRenameTodo(todoId: string) {
  const queryClient = useQueryClient()
  const todoKey = ["todos", todoId] as const           // depends only on stable input
  return useMutation({
    mutationFn: renameTodo,
    onMutate: async ([id, patch]): Promise<RenameTodoMutationResult> => {
      const title = renameTitle(id, todoId, patch)       // derived ONCE
      if (!title) return { applied: false }
      await queryClient.cancelQueries({ queryKey: todoKey })
      const previous = queryClient.getQueryData<Todo>(todoKey)
      queryClient.setQueryData<Todo>(todoKey, (t) => (t ? { ...t, title } : t))
      return { applied: true, previous, title }          // decision + rollback + derived value
    },
    onError: (_err, _vars, result) => {
      if (!result?.applied) return                        // read onMutateResult, don't recompute
      queryClient.setQueryData(todoKey, result.previous)
    },
    onSettled: (_data, _err, _vars, result) => {
      if (!result?.applied) return
      queryClient.invalidateQueries({ queryKey: todoKey })
    },
  })
}
```

**Guidelines:**

- Decide "should the optimistic/cache side effects apply, and with what derived
  value?" in `onMutate`, and return it alongside rollback snapshots. A
  discriminated union (`{ applied: false } | { applied: true; ... }`) keeps the
  rollback fields available only on the branch that has them.
- In `onError`/`onSettled`, branch on `onMutateResult`, not by re-deriving from
  the variables. Those callbacks usually should not need the variables at all.
- Hoist query keys and key predicates that depend only on stable hook inputs to
  the hook body so each callback points at one definition.
- Keep a computation in a later callback only when it needs something `onMutate`
  cannot know yet - most often the server result in `onSuccess`.
- To prevent the mutation from running at all, guard before `mutate(...)` or in
  `mutationFn`; `onMutate` only controls side effects, not whether the request
  fires.

Reference: [`useMutation` reference](https://tanstack.com/query/latest/docs/framework/react/reference/useMutation)
and [Mutations guide](https://tanstack.com/query/latest/docs/framework/react/guides/mutations).
For optimistic writes, cancel affected queries, snapshot their prior cache values, restore them on error, and invalidate as needed when the mutation settles.
