---
title: "Subscribe to and depend on only the values you use"
whenToRead: "Before writing, changing, or reviewing React components that subscribe to frequently changing values, such as window size, URL search parameters, or store state, or Effects whose dependencies are whole objects."
impact: "MEDIUM"
impactDescription: "Subscribing to or depending on broader values than a component uses re-renders it or re-runs its Effects on changes that do not matter."
tags: "react, subscriptions, dependencies, rerender"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-derived-state.md
    description: "Adapted from the Vercel Agent Skills rule rerender-derived-state: merged three rules on derived subscriptions, deferred reads, and narrow Effect dependencies, and restructured to the rule template."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-defer-reads.md
    description: "Adapted from the Vercel Agent Skills rule rerender-defer-reads: merged three rules on derived subscriptions, deferred reads, and narrow Effect dependencies, and restructured to the rule template."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-dependencies.md
    description: "Adapted from the Vercel Agent Skills rule rerender-dependencies: merged three rules on derived subscriptions, deferred reads, and narrow Effect dependencies, and restructured to the rule template."
---

## Subscribe to and depend on only the values you use

Subscribe to the narrowest value a component renders, and give Effects the narrowest dependencies they read.
When a value is needed only inside an event handler, read it there instead of subscribing to it.

### Implementation

- Subscribe to a derived value when the component only needs the derivation, such as a media query match instead of the exact window width.
- Select only the needed fields from a store, rather than the whole store object.
- When a value is read only in a handler, such as a search parameter used when sharing a link, read it in the handler.
  In a router-based app, read the current URL at that moment rather than subscribing through a Hook that re-renders on every change.
- Use primitive fields, such as `user.id`, as Effect dependencies when the Effect reads only those fields.
- Compute a boolean before the Effect, such as `const isMobile = width < 768`, when the Effect cares only about crossing a threshold.

### Rationale

A component re-renders whenever a value it subscribes to changes, and an Effect re-runs whenever a dependency changes.
Subscribing to a continuous value such as window width re-renders on every pixel of a resize, even when the output changes only at one breakpoint.
Narrowing the subscription or dependency limits the work to changes that affect the result.

### Examples

#### Application: A derived subscription

**Incorrect (counterexample):**

```tsx
function Sidebar() {
  const width = useWindowWidth();
  const isMobile = width < 768;
  return <nav className={isMobile ? 'mobile' : 'desktop'} />;
}
```

The sidebar re-renders on every resize event.

**Correct:**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery('(max-width: 767px)');
  return <nav className={isMobile ? 'mobile' : 'desktop'} />;
}
```

#### Application: A value read only in a handler

**Incorrect (counterexample):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const searchParams = useSearchParams();

  function handleShare() {
    shareChat(chatId, { ref: searchParams.get('ref') });
  }

  return <button onClick={handleShare}>Share</button>;
}
```

The button re-renders on every search parameter change, although it renders nothing that depends on them.

**Correct:**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  function handleShare() {
    const ref = new URLSearchParams(window.location.search).get('ref');
    shareChat(chatId, { ref });
  }

  return <button onClick={handleShare}>Share</button>;
}
```

#### Application: Effect dependencies

**Incorrect (counterexample):**

```tsx
useEffect(() => {
  trackProfileView(user.id);
}, [user]);
```

The Effect re-runs whenever any field of `user` changes.

**Correct:**

```tsx
useEffect(() => {
  trackProfileView(user.id);
}, [user.id]);
```

### Validation

Use the React DevTools Profiler to check that components re-render only when values they display change.
Check that Effects list the specific fields they read, and that the Hooks lint rules pass.

Subscribing to a value the component renders directly is not a violation, however often it changes.
