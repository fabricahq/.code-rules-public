---
title: "Provide shared dependencies through typed router context"
whenToRead: "Before planning, writing, changing, or reviewing how TanStack Router loaders and beforeLoad functions access shared clients and services, such as a QueryClient, authentication state, or an API client, including SSR setup and tests."
impact: "HIGH"
impactDescription: "Loaders that import module-level singletons share state across server requests and cannot be given test doubles."
tags: "tanstack-router, context, dependency-injection, ssr, tanstack-query"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/ctx-root-context.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule ctx-root-context (MIT, notice retained in NOTICE.md): merged the root-context and QueryClient-context rules, restructured to the rule template, and removed a test example that ignored its route argument."
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-integration/rules/setup-query-client-context.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule setup-query-client-context (MIT, notice retained in NOTICE.md): merged the root-context and QueryClient-context rules, restructured to the rule template, and removed a test example that ignored its route argument."
---

## Provide shared dependencies through typed router context

Declare the dependencies routes share, such as the `QueryClient` and authentication state, as the root route's context type with `createRootRouteWithContext`, and pass instances when creating the router.
Read them from `context` in loaders and `beforeLoad`, instead of importing module-level singletons.

### Implementation

- Define a `RouterContext` interface and create the root route with `createRootRouteWithContext<RouterContext>()`.
- Create the router in a function, such as `getRouter()`, that builds a new `QueryClient` and other request-specific dependencies and passes them in `createRouter({ context })`.
- With server rendering and TanStack Query, call `setupRouterSsrQueryIntegration({ router, queryClient })` from `@tanstack/react-router-ssr-query` to wire dehydration, hydration, and the provider.
- Extend context for a subtree by returning values from `beforeLoad`, such as the authenticated user for protected routes.
- In tests, create the router with fresh dependencies and a memory history, so each test gets isolated state.

### Rationale

On a server, a module-level `QueryClient` is shared by every request the process handles, so one user's cached data can appear in another's response.
Context created per router instance keeps each request isolated, gives loaders typed access to their dependencies, and lets tests provide their own.

### Examples

**Incorrect (counterexample):**

```tsx
// lib/query-client.ts
export const queryClient = new QueryClient();

// routes/posts.tsx
export const Route = createFileRoute('/posts')({
  loader: () => queryClient.ensureQueryData(postQueries.list()),
});
```

Every server request shares one cache, and tests cannot replace the client.

**Correct:**

```tsx
// routes/__root.tsx
interface RouterContext {
  queryClient: QueryClient;
}

export const Route = createRootRouteWithContext<RouterContext>()({
  component: RootComponent,
});
```

```tsx
// router.tsx
export function getRouter() {
  const queryClient = new QueryClient({ defaultOptions: { queries: { staleTime: 60 * 1000 } } });
  const router = createRouter({ routeTree, context: { queryClient }, defaultPreloadStaleTime: 0 });
  setupRouterSsrQueryIntegration({ router, queryClient });
  return router;
}
```

```tsx
// routes/posts.tsx
export const Route = createFileRoute('/posts')({
  loader: ({ context: { queryClient } }) => queryClient.ensureQueryData(postQueries.list()),
});
```

### Validation

Search route files for imports of shared clients, such as a module-level `queryClient`, and check that loaders use `context` instead.
Check that server rendering creates a new router, with new dependencies, per request.

A module-level import of a stateless utility, such as a pure formatting function, is not a violation.
