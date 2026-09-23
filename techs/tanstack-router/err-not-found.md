---
title: "Throw notFound for missing resources and render it with notFoundComponent"
whenToRead: "Before planning, writing, changing, or reviewing TanStack Router loaders that fetch a resource by URL parameters, or not-found pages and fallbacks."
impact: "MEDIUM-HIGH"
impactDescription: "Throwing a generic error for a missing resource shows an error page instead of a not-found page, and missing not-found components leave unknown URLs without useful content."
tags: "tanstack-router, not-found, errors, 404"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/err-not-found.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule err-not-found (MIT, notice retained in NOTICE.md): restructured to the rule template and corrected how notFoundComponent receives notFound data."
---

## Throw notFound for missing resources and render it with notFoundComponent

When a loader finds that the resource named by the URL does not exist, throw `notFound()`, not a generic error.
Provide a `notFoundComponent` on the route or an ancestor, and a `defaultNotFoundComponent` on the router for everything else.

### Implementation

- Throw `notFound()` from a loader or `beforeLoad` when the requested resource does not exist.
- Keep ordinary thrown errors for failures, such as a network error or a server error, which the route's error component handles.
- Set `defaultNotFoundComponent` on the router, or `notFoundComponent` on the root route, so unmatched URLs show a useful page.
- Add a route-level `notFoundComponent` where a more specific message helps, such as "Post not found" with a link to the list.
- Pass context with `notFound({ data })`; the not-found component receives it as its `data` prop.
- In a not-found component, `useParams()` and `useSearch()` work, but the route's loader data may not be available.
- A thrown `notFound()` is handled by the same route or the nearest ancestor with a not-found component; target another route with `notFound({ routeId })`.
- With server rendering, check that not-found pages respond with a 404 status, so crawlers and monitoring treat them as missing.

### Rationale

A missing resource is an expected outcome that users should be able to act on, such as by returning to a list.
A generic error renders the error component, suggests something broke, and cannot be distinguished by crawlers or monitoring from real failures.
`notFound()` lets the router render the nearest not-found component and preserve the surrounding layout.

### Examples

**Incorrect (counterexample):**

```tsx
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await fetchPost(params.postId);
    if (!post) throw new Error('Not found');
    return post;
  },
});
```

The route shows its error component, as if the request had failed.

**Correct:**

```tsx
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await fetchPost(params.postId);
    if (!post) throw notFound({ data: { postId: params.postId } });
    return post;
  },
  notFoundComponent: ({ data }) => {
    const { postId } = data as { postId: string };
    return (
      <div>
        <h1>Post not found</h1>
        <p>No post exists with ID {postId}.</p>
        <Link to="/posts">Browse all posts</Link>
      </div>
    );
  },
});
```

### Validation

Visit a URL whose resource does not exist and an unmatched URL, and check that each shows a not-found page, not an error page or blank screen.
Check that loaders throw `notFound()` rather than generic errors for missing resources.

A generic error thrown for an actual failure, such as a server error, is not a violation.
