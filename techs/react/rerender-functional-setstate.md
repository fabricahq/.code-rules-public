---
title: "Use functional updates when new state depends on old state"
whenToRead: "Before planning, writing, changing, or reviewing React state updates that compute the next value from the current one, especially inside callbacks, timers, or asynchronous code."
impact: "MEDIUM"
impactDescription: "Updates that read state from a closure can use a stale value and silently drop changes."
tags: "react, state, closures"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-functional-setstate.md
    description: "Adapted from the Vercel Agent Skills rule rerender-functional-setstate: restructured to the rule template, with an asynchronous example and corrected claims."
---

## Use functional updates when new state depends on old state

When the next state is computed from the current state, pass an updater function to the state setter, such as `setItems((current) => [...current, item])`.

### Implementation

- Use the updater form for increments, appends, removals, and toggles.
- Use it in callbacks that may run after later renders, such as timers, subscriptions, and code after an `await`.
- Setting state to a value that does not depend on the previous state, such as `setName(nextName)` or `setCount(0)`, does not need the updater form.
- Keep updater functions pure; React may call them more than once in development.

### Rationale

A callback sees the state value from the render that created it.
If the state changes before the callback runs, or several updates are queued at once, an update computed from that captured value overwrites the newer state.
An updater receives the latest pending state instead, and it lets a memoized callback omit that state from its dependencies.

### Examples

#### Application: Updates in a callback

**Incorrect (counterexample):**

```tsx
function TodoList() {
  const [items, setItems] = useState<Array<Item>>([]);

  const removeItem = useCallback((id: string) => {
    setItems(items.filter((item) => item.id !== id));
  }, []);
  // ...
}
```

The callback captured the first render's `items`, so each removal restores every item added since.

**Correct:**

```tsx
function TodoList() {
  const [items, setItems] = useState<Array<Item>>([]);

  const removeItem = useCallback((id: string) => {
    setItems((current) => current.filter((item) => item.id !== id));
  }, []);
  // ...
}
```

#### Application: Updates after asynchronous work

**Incorrect (counterexample):**

```tsx
async function handleUpload(file: File) {
  const uploaded = await upload(file);
  setFiles([...files, uploaded]);
}
```

If two uploads finish close together, the second update is computed from a list that does not include the first, and one upload disappears.

**Correct:**

```tsx
async function handleUpload(file: File) {
  const uploaded = await upload(file);
  setFiles((current) => [...current, uploaded]);
}
```

### Validation

Search for state setters whose argument reads the same state variable, such as `setCount(count + 1)` or `setItems([...items, item])`.
Each one inside a callback, timer, subscription, or asynchronous function should use the updater form.

A direct update in a synchronous event handler that runs once per render is not a violation, although the updater form is still acceptable there.
