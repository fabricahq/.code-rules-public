---
title: "qk-serializable: Ensure All Key Parts Are JSON-Serializable"
whenToRead: "Before putting functions, objects, or other non-primitive values into a TanStack Query key."
impact: "MEDIUM"
impactDescription: "keeps query-key hashing stable by avoiding non-serializable key parts"
tags: "tanstack-query, query-keys, serialization, hashing, cache"
attribution: [{"url":"https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/qk-serializable.md","description":"Underlying tanstack-agent-skills material at skills/tanstack-query/rules/qk-serializable.md, commit 0e8bcdc6af4959739e0f6a2dfb35dc70d513940a; adapted under MIT, with notice retained in the public library."}]
---

## qk-serializable: Ensure All Key Parts Are JSON-Serializable

## Explanation

Query keys are hashed using JSON serialization for cache lookups. Non-serializable values (functions, class instances, symbols, circular references) break caching and cause unexpected behavior. All parts of your query key must be JSON-serializable.

## Bad Example

```tsx
// Functions are not serializable
const { data } = useQuery({
  queryKey: ['todos', () => 'active'],  // Wrong: function in key
  queryFn: fetchTodos,
})

// Class instances lose their prototype
class Filter {
  constructor(public status: string) {}
  isActive() { return this.status === 'active' }
}
const filter = new Filter('active')
const { data: todos } = useQuery({
  queryKey: ['todos', filter],  // Wrong: class instance
  queryFn: () => fetchTodos(filter),
})

// Dates are technically serializable but become strings
const { data: events } = useQuery({
  queryKey: ['events', new Date()],  // Problematic: new Date() each render
  queryFn: () => fetchEvents(date),
})

// Symbols are not serializable
const { data: settings } = useQuery({
  queryKey: ['settings', Symbol('user')],  // Wrong: symbol
  queryFn: fetchSettings,
})
```

## Good Example

```tsx
// Use primitive values and plain objects
const { data } = useQuery({
  queryKey: ['todos', 'active'],
  queryFn: fetchTodos,
})

// Plain objects are fine
const filters = { status: 'active', priority: 'high' }
const { data: todos } = useQuery({
  queryKey: ['todos', filters],
  queryFn: () => fetchTodos(filters),
})

// For dates, use stable string representations
const dateKey = date.toISOString().split('T')[0]  // '2024-01-15'
const { data: events } = useQuery({
  queryKey: ['events', dateKey],
  queryFn: () => fetchEvents(date),
})

// Arrays of primitives work correctly
const { data: users } = useQuery({
  queryKey: ['users', { ids: [1, 2, 3] }],
  queryFn: () => fetchUsers([1, 2, 3]),
})
```

## Serializable Types

**Safe to use:**
- Strings, numbers, booleans, null
- Plain objects (no prototype methods)
- Arrays of serializable values
- undefined (stripped but handled)

**Avoid:**
- Functions
- Class instances
- Symbols
- Date objects (use ISO strings instead)
- Map/Set (use arrays/objects instead)
- Circular references

## Context

- TanStack Query uses deterministic JSON hashing
- Object property order doesn't matter: `{ a: 1, b: 2 }` equals `{ b: 2, a: 1 }`
- Keys with `undefined` properties are normalized: `{ a: 1, b: undefined }` equals `{ a: 1 }`
- Test serialization: `JSON.stringify(queryKey)` should work without errors

Source: [TanStack Agent Skills - tanstack-query/qk-serializable.md](https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/qk-serializable.md). Adapted with attribution; see the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
