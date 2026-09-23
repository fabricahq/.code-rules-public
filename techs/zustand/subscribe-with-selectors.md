---
title: "Subscribe with narrow, stable selectors"
whenToRead: "Before writing, changing, or reviewing React components that read from a Zustand store, or diagnosing re-renders or maximum update depth errors caused by a store."
impact: "HIGH"
impactDescription: "Reading a whole store re-renders on every change, and a selector that returns a new object each time re-renders endlessly in Zustand 5."
tags: "zustand, selectors, useShallow, rerender"
---

## Subscribe with narrow, stable selectors

Read only what a component uses, with a selector.
Select a single value directly, and wrap selectors that return a new object or array in `useShallow`.

### Implementation

- Pass a selector to every store Hook call; calling the Hook with no selector subscribes to the entire store.
- Select one field or action directly, such as `useStore((state) => state.sidebarOpen)`.
- When selecting several fields into an object or array, wrap the selector in `useShallow`.
- Actions never change identity, so selecting them separately costs nothing.
- Keep selectors cheap and pure; move expensive derivations into memoized helpers.

### Rationale

A component re-renders when its selector's result changes by `Object.is`.
Without a selector, the result is the whole state, which changes on every update.
A selector that builds a new object returns a different reference every time; Zustand 5 re-renders on each one and can loop until React throws a maximum update depth error.
`useShallow` compares the object's fields instead.

### Examples

#### Application: No selector

**Incorrect (counterexample):**

```tsx
function SidebarToggle() {
  const store = useWorkspaceUiStore();
  return <button aria-expanded={store.sidebarOpen} onClick={store.toggleSidebar} />;
}
```

The toggle re-renders whenever any workspace UI field changes.

**Correct:**

```tsx
function SidebarToggle() {
  const sidebarOpen = useWorkspaceUiStore((state) => state.sidebarOpen);
  const toggleSidebar = useWorkspaceUiStore((state) => state.toggleSidebar);
  return <button aria-expanded={sidebarOpen} onClick={toggleSidebar} />;
}
```

#### Application: Several fields at once

**Incorrect (counterexample):**

```tsx
const { sidebarOpen, activePanelId } = useWorkspaceUiStore((state) => ({
  sidebarOpen: state.sidebarOpen,
  activePanelId: state.activePanelId,
}));
```

The selector returns a new object on every call, which Zustand 5 treats as a change every time.

**Correct:**

```tsx
const { sidebarOpen, activePanelId } = useWorkspaceUiStore(
  useShallow((state) => ({ sidebarOpen: state.sidebarOpen, activePanelId: state.activePanelId })),
);
```

### Validation

Search for store Hook calls without a selector, and for selectors that return object or array literals without `useShallow`.
Use the React DevTools Profiler to check that components re-render only when their selected values change.

Selecting a single primitive or action without `useShallow` is not a violation.
