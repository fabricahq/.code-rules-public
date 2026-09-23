---
title: "Avoid unnecessary Effects"
whenToRead: "Before planning, writing, changing, or reviewing React Effects, values derived from props or state, or behavior triggered by a user action."
impact: "HIGH"
impactDescription: "Effects used for derived values or user actions add extra renders, drift out of sync, and can repeat actions unexpectedly."
tags: "react, effects, derived-state, events"
attribution:
  - url: https://react.dev/learn/you-might-not-need-an-effect
    description: "Official React documentation paraphrased in the source rule; merged with the related derived-state and event-handler rules and restructured to the rule template."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-derived-state-no-effect.md
    description: "Adapted from the Vercel Agent Skills rule rerender-derived-state-no-effect: merged with the related derived-state and event-handler rules and restructured to the rule template."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-move-effect-to-event.md
    description: "Adapted from the Vercel Agent Skills rule rerender-move-effect-to-event: merged with the related derived-state and event-handler rules and restructured to the rule template."
---

## Avoid unnecessary Effects

Use an Effect only to synchronize with a system outside React, such as a subscription, a timer, a network connection, or an imperative widget.
Compute derived values during render, and run logic caused by a user action in that action's event handler.

### Implementation

- When a value can be calculated from current props or state, calculate it during render instead of storing it in state and updating it in an Effect.
  Wrap an expensive calculation in `useMemo` when measurement shows it is slow.
- When code runs because the user did something, such as submitting a form or clicking a button, put it in the event handler.
  Do not set a flag in the handler and react to it in an Effect.
- To reset a component's state when an identifying prop changes, give the component a `key` based on that prop instead of resetting state in an Effect.
- Keep an Effect when the code must run because the component is displayed, such as subscribing to an external store or connecting to a server.

### Rationale

An Effect runs after render and commit.
Using one to set derived state causes an extra render with stale values in between, and the copy can drift from its source.
Modeling an action as state plus an Effect ties the action to rendering: the Effect can re-run when an unrelated dependency changes and repeat the action.

### Examples

#### Application: A derived value

**Incorrect (counterexample):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First');
  const [lastName, setLastName] = useState('Last');
  const [fullName, setFullName] = useState('');

  useEffect(() => {
    setFullName(`${firstName} ${lastName}`);
  }, [firstName, lastName]);

  return <p>{fullName}</p>;
}
```

The first render shows an empty name, and each change renders twice.

**Correct:**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First');
  const [lastName, setLastName] = useState('Last');
  const fullName = `${firstName} ${lastName}`;

  return <p>{fullName}</p>;
}
```

#### Application: An action triggered by the user

**Incorrect (counterexample):**

```tsx
function Checkout({ productId }: { productId: string }) {
  const [submitted, setSubmitted] = useState(false);
  const theme = useContext(ThemeContext);

  useEffect(() => {
    if (submitted) {
      purchase(productId);
      showToast('Purchased', theme);
    }
  }, [submitted, productId, theme]);

  return <button onClick={() => setSubmitted(true)}>Buy</button>;
}
```

Changing the theme after purchase re-runs the Effect while `submitted` is still true, so the purchase repeats.

**Correct:**

```tsx
function Checkout({ productId }: { productId: string }) {
  const theme = useContext(ThemeContext);

  function handleBuy() {
    purchase(productId);
    showToast('Purchased', theme);
  }

  return <button onClick={handleBuy}>Buy</button>;
}
```

#### Application: A necessary Effect

**Correct:**

```tsx
function ChatRoom({ roomId }: { roomId: string }) {
  useEffect(() => {
    const connection = createConnection(roomId);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]);
  // ...
}
```

The connection must exist while the component is displayed, whatever caused it to appear, so an Effect is the right tool.

### Validation

For each Effect, name the external system it synchronizes with.
An Effect that only sets state from other props or state, or that only responds to a user action, violates this rule.

An Effect that subscribes, connects, or controls a non-React widget is not a violation.
