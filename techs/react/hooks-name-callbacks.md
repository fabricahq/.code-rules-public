---
title: "Name Effect and non-trivial Hook callbacks"
whenToRead: "Before writing, changing, or reviewing callbacks passed to React Hooks, such as useEffect, useMemo, or useCallback, or deciding whether Hook logic should become a custom Hook."
impact: "LOW"
impactDescription: "Anonymous Hook callbacks hide what an Effect or computation is for at the call site and in stack traces."
tags: "react, hooks, naming, readability"
---

## Name Effect and non-trivial Hook callbacks

Pass a named function expression to every `useEffect` call, and to other Hooks such as `useMemo` and `useCallback` when the callback does non-trivial work.
Name it for the job it does, starting with a verb.
When the logic grows its own state or cleanup, move it into a custom Hook named for that behavior.

### Implementation

- Name Effects for what they synchronize, such as `syncEditorReadOnlyState` or `subscribeToResize`, not for what triggers them, such as `onReadOnlyChange`.
- Name derivations for what they produce, such as `deriveVisibleRows`.
- A one-expression callback to `useMemo` or `useCallback` can stay anonymous.
- Extract a custom Hook when the logic gains companion refs or state, non-trivial cleanup, a second caller, or when a component has so many Effects it is hard to scan.
  Name the Hook for the behavior, such as `useEditorReadOnlySync`, and keep the inner callback named.
- Do not extract a Hook just to shorten a component; the Hook should own a coherent behavior.
- Before naming an Effect, confirm it should be an Effect at all; derived values belong in render and user-triggered logic in event handlers.

This is a readability convention; a project may choose not to adopt it.

### Rationale

An anonymous callback makes readers study the body to learn what an Effect is for.
A name states the intent at the call site, appears in stack traces and profiler output, and makes it easier to notice when the logic has grown into a separate behavior.

### Examples

**Incorrect (counterexample):**

```tsx
useEffect(() => {
  if (!editor) return;
  editor.setEditable(!readOnly);
  if (readOnly) closeBlockMenu();
}, [closeBlockMenu, editor, readOnly]);
```

**Correct:**

```tsx
useEffect(
  function syncEditorReadOnlyState() {
    if (!editor) return;
    editor.setEditable(!readOnly);
    if (readOnly) closeBlockMenu();
  },
  [closeBlockMenu, editor, readOnly],
);
```

### Validation

Check that each `useEffect` callback in new or changed code is a named function expression, and that `useMemo` and `useCallback` callbacks longer than one expression are named.

A one-expression `useMemo` or `useCallback` callback is not a violation.
