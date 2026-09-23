---
title: "Deduplicate per-request server work with cache"
whenToRead: "Before planning, writing, changing, or reviewing React Server Component code that calls the same database query, authentication check, or other non-fetch operation from several components in one request."
impact: "MEDIUM"
impactDescription: "The same query or check repeated by several components in one request multiplies database and service load."
tags: "react, server-components, cache, deduplication"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/server-cache-react.md
    description: "Adapted from the Vercel Agent Skills rule server-cache-react: restructured to the rule template with scope limits and validation."
---

## Deduplicate per-request server work with cache

Wrap server data functions that several components call during one request in React's `cache`, so each distinct call runs once per request.

### Implementation

- Define the cached function at module level, and have every component call that same function.
- Pass primitive arguments, or the same object reference; `cache` compares arguments with `Object.is`, so a new object literal is always a miss.
- `cache` works only in Server Components and lasts for one server request; it does not share results across requests or users.
- In Next.js, `fetch` requests with the same URL and options are already memoized during rendering, so `cache` is for non-fetch work such as database queries and authentication checks.

### Rationale

In a component tree, several components often need the same data, such as the current user.
Passing it down through props couples them, but calling the query in each one repeats it.
`cache` lets each component call the function independently while the query runs once per request.

### Examples

**Incorrect (counterexample):**

```ts
export const getUser = cache(async (params: { id: string }) => {
  return db.user.findUnique({ where: { id: params.id } });
});

await getUser({ id: userId });
await getUser({ id: userId }); // new object: runs the query again
```

**Correct:**

```ts
export const getUser = cache(async (id: string) => {
  return db.user.findUnique({ where: { id } });
});

await getUser(userId);
await getUser(userId); // same argument: returns the cached result
```

### Validation

Log or count the underlying queries while rendering one page, and check that each distinct query runs once.
Check that cached functions take primitive arguments.

A query called once per request does not need `cache`.
