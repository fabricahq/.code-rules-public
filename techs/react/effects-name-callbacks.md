---
title: "Name Effect Callbacks; Extract a Hook When They Grow"
whenToRead: "Before writing or changing a React effect with nontrivial setup or synchronization logic."
impact: "MEDIUM"
impactDescription: "named effects aid debugging and signal when logic should become a hook"
tags: "react, useEffect, effects, naming, readability, custom-hooks, maintainability"
---

## Name Effect Callbacks; Extract a Hook When They Grow

Pass a named function expression to `useEffect` instead of an anonymous
arrow. The name documents what the effect synchronizes or sets up right at
the call site, and it surfaces in React DevTools and stack traces instead of
an anonymous frame. Name the effect for the job it does, not the value that
triggers it (`syncEditorReadOnlyState`, not `onReadOnlyChange`).

This rule is about effects that genuinely need to be effects. Before naming
one, confirm it should exist at all - interaction logic belongs in an event
handler, and values computed from props or state belong in render. For
non-effect hook callbacks, name the function when the work is nontrivial.

**Incorrect (anonymous callback):**

```tsx
useEffect(() => {
  if (!editor) return;
  editor.setEditable(!readOnly);
  if (readOnly) closeBlockMenu();
}, [closeBlockMenu, editor, readOnly]);
```

**Correct (named callback):**

```tsx
useEffect(function syncEditorReadOnlyState() {
  if (!editor) return;
  editor.setEditable(!readOnly);
  if (readOnly) closeBlockMenu();
}, [closeBlockMenu, editor, readOnly]);
```

**Escalate to a custom hook when the effect outgrows a one-liner.** Move it
and its companion logic into a `useX` hook named for the behavior it owns,
keeping the named effect inside:

```tsx
// use-editor-read-only-sync.ts
function useEditorReadOnlySync(editor: Editor | null, readOnly: boolean, closeBlockMenu: () => void) {
  useEffect(function syncEditorReadOnlyState() {
    if (!editor) return;
    editor.setEditable(!readOnly);
    if (readOnly) closeBlockMenu();
  }, [closeBlockMenu, editor, readOnly]);
}
```

**Guidelines:**

- Give every `useEffect` callback a named function expression with a
  verb-first name describing its job (`subscribeToResize`, `focusFirstField`,
  `persistDraft`). Applies even to short effects - the cost is one identifier.
- Extract the effect into a custom hook when **any** of these is true:
  - It grows companion logic - its own `ref`s, derived state, or non-trivial
    cleanup such as subscription/listener teardown.
  - The same effect is needed in more than one component (reuse).
  - The component body has so many effects that it is hard to scan top to
    bottom; lifting each into a named hook restores readability.
- Name the hook for the behavior it encapsulates (`useEditorReadOnlySync`),
  not for the effect mechanic, and keep the inner effect callback named too.
- Do not extract a hook prematurely. A single small effect with no companion
  state is fine inline as a named callback; reach for a hook only once the
  effect earns its own surface by one of the triggers above.
