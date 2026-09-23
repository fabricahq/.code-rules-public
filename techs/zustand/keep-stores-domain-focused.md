---
title: "Keep Stores Domain-Focused"
whenToRead: "Before growing a Zustand store across multiple features or deciding how to split store responsibilities."
impact: "MEDIUM"
impactDescription: "keeps global state understandable by avoiding one broad application store"
tags: "zustand, store-design, slices, domain-state, organization"
---

## Keep Stores Domain-Focused

Keep Zustand stores small and aligned to one feature or client-state domain. Split large stores into typed slices only when one composed store is still the right boundary.

**Incorrect:**

```ts
type AppStore = AuthState &
  WorkspaceState &
  SettingsState &
  EditorState &
  ToastState &
  AuthActions &
  WorkspaceActions &
  SettingsActions &
  EditorActions &
  ToastActions;

export const useAppStore = create<AppStore>()((set, get) => ({
  // Every feature and action grows in one file.
}));
```

**Correct:**

```ts
export const useWorkspaceUiStore = create<WorkspaceUiStore>()((set) => ({
  navCollapsed: false,
  activePanelId: null,
  toggleNav: () => set((state) => ({ navCollapsed: !state.navCollapsed })),
  setActivePanel: (activePanelId) => set({ activePanelId }),
}));

export const useEditorDraftStore = create<EditorDraftStore>()((set) => ({
  selectedBlockId: null,
  dirtyFieldIds: new Set<string>(),
  selectBlock: (selectedBlockId) => set({ selectedBlockId }),
}));
```

**Guidelines:**

- Start with one focused store per client-state domain instead of one app-wide store.
- Use slices when multiple related state areas must share actions or middleware within the same composed store.
- Apply middleware at the composed store boundary so persistence, devtools, and immer wrap the final store consistently.
- Keep derived values as selectors or pure helpers unless there is a measured reason to cache them in state.

References: Synthesized from the Zustand guidance sources listed in the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
