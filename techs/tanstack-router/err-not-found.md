---
title: "err-not-found: Handle Not-Found Routes Properly"
whenToRead: "Before handling missing routes or missing route data with TanStack Router, at either a root or nested route."
impact: "HIGH"
impactDescription: "prevents blank screens and generic errors for missing route data"
tags: "tanstack-router, not-found, 404, errors, ux"
attribution: [{"url":"https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/err-not-found.md","description":"Underlying tanstack-agent-skills material at skills/tanstack-router/rules/err-not-found.md, commit 0e8bcdc6af4959739e0f6a2dfb35dc70d513940a; adapted under MIT, with notice retained in the public library."}]
---

## err-not-found: Handle Not-Found Routes Properly

## Explanation

Configure `notFoundComponent` to handle 404 errors gracefully. TanStack Router provides not-found handling at multiple levels: root, route-specific, and programmatic via `notFound()`. Proper configuration prevents blank screens and improves UX.

## Bad Example

```tsx
// No not-found handling - shows blank screen or error
const router = createRouter({
  routeTree,
  // Missing defaultNotFoundComponent
})

// Or throwing generic error
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await fetchPost(params.postId)
    if (!post) {
      throw new Error('Not found')  // Generic error, not proper 404
    }
    return post
  },
})
```

## Good Example: Root-Level Not Found

```tsx
// routes/__root.tsx
export const Route = createRootRoute({
  component: RootComponent,
  notFoundComponent: GlobalNotFound,
})

function GlobalNotFound() {
  return (
    <div className="not-found">
      <h1>404 - Page Not Found</h1>
      <p>The page you're looking for doesn't exist.</p>
      <Link to="/">Go Home</Link>
    </div>
  )
}

// router.tsx - Can also set default
const router = createRouter({
  routeTree,
  defaultNotFoundComponent: () => (
    <div>
      <h1>404</h1>
      <Link to="/">Return Home</Link>
    </div>
  ),
})
```

## Good Example: Route-Specific Not Found

```tsx
// routes/posts/$postId.tsx
import { createFileRoute, notFound } from '@tanstack/react-router'

export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await fetchPost(params.postId)
    if (!post) {
      throw notFound()  // Proper 404 handling
    }
    return post
  },
  notFoundComponent: PostNotFound,  // Custom 404 for this route
  component: PostPage,
})

function PostNotFound() {
  const { postId } = Route.useParams()

  return (
    <div>
      <h1>Post Not Found</h1>
      <p>No post exists with ID: {postId}</p>
      <Link to="/posts">Browse all posts</Link>
    </div>
  )
}
```

## Good Example: Not Found with Data

```tsx
export const Route = createFileRoute('/users/$username')({
  loader: async ({ params }) => {
    const user = await fetchUser(params.username)
    if (!user) {
      throw notFound({
        // Pass data to notFoundComponent
        data: {
          username: params.username,
          suggestions: await fetchSimilarUsernames(params.username),
        },
      })
    }
    return user
  },
  notFoundComponent: UserNotFound,
})

function UserNotFound() {
  const { data } = Route.useMatch()

  return (
    <div>
      <h1>User @{data?.username} not found</h1>
      {data?.suggestions?.length > 0 && (
        <div>
          <p>Did you mean:</p>
          <ul>
            {data.suggestions.map((username) => (
              <li key={username}>
                <Link to="/users/$username" params={{ username }}>
                  @{username}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
```

## Good Example: Catch-All Route

```tsx
// routes/$.tsx - Catch-all splat route
export const Route = createFileRoute('/$')({
  component: CatchAllNotFound,
})

function CatchAllNotFound() {
  const { _splat } = Route.useParams()

  return (
    <div>
      <h1>Page Not Found</h1>
      <p>No page exists at: /{_splat}</p>
      <Link to="/">Go to homepage</Link>
    </div>
  )
}
```

## Good Example: Nested Not Found Bubbling

```tsx
// Not found bubbles up through route tree
// routes/posts.tsx
export const Route = createFileRoute('/posts')({
  notFoundComponent: PostsNotFound,  // Catches child 404s too
})

// routes/posts/$postId.tsx
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await fetchPost(params.postId)
    if (!post) throw notFound()
    return post
  },
  // No notFoundComponent - bubbles to parent
})

// routes/posts/$postId/comments.tsx
export const Route = createFileRoute('/posts/$postId/comments')({
  loader: async ({ params }) => {
    const comments = await fetchComments(params.postId)
    if (!comments) throw notFound()  // Bubbles to /posts notFoundComponent
    return comments
  },
})
```

## Context

- `notFound()` throws a special error caught by nearest `notFoundComponent`
- Not found bubbles up the route tree if not handled locally
- Use `defaultNotFoundComponent` on router for global fallback
- Pass data to `notFound({ data })` for contextual 404 pages
- Catch-all routes (`/$`) can handle truly unknown paths
- Different from error boundaries - specifically for 404 cases

Source: [TanStack Agent Skills - tanstack-router/err-not-found.md](https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/err-not-found.md). Adapted with attribution; see the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
