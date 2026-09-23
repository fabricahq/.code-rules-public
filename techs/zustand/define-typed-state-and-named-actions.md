---
title: "Define typed state and named actions"
whenToRead: "Before planning, writing, changing, or reviewing a Zustand store's type, its actions, or components that update store state."
impact: "MEDIUM-HIGH"
impactDescription: "A catch-all setter lets any component write any field in any combination, bypassing the rules that keep related fields consistent."
tags: "zustand, typescript, actions, invariants"
---

## Define typed state and named actions

Type each store as its state plus named actions, and change state only through those actions.
Each action should express one domain operation and keep related fields consistent.

### Implementation

- Declare separate state and action types, and create the store with `create<Store>()(...)`, which keeps inference working with middleware.
- Name actions for what they do, such as `openPanel`, `renameDraft`, or `resetSelection`.
- Update related fields together inside one action, such as opening a panel and recording which one is active.
- Do not expose a generic `setState(patch)` action or the raw store's `setState` to components.
- Keep `getState` and `setState` on the store for tests and non-React code, not for ordinary components.

### Rationale

Fields in a store often depend on each other, such as a selected ID that must point at an open panel.
A generic setter moves the responsibility for those rules to every caller, and one caller that forgets breaks them.
Named actions keep each rule in one place, make the store's operations discoverable, and give TypeScript precise payload types.

### Examples

**Incorrect (counterexample):**

```ts
type UiStore = {
  sidebarOpen: boolean;
  activePanelId: string | null;
  setState: (patch: Partial<UiStore>) => void;
};

export const useUiStore = create<UiStore>()((set) => ({
  sidebarOpen: false,
  activePanelId: null,
  setState: (patch) => set(patch),
}));
```

A component can set `activePanelId` while leaving the sidebar closed, an inconsistent combination.

**Correct:**

```ts
type UiState = { sidebarOpen: boolean; activePanelId: string | null };
type UiActions = {
  openPanel: (panelId: string) => void;
  closeSidebar: () => void;
};

export const useUiStore = create<UiState & UiActions>()((set) => ({
  sidebarOpen: false,
  activePanelId: null,
  openPanel: (panelId) => set({ sidebarOpen: true, activePanelId: panelId }),
  closeSidebar: () => set({ sidebarOpen: false, activePanelId: null }),
}));
```

### Validation

Check that components change store state only through named actions, and that no action accepts an arbitrary partial state.

A tiny store with one independent field and a single setter, such as a theme name, is not a violation.
