---
title: "Set app-wide navigation behavior in router defaults"
whenToRead: "Before planning, writing, changing, or reviewing a TanStack Router createRouter call, or deciding app-wide preloading, error, not-found, pending, or scroll restoration behavior."
impact: "MEDIUM"
impactDescription: "Without router defaults, every navigation waits for data after the click, unexpected errors and unknown URLs fall back to bare built-in screens, and back navigation loses scroll position."
tags: "tanstack-router, createRouter, preload, errors, scroll-restoration"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/tree/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules
    description: "Adapted from two rules in Deckard Gerritsen's TanStack Agent Skills (router-default-options and preload-intent; MIT, notice retained in NOTICE.md): merged the intent-preloading rule, restructured to the rule template, removed an incorrect structural sharing default, and added the Query error reset to the retry example."
---

## Set app-wide navigation behavior in router defaults

Configure behavior that should apply to every route in `createRouter`: preloading on intent, a default error component with retry, a default not-found component, and scroll restoration.
Override it per route only where a route needs something different.

### Implementation

- Set `defaultPreload: 'intent'` so links preload their route's code and loaders on hover or focus.
  Use `defaultPreloadDelay` to skip passing mouse movements.
- Override per link with `preload={false}` for routes that are expensive or have side effects, or `preload="viewport"` for touch-heavy layouts where hover does not happen.
- When the app uses TanStack Query, set `defaultPreloadStaleTime: 0` so Query controls freshness.
  Without Query, preloaded data stays fresh for 30 seconds by default.
- Set `defaultErrorComponent` with a retry that calls `router.invalidate()`, and, when using TanStack Query, also resets query errors.
- Set `defaultNotFoundComponent` for unmatched URLs.
- Set `scrollRestoration: true` so back and forward navigation return users to where they were.
- Tune `defaultPendingComponent`, `defaultPendingMs`, and `defaultPendingMinMs` so slow navigations show progress without flashing it on fast ones.

### Rationale

Router defaults are applied to every route, so setting them once keeps behavior consistent and avoids each route re-implementing error and loading handling.
Preloading on intent starts a route's work a few hundred milliseconds before the click.
Without scroll restoration, back navigation drops users at the top of long lists.

### Examples

**Incorrect (counterexample):**

```tsx
const router = createRouter({ routeTree, context: { queryClient } });
```

Every navigation starts loading only after the click, errors show the built-in screen, and back navigation loses scroll position.

**Correct:**

```tsx
function DefaultErrorComponent({ error }: ErrorComponentProps) {
  const router = useRouter();
  const queryErrorResetBoundary = useQueryErrorResetBoundary();

  return (
    <div role="alert">
      <p>Something went wrong{error instanceof Error ? `: ${error.message}` : '.'}</p>
      <button
        onClick={() => {
          queryErrorResetBoundary.reset();
          void router.invalidate();
        }}
      >
        Try again
      </button>
    </div>
  );
}

const router = createRouter({
  routeTree,
  context: { queryClient },
  defaultPreload: 'intent',
  defaultPreloadStaleTime: 0,
  defaultErrorComponent: DefaultErrorComponent,
  defaultNotFoundComponent: () => <p>Page not found.</p>,
  scrollRestoration: true,
});
```

### Validation

Hover a link and check in the network panel that the route's data starts loading before the click.
Force a loader error and check that the default error component appears and its retry refetches.
Navigate back from a scrolled list and check that the scroll position returns.

A route-level override of a default, such as `preload: false` on a route with side effects, is not a violation.
