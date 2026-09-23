---
title: "setup-query-client-context: Pass QueryClient Through Router Context"
whenToRead: "Before passing a TanStack Query client into TanStack Router loaders, especially when server rendering or tests need isolated clients."
impact: "HIGH"
impactDescription: "makes QueryClient injectable through Router context for typed loaders, SSR, and tests"
tags: "tanstack-router, tanstack-integration, tanstack-query, router-context, query-client"
attribution: [{"url":"https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-integration/rules/setup-query-client-context.md","description":"Underlying tanstack-agent-skills material at skills/tanstack-integration/rules/setup-query-client-context.md, commit 0e8bcdc6af4959739e0f6a2dfb35dc70d513940a; adapted under MIT, with notice retained in the public library."}]
---

## setup-query-client-context: Pass QueryClient Through Router Context

## Explanation

Pass the QueryClient instance through TanStack Router's context system rather than using a global. This enables proper SSR with per-request clients, testability, and type-safe access in loaders. Use `@tanstack/react-router-ssr-query` for automatic SSR integration.

## Bad Example

```tsx
// lib/query-client.ts - Global singleton
export const queryClient = new QueryClient()

// routes/posts.tsx - Importing global
import { queryClient } from '@/lib/query-client'

export const Route = createFileRoute('/posts')({
  loader: async () => {
    // Using global - breaks SSR, harder to test
    return queryClient.fetchQuery(postQueries.list())
  },
})
```

## Good Example: Modern Router Setup

```tsx
// routes/__root.tsx
import { createRootRouteWithContext } from '@tanstack/react-router'
import { QueryClient } from '@tanstack/react-query'

interface RouterContext {
  queryClient: QueryClient
}

export const Route = createRootRouteWithContext<RouterContext>()({
  component: RootComponent,
})

// router.tsx
import { QueryClient } from '@tanstack/react-query'
import { createRouter } from '@tanstack/react-router'
import { setupRouterSsrQueryIntegration } from '@tanstack/react-router-ssr-query'
import { routeTree } from './routeTree.gen'

export function getRouter() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
        staleTime: 1000 * 60 * 2, // 2 minutes
      },
    },
  })

  const router = createRouter({
    routeTree,
    context: { queryClient },
    defaultPreload: 'intent',
    defaultPreloadStaleTime: 0,
    scrollRestoration: true,
  })

  setupRouterSsrQueryIntegration({
    router,
    queryClient,
  })

  return router
}

declare module '@tanstack/react-router' {
  interface Register {
    router: ReturnType<typeof getRouter>
  }
}

// routes/posts.tsx - Access from context
export const Route = createFileRoute('/posts')({
  loader: async ({ context: { queryClient } }) => {
    // Type-safe access to queryClient from context
    await queryClient.ensureQueryData(postQueries.list())
  },
})
```

## Good Example: Root Route with Context

```tsx
// routes/__root.tsx
import { createRootRouteWithContext, Outlet, HeadContent, Scripts } from '@tanstack/react-router'
import { QueryClient } from '@tanstack/react-query'

interface RouterContext {
  queryClient: QueryClient
  user: User | null
}

export const Route = createRootRouteWithContext<RouterContext>()({
  component: RootComponent,
  beforeLoad: async ({ context }) => {
    // Prefetch auth or other global data
    await context.queryClient.ensureQueryData(authQueryOptions)
  },
})

function RootComponent() {
  return (
    <html>
      <head>
        <HeadContent />
      </head>
      <body>
        <Outlet />
        <Scripts />
      </body>
    </html>
  )
}
```

TanStack Start handles SSR and hydration automatically via the Vite plugin. No separate entry files needed.

## Good Example: Testing with Mock QueryClient

```tsx
// tests/posts.test.tsx
import { createRouter, RouterProvider } from '@tanstack/react-router'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render } from '@testing-library/react'

function renderWithProviders(route: string) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  })

  const router = createRouter({
    routeTree,
    context: { queryClient },
    Wrap: ({ children }) => (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    ),
  })

  return {
    ...render(<RouterProvider router={router} />),
    queryClient,
  }
}

test('loads posts', async () => {
  const { queryClient } = renderWithProviders('/posts')

  // Pre-populate cache for testing
  queryClient.setQueryData(['posts'], mockPosts)

  // ... assertions
})
```

## Context

- Router context flows to all loaders and beforeLoad hooks
- Creating QueryClient per request is essential for SSR
- Use `setupRouterSsrQueryIntegration` for automatic SSR handling
- Access queryClient via `context` parameter in loaders
- This pattern enables clean dependency injection for testing
- Install: `npm install @tanstack/react-router-ssr-query`

Source: [TanStack Agent Skills - tanstack-integration/setup-query-client-context.md](https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-integration/rules/setup-query-client-context.md). Adapted with attribution; see the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
