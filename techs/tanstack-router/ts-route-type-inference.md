---
title: "Register the router and read route data through typed route APIs"
whenToRead: "Before planning, writing, changing, or reviewing TanStack Router setup or components that read params, search params, loader data, or context, or that navigate."
impact: "MEDIUM"
impactDescription: "Without router registration and route-specific hooks, invalid routes, missing params, and wrong search param types are not caught by TypeScript."
tags: "tanstack-router, typescript, type-safety, Register"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/ts-register-router.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule ts-register-router (MIT, notice retained in NOTICE.md): merged the router registration and from-parameter rules, restructured to the rule template, and corrected the counterexample, since hooks without from or strict false do not compile."
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/ts-use-from-param.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule ts-use-from-param (MIT, notice retained in NOTICE.md): merged the router registration and from-parameter rules, restructured to the rule template, and corrected the counterexample, since hooks without from or strict false do not compile."
---

## Register the router and read route data through typed route APIs

Register the router type once with the `Register` interface, and read params, search params, and loader data through route-specific APIs, such as `Route.useParams()`, `getRouteApi('/path')`, or hooks with `from`.

### Implementation

- Declare `Register` next to where the router is created: `declare module '@tanstack/react-router' { interface Register { router: ReturnType<typeof getRouter> } }`.
- In a route file, use the route's own hooks, such as `Route.useParams()` and `Route.useLoaderData()`.
- In a component split from its route, use `getRouteApi('/posts/$postId')`.
- Pass `from` to generic hooks, such as `useParams({ from: '/posts/$postId' })`, when neither of the above is convenient.
- Use `strict: false` only in components shared across routes, such as breadcrumbs, and handle every field as possibly missing.
- Navigate with `Link` or `navigate` using route paths and `params`, not hand-built URL strings, so TypeScript checks them.

### Rationale

TanStack Router infers route paths, params, search params, and loader data from the route tree, but global hooks and `Link` see those types only after the router is registered.
Route-specific APIs return exact types for one route, while `strict: false` returns a loose union where every field may be missing.

### Examples

#### Application: Registration

**Incorrect (counterexample):**

```tsx
export const router = createRouter({ routeTree });
```

Without registration, `Link` and `navigate` accept any `to` value, so a mistyped route compiles.

**Correct:**

```tsx
export const router = createRouter({ routeTree });

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}
```

#### Application: Reading params in a route component

**Incorrect (counterexample):**

```tsx
function PostDetail() {
  const params = useParams({ strict: false });
  return <Post id={params.postId!} />;
}
```

`postId` is typed as possibly missing, so the component needs a non-null assertion that hides real mistakes.

**Correct:**

```tsx
const postRoute = getRouteApi('/posts/$postId');

function PostDetail() {
  const { postId } = postRoute.useParams();
  return <Post id={postId} />;
}
```

### Validation

Run the type checker and check that a navigation to a nonexistent route or with missing params fails to compile.
Search route-specific components for `strict: false` and non-null assertions on params.

`strict: false` in a component genuinely shared across routes is not a violation.
