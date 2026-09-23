---
title: "Subscribe With Selectors"
whenToRead: "Before reading a Zustand store in a React component or tuning rerenders from store updates."
impact: "HIGH"
impactDescription: "prevents components from rerendering for unrelated store changes"
tags: "zustand, selectors, use-shallow, rerenders, performance"
---

## Subscribe With Selectors

Components should subscribe to the smallest store slice they need. Calling a store hook with no selector makes the component rerender for any store field change.

**Incorrect:**

```tsx
function SidebarToggle() {
  const store = useWorkspaceUiStore();

  return (
    <button type="button" aria-expanded={store.sidebarOpen} onClick={store.toggleSidebar}>
      Toggle sidebar
    </button>
  );
}
```

**Correct:**

```tsx
import { useShallow } from "zustand/react/shallow";

function SidebarToggle() {
  const { sidebarOpen, toggleSidebar } = useWorkspaceUiStore(
    useShallow((state) => ({
      sidebarOpen: state.sidebarOpen,
      toggleSidebar: state.toggleSidebar,
    })),
  );

  return (
    <button type="button" aria-expanded={sidebarOpen} onClick={toggleSidebar}>
      Toggle sidebar
    </button>
  );
}
```

**Guidelines:**

- Select a single primitive directly when the component only needs one field.
- Use `useShallow` for object or tuple selectors that return multiple fields.
- Select actions separately or in a shallow selector when grouping actions with state.
- Keep selectors pure and cheap; move expensive derivations into memoized helpers or domain-specific selectors.

References: Synthesized from the Zustand guidance sources listed in the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
