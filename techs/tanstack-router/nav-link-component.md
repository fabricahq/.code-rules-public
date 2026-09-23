---
title: "Use Link for navigation users can open, and redirect in the router"
whenToRead: "Before planning, writing, changing, or reviewing navigation in a TanStack Router app, such as clickable cards, menus, buttons that change pages, or redirects after checks."
impact: "MEDIUM"
impactDescription: "Navigation built from click handlers loses link behavior such as opening in a new tab and screen reader announcements, and redirects in Effects flash the wrong page."
tags: "tanstack-router, navigation, Link, accessibility, redirects"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/nav-link-component.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule nav-link-component (MIT, notice retained in NOTICE.md): restructured to the rule template and replaced the Effect-based redirect with beforeLoad and Navigate."
---

## Use Link for navigation users can open, and redirect in the router

Render navigation the user triggers directly as a `<Link>`.
Use `useNavigate` only for navigation that follows an action, such as after a form submits, and redirect with `beforeLoad` or `<Navigate>` rather than an Effect.

### Implementation

- Use `<Link>` for anything that behaves like a link, including cards and menu items, so it renders an `<a>` with an `href`.
- Pass `params` and `search` to `Link` rather than building URL strings, so they are type-checked.
- Use `search={(prev) => ({ ...prev, sort })}` to change one search param while keeping the others.
- Use `activeProps` or the render-function children to style the active link.
- Use `useNavigate` after an action completes, such as a successful mutation or sign-in.
- Redirect unauthorized or misplaced users by throwing `redirect()` from `beforeLoad`, or render `<Navigate>` when the decision depends on render-time state.

### Rationale

An `<a href>` gets browser behavior that click handlers do not: opening in a new tab or window, copying the address, middle-clicking, crawling, and being announced as a link.
`Link` also triggers route preloading on intent.
A redirect in an Effect runs after the wrong page renders, so users see a flash of content they should not see.

### Examples

#### Application: A clickable card

**Incorrect (counterexample):**

```tsx
function PostCard({ post }: { post: Post }) {
  const navigate = useNavigate();
  return (
    <div onClick={() => navigate({ to: '/posts/$postId', params: { postId: post.id } })}>
      <h2>{post.title}</h2>
    </div>
  );
}
```

The card cannot be opened in a new tab, is not announced as a link, and cannot be reached with the keyboard.

**Correct:**

```tsx
function PostCard({ post }: { post: Post }) {
  return (
    <Link to="/posts/$postId" params={{ postId: post.id }}>
      <h2>{post.title}</h2>
    </Link>
  );
}
```

#### Application: A redirect

**Incorrect (counterexample):**

```tsx
useEffect(() => {
  if (!isAuthenticated) navigate({ to: '/login' });
}, [isAuthenticated, navigate]);
```

The protected page renders before the redirect runs.

**Correct:**

```tsx
export const Route = createFileRoute('/_authenticated')({
  beforeLoad: ({ context, location }) => {
    if (!context.auth.isAuthenticated) {
      throw redirect({ to: '/login', search: { redirect: location.href } });
    }
  },
});
```

### Validation

Check that elements that navigate on click render as links, by middle-clicking or inspecting for an `href`.
Search for `navigate` calls inside `useEffect` and replace redirects with `beforeLoad` or `<Navigate>`.

`useNavigate` after a form submission or other completed action is not a violation.
