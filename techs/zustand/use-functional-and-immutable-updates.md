---
title: "Use Functional and Immutable Updates"
whenToRead: "Before updating Zustand state from its prior value or changing nested objects and arrays."
impact: "HIGH"
impactDescription: "prevents stale reads and missed rerenders when actions depend on current state"
tags: "zustand, set, immutable-updates, immer, stale-closures"
---

## Use Functional and Immutable Updates

Use functional `set((state) => nextState)` whenever the next value depends on current state. Treat nested state immutably unless the store is explicitly wrapped in Immer middleware.

**Incorrect:**

```ts
type CounterStore = {
  count: number;
  nested: { selectedIds: Array<string> };
  incrementLater: () => Promise<void>;
  select: (id: string) => void;
};

export const useCounterStore = create<CounterStore>()((set, get) => ({
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

**Correct:**

```ts
export const useCounterStore = create<CounterStore>()((set) => ({
  count: 0,
  nested: { selectedIds: [] },
  incrementLater: async () => {
    await waitForAnimation();
    set((state) => ({ count: state.count + 1 }));
  },
  select: (id) =>
    set((state) => ({
      nested: {
        ...state.nested,
        selectedIds: [...state.nested.selectedIds, id],
      },
    })),
}));
```

**Guidelines:**

- Use object `set({ value })` only when the next value does not depend on current state.
- Use functional `set` for counters, toggles, appends, removals, async continuations, and batched user actions.
- Install Immer only when nested updates are frequent enough to justify the middleware.
- If using Immer, keep mutable-looking updates inside the Immer-wrapped store so callers do not assume mutation is generally safe.

References: Synthesized from the Zustand guidance sources listed in the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
