---
title: "nav-link-component: Prefer Link Component for Navigation"
whenToRead: "Before adding navigation from a clickable UI element to another TanStack Router route."
impact: "MEDIUM"
impactDescription: "preserves accessible anchor behavior, preloading, and active route state"
tags: "tanstack-router, link, navigation, accessibility, preloading"
attribution: [{"url":"https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/nav-link-component.md","description":"Underlying tanstack-agent-skills material at skills/tanstack-router/rules/nav-link-component.md, commit 0e8bcdc6af4959739e0f6a2dfb35dc70d513940a; adapted under MIT, with notice retained in the public library."}]
---

## nav-link-component: Prefer Link Component for Navigation

## Explanation

Use the `<Link>` component for navigation instead of `useNavigate()` when possible. Links render proper `<a>` tags with valid `href` attributes, enabling right-click -> open in new tab, better SEO, and accessibility.

## Bad Example

```tsx
// Using onClick with navigate - loses standard link behavior
function PostCard({ post }: { post: Post }) {
  const navigate = useNavigate()

  return (
    <div
      onClick={() => navigate({ to: '/posts/$postId', params: { postId: post.id } })}
      className="post-card"
    >
      <h2>{post.title}</h2>
      <p>{post.excerpt}</p>
    </div>
  )
}
// Problems:
// - No right-click -> open in new tab
// - No cmd/ctrl+click for new tab
// - Not announced as link to screen readers
// - No valid href for SEO
```

## Good Example

```tsx
import { Link } from '@tanstack/react-router'

function PostCard({ post }: { post: Post }) {
  return (
    <Link
      to="/posts/$postId"
      params={{ postId: post.id }}
      className="post-card"
    >
      <h2>{post.title}</h2>
      <p>{post.excerpt}</p>
    </Link>
  )
}
// Benefits:
// - Renders <a href="/posts/123">
// - Right-click menu works
// - Cmd/Ctrl+click opens new tab
// - Screen readers announce as link
// - Preloading works on hover
```

## Good Example: With Search Params

```tsx
function FilteredLink() {
  return (
    <Link
      to="/products"
      search={{ category: 'electronics', sort: 'price' }}
    >
      View Electronics
    </Link>
  )
}

// Preserving existing search params
function SortLink({ sort }: { sort: 'asc' | 'desc' }) {
  return (
    <Link
      to="."  // Current route
      search={(prev) => ({ ...prev, sort })}
    >
      Sort {sort === 'asc' ? 'Ascending' : 'Descending'}
    </Link>
  )
}
```

## Good Example: With Active States

```tsx
function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  return (
    <Link
      to={to}
      activeProps={{
        className: 'nav-link-active',
        'aria-current': 'page',
      }}
      inactiveProps={{
        className: 'nav-link',
      }}
      activeOptions={{
        exact: true,  // Only active on exact match
      }}
    >
      {children}
    </Link>
  )
}

// Or use render props for more control
function CustomNavLink({ to, children }: { to: string; children: React.ReactNode }) {
  return (
    <Link to={to}>
      {({ isActive }) => (
        <span className={isActive ? 'text-blue-600 font-bold' : 'text-gray-600'}>
          {children}
          {isActive && <CheckIcon className="ml-2" />}
        </span>
      )}
    </Link>
  )
}
```

## Good Example: With Preloading

```tsx
function PostList({ posts }: { posts: Post[] }) {
  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>
          <Link
            to="/posts/$postId"
            params={{ postId: post.id }}
            preload="intent"      // Preload on hover/focus
            preloadDelay={100}    // Wait 100ms before preloading
          >
            {post.title}
          </Link>
        </li>
      ))}
    </ul>
  )
}
```

## When to Use useNavigate Instead

```tsx
// 1. After form submission
const createPost = useMutation({
  mutationFn: submitPost,
  onSuccess: (data) => {
    navigate({ to: '/posts/$postId', params: { postId: data.id } })
  },
})

// 2. After authentication
async function handleLogin(credentials: Credentials) {
  await login(credentials)
  navigate({ to: '/dashboard' })
}

// 3. Programmatic redirects
useEffect(() => {
  if (!isAuthenticated) {
    navigate({ to: '/login', search: { redirect: location.pathname } })
  }
}, [isAuthenticated])
```

## Context

- `<Link>` renders actual `<a>` tags with proper `href`
- Supports all standard link behaviors (middle-click, cmd+click, etc.)
- Enables preloading on hover/focus
- Better for SEO - crawlers can follow links
- Reserve `useNavigate` for side effects and programmatic navigation
- Use `<Navigate>` component for immediate redirects on render

Source: [TanStack Agent Skills - tanstack-router/nav-link-component.md](https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/nav-link-component.md). Adapted with attribution; see the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
