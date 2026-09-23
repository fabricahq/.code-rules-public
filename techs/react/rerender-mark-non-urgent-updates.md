---
title: "Keep input responsive by marking non-urgent updates"
whenToRead: "Before planning, writing, changing, or reviewing React UI where user input or frequent events trigger expensive rendering or asynchronous work, such as filtering large lists, searching, or switching tabs."
impact: "MEDIUM"
impactDescription: "Rendering expensive updates at the same priority as typing makes input lag, and hand-written loading flags drift from the actual work."
tags: "react, transitions, useTransition, useDeferredValue, concurrency"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/tree/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules
    description: "Adapted from three Vercel Agent Skills rules (rerender-transitions, rerender-use-deferred-value, and rendering-usetransition-loading): merged three rules on transitions, deferred values, and transition-based loading state; restructured to the rule template; and corrected the async transition example to wrap updates after await."
---

## Keep input responsive by marking non-urgent updates

Keep updates that reflect what the user just did, such as the text in an input, urgent.
Mark the expensive updates they cause as non-urgent with `useTransition` or `useDeferredValue`, so React can interrupt them to handle new input.

### Implementation

- Use `useDeferredValue` when an expensive render derives from a value you do not control the update of, such as a prop or the text of a controlled input.
  Memoize the expensive computation with the deferred value as its dependency, or it still runs on every render.
- Use `useTransition` when you own the state update, such as switching tabs or starting an action, and use its `isPending` flag instead of a separate loading state.
- Never put the state that controls a text input inside a transition; input updates must be synchronous.
- In an async transition, wrap state updates that come after an `await` in another `startTransition` call; React does not yet mark them automatically.
- Guard against out-of-order results when several async transitions can overlap, such as by ignoring a response that does not match the latest request, or by using a data library that does so.
- Do not wrap cheap updates in transitions; they add scheduling without benefit.

### Rationale

React renders urgent updates to completion before handling the next event.
An expensive render caused by typing therefore blocks the next keystroke.
A transition or deferred value lets React show the typed character first and render the expensive result in the background, discarding it if newer input arrives.

### Examples

#### Application: Filtering a large list as the user types

**Incorrect (counterexample):**

```tsx
function Search({ items }: { items: ReadonlyArray<Item> }) {
  const [query, setQuery] = useState('');
  const filtered = items.filter((item) => fuzzyMatch(item, query));

  return (
    <>
      <input value={query} onChange={(event) => setQuery(event.target.value)} />
      <ResultsList results={filtered} />
    </>
  );
}
```

Each keystroke waits for the full filter and list render.

**Correct:**

```tsx
function Search({ items }: { items: ReadonlyArray<Item> }) {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  const filtered = useMemo(() => items.filter((item) => fuzzyMatch(item, deferredQuery)), [items, deferredQuery]);
  const isStale = query !== deferredQuery;

  return (
    <>
      <input value={query} onChange={(event) => setQuery(event.target.value)} />
      <div style={{ opacity: isStale ? 0.7 : 1 }}>
        <ResultsList results={filtered} />
      </div>
    </>
  );
}
```

#### Application: Loading state for asynchronous work

**Incorrect (counterexample):**

```tsx
async function handleSelectTab(tab: Tab) {
  setIsLoading(true);
  const data = await fetchTabData(tab);
  setTabData(data);
  setIsLoading(false);
}
```

If `fetchTabData` throws, `isLoading` stays true.

**Correct:**

```tsx
const [isPending, startTransition] = useTransition();

function handleSelectTab(tab: Tab) {
  startTransition(async () => {
    const data = await fetchTabData(tab);
    startTransition(() => {
      setTabData(data);
    });
  });
}
```

`isPending` resets when the transition ends, whether it succeeds or throws, and the update after `await` is wrapped so it is also a transition.

### Validation

Type quickly into the input with CPU throttling enabled, and check that characters appear without delay while results catch up.
Check that no state controlling an input is updated inside `startTransition`, and that updates after `await` in transitions are wrapped.

Cheap updates without transitions are not a violation.
