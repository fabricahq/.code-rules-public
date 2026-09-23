---
title: "Load route data in loaders, in parallel"
whenToRead: "Before planning, writing, changing, or reviewing how a TanStack Router route fetches its data, including loaders, beforeLoad, and components that fetch on mount."
impact: "HIGH"
impactDescription: "Fetching in components or in beforeLoad starts requests late or in sequence, which adds loading states and waterfalls to every navigation."
tags: "tanstack-router, loaders, beforeLoad, data-loading, waterfalls"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/tree/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules
    description: "Adapted from two rules in Deckard Gerritsen's TanStack Agent Skills (load-use-loaders and load-parallel; MIT, notice retained in NOTICE.md): merged the parallel-loading rule, restructured to the rule template, and corrected the claim that child loaders wait for parent loaders."
---

## Load route data in loaders, in parallel

Fetch the data a route needs in its `loader`, start independent requests together, and keep `beforeLoad` for checks and context that must come first, such as authentication and redirects.

### Implementation

- Put data fetching in `loader`, not in a component Effect, so it starts during navigation and can run on preload.
- Start independent requests in a loader together with `Promise.all`; await in sequence only when one request needs another's result.
- Keep `beforeLoad` short.
  `beforeLoad` functions run in order from parent to child, and loaders run after all of them, so a slow `beforeLoad` delays every loader below it.
- Rely on the router to run the loaders of nested matched routes in parallel; a child loader does not wait for its parent's loader.
- Pass the loader's `abortController.signal` to requests that should stop when the navigation is superseded.
- When the app uses TanStack Query, have loaders fill the Query cache instead of returning data directly.

### Rationale

A component that fetches on mount starts its request only after the route renders, so every navigation shows a loading state and nested components fetch in a chain.
Loaders start work as soon as the route matches, and the router runs matched routes' loaders concurrently.
`beforeLoad` is sequential by design, so data fetching placed there becomes a waterfall.

### Examples

#### Application: Fetching in a component

**Incorrect (counterexample):**

```tsx
function PostsPage() {
  const [posts, setPosts] = useState<Array<Post>>([]);

  useEffect(() => {
    fetchPosts().then(setPosts);
  }, []);
  // ...
}
```

The request starts only after the page renders, and it cannot run on hover preload.

**Correct:**

```tsx
export const Route = createFileRoute('/posts')({
  loader: () => fetchPosts(),
  component: PostsPage,
});

function PostsPage() {
  const posts = Route.useLoaderData();
  // ...
}
```

#### Application: Data fetched in beforeLoad or in sequence

**Incorrect (counterexample):**

```tsx
export const Route = createFileRoute('/dashboard')({
  beforeLoad: async () => {
    const user = await fetchUser();
    const stats = await fetchStats(user.id);
    const activity = await fetchActivity(user.id);
    return { user, stats, activity };
  },
});
```

Every child route's `beforeLoad` and loader waits for three sequential requests.

**Correct:**

```tsx
export const Route = createFileRoute('/dashboard')({
  beforeLoad: async () => ({ user: await fetchUser() }),
  loader: async ({ context }) => {
    const [stats, activity] = await Promise.all([fetchStats(context.user.id), fetchActivity(context.user.id)]);
    return { stats, activity };
  },
});
```

`beforeLoad` provides only the user that child routes need, and the loader fetches the rest in parallel.

### Validation

Navigate to the route with network throttling and check that its requests start during navigation, not after render, and that independent requests overlap.
Search `beforeLoad` functions for data fetching that child routes do not need.

Fetching in `beforeLoad` is not a violation when child routes need the result, such as the current user for an authorization check.
