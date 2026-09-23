---
title: "Mask modal routes with the resource's canonical URL"
whenToRead: "Before planning, writing, changing, or reviewing TanStack Router UI that opens a resource in a modal, drawer, or quick view over another page, or uses route masks."
impact: "LOW"
impactDescription: "Modals opened with local state lose their place on back, refresh, and sharing, while masks pointing at the wrong URL share links that do not show the resource."
tags: "tanstack-router, route-masking, modals, navigation"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/nav-route-masks.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule nav-route-masks (MIT, notice retained in NOTICE.md): restructured to the rule template and corrected the example to mask the modal route as the resource's canonical URL, matching documented sharing and reload behavior."
---

## Mask modal routes with the resource's canonical URL

When a resource opens in a modal over another page, give the modal its own route and navigate to it with a mask whose URL is the resource's full page, such as navigating to `/photos/5/modal` masked as `/photos/5`.

### Implementation

- Create a route for the modal view, nested under the page it overlays, such as `/photos/$photoId/modal`.
- Navigate to it with `mask` pointing at the resource's standalone page, such as `/photos/$photoId`.
- Make the standalone page work on its own, because anyone who opens a shared link lands there.
- Masks are kept in local history state: back and forward work, and a local reload keeps the mask unless `unmaskOnReload` is set.
- A copied or shared URL loses the mask and opens the standalone page.
- Use `createRouteMask` on the router for masks that apply to every navigation between two routes.

### Rationale

A modal controlled by local state has no URL, so back does not close it, refresh loses it, and it cannot be shared.
A route gives the modal history and loading like any page.
Masking it with the resource's canonical URL means the address bar shows a meaningful URL, and anyone who opens that URL sees the resource as a full page.

### Examples

**Incorrect (counterexample):**

```tsx
<Link to="/posts/$postId" params={{ postId: post.id }} mask={{ to: '/posts' }}>
  {post.title}
</Link>
```

The address bar shows `/posts`, so a copied link opens the list instead of the post.

**Correct:**

```tsx
<Link
  to="/posts/$postId/modal"
  params={{ postId: post.id }}
  mask={{ to: '/posts/$postId', params: { postId: post.id } }}
>
  {post.title}
</Link>
```

The modal opens over the list, the address bar shows the post's own URL, and sharing it opens the full post page.

### Validation

Open the modal, then check that the address bar shows the resource's URL, that back closes the modal, and that opening the copied URL in a new tab shows the resource's full page.

A modal for transient UI with no shareable resource, such as a confirmation dialog, does not need a route.
