---
title: "Update store state functionally and immutably"
whenToRead: "Before writing, changing, or reviewing Zustand actions that compute new state from current state, update nested objects or arrays, or update state after awaiting."
impact: "HIGH"
impactDescription: "Updates computed from a stale snapshot drop concurrent changes, and mutating state in place leaves subscribers unaware of the change."
tags: "zustand, actions, immutability, set"
---

## Update store state functionally and immutably

When new state depends on current state, pass a function to `set`, and return new objects and arrays for anything that changed.
Mutate state directly only inside a store wrapped in the `immer` middleware.

### Implementation

- Use `set((state) => ...)` for increments, toggles, appends, removals, and updates made after an `await`.
- Use `set({ field: value })` only when the value does not depend on current state.
- `set` merges only the top level; copy each nested level you change, such as `{ nested: { ...state.nested, ids: [...state.nested.ids, id] } }`.
- Never mutate `state` inside `set` and return it; the store sees the same reference and does not notify subscribers.
- Add the `immer` middleware when nested updates are frequent enough that copying becomes error-prone, and keep mutable-style updates inside that store.

### Rationale

Zustand notifies subscribers when the new state differs by reference.
A value read before an `await` may be outdated by the time `set` runs, so the update overwrites changes made in between.
Mutating the existing state object keeps the same references, so selectors see no change and the UI does not update.

### Examples

**Incorrect (counterexample):**

```ts
export const useSelectionStore = create<SelectionStore>()((set, get) => ({
  count: 0,
  nested: { selectedIds: [] },
  incrementLater: async () => {
    const count = get().count;
    await waitForAnimation();
    set({ count: count + 1 });
  },
  select: (id) =>
    set((state) => {
      state.nested.selectedIds.push(id);
      return state;
    }),
}));
```

Two overlapping `incrementLater` calls add one instead of two, and `select` mutates in place, so components never re-render.

**Correct:**

```ts
export const useSelectionStore = create<SelectionStore>()((set) => ({
  count: 0,
  nested: { selectedIds: [] },
  incrementLater: async () => {
    await waitForAnimation();
    set((state) => ({ count: state.count + 1 }));
  },
  select: (id) =>
    set((state) => ({
      nested: { ...state.nested, selectedIds: [...state.nested.selectedIds, id] },
    })),
}));
```

### Validation

Search actions for `set` calls that use values read before an `await`, and for mutations of `state` inside `set`.
Check that components re-render after each action changes the fields they select.

Mutable-style updates inside a store wrapped in `immer` are not a violation.
