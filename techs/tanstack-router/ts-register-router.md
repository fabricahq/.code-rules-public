---
title: "ts-register-router: Register Router Type for Global Inference"
whenToRead: "Before wiring TypeScript types for TanStack Router hooks and navigation across an application."
impact: "MEDIUM"
impactDescription: "enables route, param, search, and navigation inference across the app"
tags: "tanstack-router, type-safety, router-registration, navigation, inference"
attribution: [{"url":"https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/ts-register-router.md","description":"Underlying tanstack-agent-skills material at skills/tanstack-router/rules/ts-register-router.md, commit 0e8bcdc6af4959739e0f6a2dfb35dc70d513940a; adapted under MIT, with notice retained in the public library."}]
---

## ts-register-router: Register Router Type for Global Inference

## Explanation

Register your router instance with TypeScript's module declaration to enable type inference across your entire application. Without registration, hooks like `useNavigate`, `useParams`, and `useSearch` won't know your route structure.

## Bad Example

```tsx
// router.tsx - Missing type registration
import { createRouter, createRootRoute } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'

export const router = createRouter({ routeTree })

// components/Navigation.tsx
import { useNavigate } from '@tanstack/react-router'

function Navigation() {
  const navigate = useNavigate()

  // TypeScript doesn't know valid routes - no autocomplete or type checking
  navigate({ to: '/posts/$postId' })  // No error even if route doesn't exist
}
```

## Good Example

```tsx
// router.tsx
import { createRouter } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'

export const router = createRouter({ routeTree })

// Register the router instance for type inference
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}

// components/Navigation.tsx
import { useNavigate } from '@tanstack/react-router'

function Navigation() {
  const navigate = useNavigate()

  // Full type safety - TypeScript knows all valid routes
  navigate({ to: '/posts/$postId', params: { postId: '123' } })

  // Type error if route doesn't exist
  navigate({ to: '/invalid-route' })  // Error: Type '"/invalid-route"' is not assignable...

  // Autocomplete for params
  navigate({
    to: '/users/$userId/posts/$postId',
    params: { userId: '1', postId: '2' },  // Both required
  })
}
```

## Benefits of Registration

```tsx
// After registration, all these get full type inference:

// 1. Navigation
const navigate = useNavigate()
navigate({ to: '/posts/$postId', params: { postId: '123' } })

// 2. Link component
<Link to="/posts/$postId" params={{ postId: '123' }}>View Post</Link>

// 3. useParams hook
const { postId } = useParams({ from: '/posts/$postId' })  // postId: string

// 4. useSearch hook
const search = useSearch({ from: '/posts' })  // Knows search param types

// 5. useLoaderData hook
const data = useLoaderData({ from: '/posts/$postId' })  // Knows loader return type
```

## File-Based Routing Setup

```tsx
// With file-based routing, routeTree is auto-generated
// router.tsx
import { createRouter } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'  // Generated file

export const router = createRouter({
  routeTree,
  defaultPreload: 'intent',
})

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
```

## Context

- Must be done once, typically in your router configuration file
- Enables IDE autocomplete for routes, params, and search params
- Catches invalid routes at compile time
- Works with both file-based and code-based routing
- Required for full TypeScript benefits of TanStack Router

Source: [TanStack Agent Skills - tanstack-router/ts-register-router.md](https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/ts-register-router.md). Adapted with attribution; see the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
