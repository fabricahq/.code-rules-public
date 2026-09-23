---
title: "Keep values that do not affect rendering in refs"
whenToRead: "Before writing, changing, or reviewing React components that track frequently changing values the UI does not display, such as pointer positions, timers, or in-flight request ids."
impact: "MEDIUM"
impactDescription: "Storing non-visual, frequently changing values in state re-renders the component on every change."
tags: "react, refs, state, performance"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-use-ref-transient-values.md
    description: "Adapted from the Vercel Agent Skills rule rerender-use-ref-transient-values: restructured to the rule template, with the rule against reading refs during render."
---

## Keep values that do not affect rendering in refs

Store a value in `useRef` when it changes often and the rendered output does not depend on it.
Keep a value in state when the UI displays it or derives output from it.

### Implementation

- Use refs for values such as timer ids, the latest pointer position used by an animation, or whether a request is in flight.
- Update refs in event handlers and Effects, not during render.
- Do not read a ref's `current` value during render; the output would not update when it changes.
- When a frequently changing value must drive visual changes, such as a cursor-following element, update the DOM node through a ref instead of re-rendering.

### Rationale

Every state update re-renders the component and its children.
A value updated on every pointer move or animation frame can trigger many renders per second for no visible change.
Changing a ref does not trigger a render.

### Examples

**Incorrect (counterexample):**

```tsx
function Canvas() {
  const [lastPointer, setLastPointer] = useState({ x: 0, y: 0 });

  function handlePointerMove(event: React.PointerEvent) {
    setLastPointer({ x: event.clientX, y: event.clientY });
  }

  function handleClick() {
    placeMarker(lastPointer);
  }

  return <div onPointerMove={handlePointerMove} onClick={handleClick} />;
}
```

The component re-renders on every pointer move, although only the click handler reads the position.

**Correct:**

```tsx
function Canvas() {
  const lastPointer = useRef({ x: 0, y: 0 });

  function handlePointerMove(event: React.PointerEvent) {
    lastPointer.current = { x: event.clientX, y: event.clientY };
  }

  function handleClick() {
    placeMarker(lastPointer.current);
  }

  return <div onPointerMove={handlePointerMove} onClick={handleClick} />;
}
```

### Validation

For each frequently updated state variable, check whether the rendered output uses it.
If it does not, it belongs in a ref.

State that the UI displays is not a violation, however often it changes.
