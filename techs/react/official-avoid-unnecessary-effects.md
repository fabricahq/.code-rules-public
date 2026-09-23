---
title: "Avoid Unnecessary Effects"
whenToRead: "When planning, implementing, or reviewing React effects, derived values, or event-driven actions."
impact: "HIGH"
impactDescription: "reduces redundant renders, dependency churn, and state synchronization bugs"
tags: "react, effects, derived-state, event-handlers, render"

attribution:
  - url: https://react.dev/learn/you-might-not-need-an-effect
    description: "Official React documentation paraphrased in the source rule."
---

## Avoid Unnecessary Effects

Do not reach for `useEffect` when the work can happen during render or inside the event handler that caused it. Effects are for synchronizing with systems outside React, such as subscriptions, imperative widgets, timers, and network connections.

**Incorrect (effect used for event-specific logic):**

```tsx
function Checkout({ productId }: { productId: string }) {
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    if (submitted) {
      trackPurchase(productId);
    }
  }, [submitted, productId]);

  return <button onClick={() => setSubmitted(true)}>Buy</button>;
}
```

**Correct (the event owns the event-specific work):**

```tsx
function Checkout({ productId }: { productId: string }) {
  function handleBuy() {
    trackPurchase(productId);
  }

  return <button onClick={handleBuy}>Buy</button>;
}
```

When an Effect only derives one piece of state from another, calculate the value during render instead. When an Effect only responds to a user action, move that work into the action handler.

References: [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect), [Separating Events from Effects](https://react.dev/learn/separating-events-from-effects).

Source: [React docs - You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect). Paraphrased from official React documentation.
