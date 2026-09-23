---
title: "Define Typed State and Named Actions"
whenToRead: "Before designing a Zustand store interface or exposing actions that update its state."
impact: "HIGH"
impactDescription: "keeps store shape explicit and prevents components from bypassing domain actions"
tags: "zustand, typescript, actions, store-shape, setters"
---

## Define Typed State and Named Actions

Model each store as explicit state plus named actions. Avoid anonymous catch-all setters that let components mutate arbitrary store fields without preserving domain invariants.

**Incorrect:**

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

**Correct:**

```ts
import { create } from "zustand";

type UiState = {
  sidebarOpen: boolean;
  activePanelId: string | null;
};

type UiActions = {
  openPanel: (panelId: string) => void;
  closeSidebar: () => void;
  toggleSidebar: () => void;
};

type UiStore = UiState & UiActions;

export const useUiStore = create<UiStore>()((set) => ({
  sidebarOpen: false,
  activePanelId: null,
  openPanel: (panelId) => set({ sidebarOpen: true, activePanelId: panelId }),
  closeSidebar: () => set({ sidebarOpen: false, activePanelId: null }),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
}));
```

**Guidelines:**

- Define state and action types for shared stores so action payloads and async return values are checked.
- Prefer verb-oriented action names such as `openPanel`, `renameDraft`, or `resetSelection`.
- Export the hook and any useful state types; avoid exporting a mutable raw store for ordinary component code.
- Use `create<T>()(...)` when typing stores, especially once middleware or slices are involved.

References: Synthesized from the Zustand guidance sources listed in the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
