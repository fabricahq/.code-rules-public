---
title: "Key each query by every input it uses"
whenToRead: "Before planning, writing, changing, or reviewing a TanStack Query key or query function, especially one that reads IDs, filters, search terms, dates, or other changing inputs."
impact: "HIGH"
impactDescription: "A key that omits an input makes different requests share one cache entry, so users see another input's data and changes do not refetch."
tags: "tanstack-query, query-keys, cache"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/qk-include-dependencies.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule qk-include-dependencies (MIT, notice retained in NOTICE.md): merged the array-key and serializable-key rules, restructured to the rule template, and corrected the serialization details against the query-core key hashing."
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/qk-serializable.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule qk-serializable (MIT, notice retained in NOTICE.md): merged the array-key and serializable-key rules, restructured to the rule template, and corrected the serialization details against the query-core key hashing."
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/qk-array-structure.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule qk-array-structure (MIT, notice retained in NOTICE.md): merged the array-key and serializable-key rules, restructured to the rule template, and corrected the serialization details against the query-core key hashing."
---

## Key each query by every input it uses

Put every value the query function reads into the query key, as plain serializable values.
The key must change whenever the request would change.

### Implementation

- Include each ID, filter, page, search term, and option the query function uses.
- Use an array whose parts are strings, numbers, booleans, `null`, plain objects, or arrays of these.
  TanStack Query hashes keys with `JSON.stringify`, sorting plain object properties, so `{ status, page }` and `{ page, status }` match.
- Convert other values to a stable, meaningful form before putting them in a key:
  - Dates: an ISO string or date string, such as `'2024-01-15'`.
  - `Map` and `Set`: an array or plain object; both serialize to `{}`, so different values collide.
  - Class instances: a plain object of the fields that matter; the class itself is lost.
  - Functions and symbols: never in a key; they serialize to `null` or disappear.
- Compute key parts from inputs that are stable across renders; `new Date()` in a key creates a new cache entry on every render.
- Keep the key and the query function together, such as in a `queryOptions` factory, so they cannot drift apart.

### Rationale

TanStack Query identifies cache entries by the hashed key.
If the query function reads a value that is not in the key, two different requests share one entry: switching users shows the previous user's data, and changing a filter does not refetch.
Values that do not serialize meaningfully either collide, as `Map` and `Set` do, or produce a new key every time.

### Examples

#### Application: A missing input

**Incorrect (counterexample):**

```tsx
function UserPosts({ userId }: { userId: string }) {
  const { data } = useQuery({
    queryKey: ['posts'],
    queryFn: () => fetchPostsByUser(userId),
  });
  // ...
}
```

All users share the `['posts']` entry, so navigating from one user to another shows the first user's posts until a refetch completes.

**Correct:**

```tsx
function UserPosts({ userId }: { userId: string }) {
  const { data } = useQuery({
    queryKey: ['posts', { userId }],
    queryFn: () => fetchPostsByUser(userId),
  });
  // ...
}
```

#### Application: A value that does not serialize meaningfully

**Incorrect (counterexample):**

```tsx
const { data } = useQuery({
  queryKey: ['events', selectedTags],
  queryFn: () => fetchEvents([...selectedTags]),
});
```

If `selectedTags` is a `Set`, every selection serializes to `{}`, so all selections share one cache entry.

**Correct:**

```tsx
const tags = [...selectedTags].sort();

const { data } = useQuery({
  queryKey: ['events', { tags }],
  queryFn: () => fetchEvents(tags),
});
```

### Validation

For each query, list the variables the query function reads and check that each appears in the key.
Check that `JSON.stringify(queryKey)` produces a distinct, stable string for each distinct request.
The TanStack Query ESLint plugin's `exhaustive-deps` rule can catch missing variables.

A value that does not affect the request, such as a callback used only for logging, does not belong in the key.
