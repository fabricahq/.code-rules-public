---
title: "Keep each store focused on one domain"
whenToRead: "Before planning, writing, changing, or reviewing the boundaries of Zustand stores, such as adding state for a new feature, splitting a large store, or composing slices."
impact: "MEDIUM"
impactDescription: "One app-wide store couples unrelated features, grows without bound, and makes every change touch shared code."
tags: "zustand, store-design, slices, modularity"
---

## Keep each store focused on one domain

Create one store per feature or client-state domain, such as workspace UI or editor selection, instead of one app-wide store.
Use slices only when several state areas genuinely need to share actions or middleware in one store.

### Implementation

- Start a new store when a feature's state has no reason to change together with existing state.
- Name each store for its domain, such as `useWorkspaceUiStore` or `useEditorSelectionStore`.
- When related state areas must update together or share middleware, compose them from typed slices into one store.
- Apply middleware such as `persist`, `devtools`, or `immer` once, around the composed store, not inside individual slices.
- Derive values with selectors or pure helpers rather than storing them, unless measurement shows the derivation is expensive.

### Rationale

Features change independently.
In an app-wide store, each change to one feature edits a shared file and type, and every action can reach every other feature's state.
Focused stores keep ownership clear and make each store easy to test and reset on its own.

### Examples

**Incorrect (counterexample):**

```ts
type AppStore = AuthState & WorkspaceState & SettingsState & EditorState & ToastState;

export const useAppStore = create<AppStore>()((set, get) => ({
  // Every feature's state and actions grow in one file.
}));
```

**Correct:**

```ts
export const useWorkspaceUiStore = create<WorkspaceUiStore>()((set) => ({
  navCollapsed: false,
  toggleNav: () => set((state) => ({ navCollapsed: !state.navCollapsed })),
}));

export const useEditorSelectionStore = create<EditorSelectionStore>()((set) => ({
  selectedBlockId: null,
  selectBlock: (selectedBlockId) => set({ selectedBlockId }),
}));
```

### Validation

Check whether a new field belongs to an existing store's domain, and whether any store's actions change state belonging to unrelated features.

A composed store built from slices that share middleware and actions is not a violation.
