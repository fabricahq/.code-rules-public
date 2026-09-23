---
title: "Share client data requests through a caching data layer"
whenToRead: "Before planning, writing, changing, or reviewing client-side data fetching in React components, especially data that several components need or code that fetches in useEffect."
impact: "MEDIUM-HIGH"
impactDescription: "Fetching in each component's Effect duplicates requests, leaves data stale, and requires hand-written loading, error, and race handling."
tags: "react, data-fetching, swr, tanstack-query"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/client-swr-dedup.md
    description: "Adapted from the Vercel Agent Skills rule client-swr-dedup: generalized from SWR to any caching data layer, restructured to the rule template, and corrected the SWR import examples."
---

## Share client data requests through a caching data layer

Fetch server data in client components through a caching data library, such as TanStack Query or SWR, keyed by the resource, instead of fetching in each component's Effect.

### Implementation

- Use one data library per app, and give each resource a stable key.
- Let components that need the same resource call the same query with the same key; the library deduplicates concurrent requests and shares the cached result.
- Configure freshness per resource: long-lived data can skip revalidation, and frequently changing data can revalidate on focus or on an interval.
- Perform writes through the library's mutation API and update or invalidate the affected keys afterward.
- In frameworks that load data on the server, such as Server Components or route loaders, use those for the initial data and the client library for client-driven updates.

### Rationale

A `fetch` in `useEffect` runs separately in every component instance, starts only after render, and needs hand-written loading state, error handling, and protection against responses arriving out of order.
A caching data layer handles deduplication, caching, revalidation, and races once for the whole app.

### Examples

**Incorrect (counterexample):**

```tsx
function UserList() {
  const [users, setUsers] = useState<Array<User>>([]);

  useEffect(() => {
    fetch('/api/users')
      .then((response) => response.json())
      .then(setUsers);
  }, []);
  // ...
}
```

Every mounted `UserList` sends its own request, and errors are silently ignored.

**Correct (SWR):**

```tsx
import useSWR from 'swr';

function UserList() {
  const { data: users, error, isLoading } = useSWR('/api/users', fetchJson);
  // ...
}
```

**Correct (TanStack Query):**

```tsx
import { useQuery } from '@tanstack/react-query';

function UserList() {
  const { data: users, error, isPending } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetchJson('/api/users'),
  });
  // ...
}
```

Both libraries share one request among all components using the same key.

### Validation

Search client components for `fetch` or API calls inside `useEffect`.
Each should be a query or mutation through the app's data library, or have a documented reason not to be.

A one-off request in an event handler, such as submitting a form in an app without a data library, is not a violation.
