---
title: "Read mutation state from other components with useMutationState"
whenToRead: "Before planning, writing, changing, or reviewing React components that show the progress or pending values of a TanStack Query mutation started in a different component."
impact: "LOW-MEDIUM"
impactDescription: "Passing mutation state through props or custom context couples unrelated components to the one that triggered the mutation."
tags: "tanstack-query, mutations, useMutationState"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/mut-mutation-state.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule mut-mutation-state (MIT, notice retained in NOTICE.md): restructured to the rule template, used stable mutation ids as list keys, and scoped the rule to cross-component reads."
---

## Read mutation state from other components with useMutationState

When a component other than the one calling `useMutation` needs a mutation's status or pending variables, give the mutation a `mutationKey` and read it with `useMutationState`.

### Implementation

- Set a `mutationKey` on mutations that other components observe, using the same hierarchical style as query keys, such as `['todos', 'create']` or `['posts', postId, 'delete']`.
- Filter with `mutationKey` and `status`, and use `select` to return only what the component renders.
- Without `select`, each result is the mutation's state object, with fields such as `status`, `variables`, and `isPaused`.
- Use `mutation.mutationId` as a stable React key when rendering pending items.
- Use `useIsMutating` when you only need a count.
- The component calling `useMutation` can read its own `isPending` and `variables` directly.

### Rationale

Mutation state lives in the query client's mutation cache, which any component under the provider can read.
Threading it through props or a custom context couples distant components to the one that triggered the mutation and breaks when the trigger moves.

### Examples

**Incorrect (counterexample):**

```tsx
function TodoPage() {
  const createTodo = useMutation({ mutationFn: api.createTodo });
  return (
    <>
      <TodoForm onCreate={createTodo.mutate} />
      <TodoList pendingTodo={createTodo.isPending ? createTodo.variables : undefined} />
    </>
  );
}
```

The page owns the mutation only so it can pass its state to a sibling.

**Correct:**

```tsx
function TodoForm() {
  const createTodo = useMutation({ mutationKey: ['todos', 'create'], mutationFn: api.createTodo });
  // ...
}

function TodoList() {
  const pendingTodos = useMutationState({
    filters: { mutationKey: ['todos', 'create'], status: 'pending' },
    select: (mutation) => ({ id: mutation.mutationId, todo: mutation.state.variables as NewTodo }),
  });

  return (
    <ul>
      {pendingTodos.map(({ id, todo }) => (
        <PendingTodoItem key={id} todo={todo} />
      ))}
    </ul>
  );
}
```

### Validation

Check that components showing another component's mutation progress read it through `useMutationState` or `useIsMutating`, and that the observed mutations have a `mutationKey`.

Reading `isPending` or `variables` in the component that calls `useMutation` is not a violation.
