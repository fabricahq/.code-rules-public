---
title: "Use useDeferredValue for Expensive Derived Renders"
whenToRead: "Before handling user input that triggers expensive React rendering or derived computation."
impact: "MEDIUM"
impactDescription: "keeps input responsive during heavy computation"
tags: "react, performance, rerender, useDeferredValue, optimization, concurrent"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-use-deferred-value.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Use useDeferredValue for Expensive Derived Renders

When user input triggers expensive computations or renders, use `useDeferredValue` to keep the input responsive. The deferred value lags behind, allowing React to prioritize the input update and render the expensive result when idle.

**Incorrect (input feels laggy while filtering):**

```tsx
function Search({ items }: { items: Item[] }) {
  const [query, setQuery] = useState('')
  const filtered = items.filter(item => fuzzyMatch(item, query))

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <ResultsList results={filtered} />
    </>
  )
}
```

**Correct (input stays snappy, results render when ready):**

```tsx
function Search({ items }: { items: Item[] }) {
  const [query, setQuery] = useState('')
  const deferredQuery = useDeferredValue(query)
  const filtered = useMemo(
    () => items.filter(item => fuzzyMatch(item, deferredQuery)),
    [items, deferredQuery]
  )
  const isStale = query !== deferredQuery

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <div style={{ opacity: isStale ? 0.7 : 1 }}>
        <ResultsList results={filtered} />
      </div>
    </>
  )
}
```

**When to use:**

- Filtering/searching large lists
- Expensive visualizations (charts, graphs) reacting to input
- Any derived state that causes noticeable render delays

**Note:** Wrap the expensive computation in `useMemo` with the deferred value as a dependency, otherwise it still runs on every render.

Reference: [React useDeferredValue](https://react.dev/reference/react/useDeferredValue)

Source: [Vercel Agent Skills - react-best-practices/rerender-use-deferred-value.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-use-deferred-value.md). Adapted with attribution.
