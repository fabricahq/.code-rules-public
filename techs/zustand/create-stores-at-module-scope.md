---
title: "Create Stores at Module Scope"
whenToRead: "Before creating a Zustand store used by React components or deciding whether it needs a per-instance factory."
impact: "HIGH"
impactDescription: "prevents store instances from being recreated during render and losing state or subscriptions"
tags: "zustand, store-creation, module-scope, react-render, subscriptions"
---

## Create Stores at Module Scope

Create Zustand stores once at module scope. Do not call `create` inside React components, hooks, render functions, or other code paths that can run repeatedly.

**Incorrect:**

```tsx
import { create } from "zustand";

function Panel() {
  const usePanelStore = create<{ open: boolean; toggle: () => void }>()((set) => ({
    open: false,
    toggle: () => set((state) => ({ open: !state.open })),
  }));

  const open = usePanelStore((state) => state.open);
  return <div hidden={!open}>Panel content</div>;
}
```

**Correct:**

```ts
import { create } from "zustand";

type PanelStore = {
  open: boolean;
  toggle: () => void;
};

export const usePanelStore = create<PanelStore>()((set) => ({
  open: false,
  toggle: () => set((state) => ({ open: !state.open })),
}));
```

```tsx
import { usePanelStore } from "./panel-store";

function Panel() {
  const open = usePanelStore((state) => state.open);
  return <div hidden={!open}>Panel content</div>;
}
```

**Guidelines:**

- Put ordinary store `create` calls in dedicated store modules.
- Use a vanilla store factory only when a framework boundary genuinely needs per-request or per-instance stores.
- If a component needs isolated local state, use React state or a scoped vanilla-store provider pattern rather than creating a hook store during render.
- Keep store initialization deterministic and free of browser-only reads; use middleware or explicit actions for runtime initialization.

References: Synthesized from the Zustand guidance sources listed in the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
