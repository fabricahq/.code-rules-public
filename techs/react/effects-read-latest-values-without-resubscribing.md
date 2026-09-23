---
title: "Read the latest callbacks in Effects without resubscribing"
whenToRead: "Before planning, writing, changing, or reviewing React Effects or custom Hooks that subscribe to something and call a callback prop or read values that should not restart the subscription, or code that uses useEffectEvent."
impact: "MEDIUM"
impactDescription: "Listing a changing callback as an Effect dependency tears down and recreates the subscription on every render, while omitting it reads stale values."
tags: "react, effects, useEffectEvent, refs, subscriptions"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/tree/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules
    description: "Adapted from three Vercel Agent Skills rules (advanced-use-latest, advanced-event-handler-refs, and advanced-effect-event-deps): merged three related rules on Effect Events and callback refs, restructured to the rule template, and aligned with the documented useEffectEvent caveats."
---

## Read the latest callbacks in Effects without resubscribing

When an Effect should re-run only for some values but also needs the latest version of others, such as a callback prop, read those others through `useEffectEvent`, or through a ref in React versions without it.
Keep only the values that should restart the Effect in its dependency array.

### Implementation

- In React 19.2 or newer, wrap the non-reactive logic in `useEffectEvent` and call the returned function from inside the Effect or the subscriptions it creates.
- Do not put an Effect Event in a dependency array; its identity changes on every render by design.
- Call Effect Events only from Effects or other Effect Events in the same component.
  Do not call them during render or pass them to other components or Hooks.
- In older React versions, store the latest callback in a ref updated by an Effect, and call `ref.current` from the subscription.
- Keep values that should restart the Effect, such as a room id or event type, as ordinary dependencies.

### Rationale

An Effect re-runs whenever a dependency changes.
Callback props are usually new functions on every render, so listing one restarts the subscription on every render.
Leaving it out without an Effect Event or ref makes the Effect call the version from its first render, with stale props and state.

### Examples

#### Application: A subscription that calls a callback prop

**Incorrect (counterexample):**

```tsx
function useWindowEvent(type: string, handler: (event: Event) => void) {
  useEffect(() => {
    window.addEventListener(type, handler);
    return () => window.removeEventListener(type, handler);
  }, [type, handler]);
}
```

Callers usually pass an inline function, so the listener is removed and added again on every render.

**Correct (React 19.2 or newer):**

```tsx
function useWindowEvent(type: string, handler: (event: Event) => void) {
  const onEvent = useEffectEvent(handler);

  useEffect(() => {
    const listener = (event: Event) => onEvent(event);
    window.addEventListener(type, listener);
    return () => window.removeEventListener(type, listener);
  }, [type]);
}
```

**Correct (earlier React versions):**

```tsx
function useWindowEvent(type: string, handler: (event: Event) => void) {
  const handlerRef = useRef(handler);

  useEffect(() => {
    handlerRef.current = handler;
  }, [handler]);

  useEffect(() => {
    const listener = (event: Event) => handlerRef.current(event);
    window.addEventListener(type, listener);
    return () => window.removeEventListener(type, listener);
  }, [type]);
}
```

#### Application: An Effect Event in dependencies

**Incorrect (counterexample):**

```tsx
const onConnected = useEffectEvent(onConnectedProp);

useEffect(() => {
  const connection = createConnection(roomId);
  connection.on('connected', () => onConnected());
  connection.connect();
  return () => connection.disconnect();
}, [roomId, onConnected]);
```

The Effect Event's identity changes every render, so the connection restarts every render, and the Hooks lint rule reports it.

**Correct:**

```tsx
useEffect(() => {
  const connection = createConnection(roomId);
  connection.on('connected', () => onConnected());
  connection.connect();
  return () => connection.disconnect();
}, [roomId]);
```

### Validation

Check that the React Hooks lint rules pass without suppressions for these Effects.
Re-render the component with a new callback prop and check that the subscription is not recreated.

Listing a callback as a dependency is not a violation when the Effect should restart whenever that callback changes.
