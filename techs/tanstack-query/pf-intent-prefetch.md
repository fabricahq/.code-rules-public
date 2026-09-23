---
title: "Prefetch likely next data on user intent"
whenToRead: "Before planning, writing, changing, or reviewing links, buttons, or routes that lead to screens backed by TanStack Query data, or diagnosing loading states after navigation."
impact: "MEDIUM"
impactDescription: "Starting a fetch only after navigation makes users wait for data they signaled they wanted moments earlier."
tags: "tanstack-query, prefetch, navigation, performance"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/pf-intent-prefetch.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule pf-intent-prefetch (MIT, notice retained in NOTICE.md): restructured to the rule template, fixed the timer ref for current React types, and added touch and router guidance."
---

## Prefetch likely next data on user intent

When a user signals that they are about to open a screen, such as hovering or focusing its link, prefetch that screen's queries with `queryClient.prefetchQuery`.

### Implementation

- Prefetch with the same query options factory the destination uses, so the prefetched entry is the one it reads.
- Trigger on hover and focus for pointer and keyboard users; on touch devices, trigger on `touchstart` or when the link scrolls into view.
- Rely on `staleTime`: `prefetchQuery` does nothing while the cached data is fresh, so repeated hovers do not refetch.
- Add a short delay, and cancel it when the pointer leaves, to skip prefetches from passing mouse movements.
- In a router with loaders, such as TanStack Router with `preload: 'intent'`, prefetch from the route loader instead of from each link.
- Prefetch only likely paths; prefetching every link on a long list wastes bandwidth.

### Rationale

Hover and focus usually precede a click by a few hundred milliseconds.
Starting the request then lets the data arrive before, or soon after, the next screen renders.

### Examples

**Incorrect (counterexample):**

```tsx
<Link to={`/posts/${post.id}`}>{post.title}</Link>
```

The post's data starts loading only after the detail page mounts.

**Correct:**

```tsx
function PostLink({ post }: { post: Post }) {
  const queryClient = useQueryClient();
  const timer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);

  function prefetch() {
    timer.current = setTimeout(() => {
      void queryClient.prefetchQuery(postQueries.detail(post.id));
    }, 100);
  }

  function cancel() {
    clearTimeout(timer.current);
  }

  return (
    <Link to={`/posts/${post.id}`} onMouseEnter={prefetch} onFocus={prefetch} onMouseLeave={cancel} onBlur={cancel}>
      {post.title}
    </Link>
  );
}
```

### Validation

Hover over a link, wait briefly, then open it, and check in the network panel that the detail request started on hover and that the page renders without a loading state.

Links to screens that load instantly, or rarely visited paths, do not need prefetching.
