---
title: "Split route components out of the main bundle"
whenToRead: "Before planning, writing, changing, or reviewing TanStack Router route files, bundler plugin configuration, or lazy route files, especially routes that import large components or libraries."
impact: "MEDIUM"
impactDescription: "Route components bundled together load every page's code, including heavy libraries, before the first page is interactive."
tags: "tanstack-router, code-splitting, lazy, bundling"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/tree/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules
    description: "Adapted from two rules in Deckard Gerritsen's TanStack Agent Skills (split-lazy-routes and org-virtual-routes; MIT, notice retained in NOTICE.md): merged the virtual-routes rule, restructured to the rule template, made automatic code splitting the primary approach, and updated the deprecated plugin export."
---

## Split route components out of the main bundle

Load each route's components only when that route is visited.
Prefer the router plugin's automatic code splitting; use `.lazy.tsx` files when you need manual control.

### Implementation

- Enable `autoCodeSplitting: true` in the router bundler plugin, imported as `tanstackRouter` from `@tanstack/router-plugin/vite` or the matching bundler entry.
  The older `TanStackRouterVite` export is deprecated.
- Without automatic splitting, move `component`, `pendingComponent`, `errorComponent`, and `notFoundComponent` into a `.lazy.tsx` file created with `createLazyFileRoute`.
- Keep options needed before rendering in the main route file: `loader`, `beforeLoad`, `validateSearch`, `loaderDeps`, and context.
- A route with only a `.lazy.tsx` file gets a generated virtual route, so an empty main route file is unnecessary.
- In components split from the route file, use `getRouteApi('/path')` for typed hooks instead of importing the route.

### Rationale

Loaders and search validation must run before a route renders, so they stay in the main bundle.
Components, and the heavy libraries they import, are needed only when their route renders, so splitting them keeps the initial download small.
Automatic splitting does this for every route without a second file per route.

### Examples

**Incorrect (counterexample):**

```tsx
// routes/dashboard.tsx
import { HeavyChart } from 'heavy-chart-library';

export const Route = createFileRoute('/dashboard')({
  loader: ({ context }) => context.queryClient.ensureQueryData(dashboardQueries.stats()),
  component: () => <HeavyChart />,
});
```

Without code splitting, the chart library ships in the initial bundle for every visitor.

**Correct:**

```ts
// vite.config.ts
import { tanstackRouter } from '@tanstack/router-plugin/vite';

export default defineConfig({
  plugins: [tanstackRouter({ target: 'react', autoCodeSplitting: true }), react()],
});
```

The same route file now loads its component, and the chart library, only when `/dashboard` renders.

### Validation

Inspect the build output and check that each route's component is in its own chunk, and that heavy libraries are not in the entry chunk.

A small app whose whole bundle loads quickly does not need route splitting.
