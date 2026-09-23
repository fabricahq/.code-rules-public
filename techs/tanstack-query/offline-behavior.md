---
title: "Make offline behavior explicit"
whenToRead: "Before planning, writing, changing, or reviewing TanStack Query configuration for apps that must work offline, restore data after a reload, or use local data sources, such as networkMode settings or cache persistence."
impact: "LOW-MEDIUM"
impactDescription: "Queries and mutations pause silently while offline, and a persisted cache without versioning or filtering can restore outdated or sensitive data."
tags: "tanstack-query, offline, networkMode, persistence"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/network-mode.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule network-mode (MIT, notice retained in NOTICE.md): merged the network-mode and persistence rules into one offline rule, restructured to the rule template, and replaced APIs that do not exist with useIsRestoring and the async storage persister."
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/persist-queries.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule persist-queries (MIT, notice retained in NOTICE.md): merged the network-mode and persistence rules into one offline rule, restructured to the rule template, and replaced APIs that do not exist with useIsRestoring and the async storage persister."
---

## Make offline behavior explicit

When an app must keep working offline or restore data after a reload, choose each query's network mode from where its data comes from, show users when work is paused, and persist only versioned, non-sensitive cache entries.

### Implementation

- Keep the default `networkMode: 'online'` for queries that need the network; they pause while offline.
- Use `networkMode: 'always'` for query functions that read local data or fall back to it, so they run offline.
- Use `networkMode: 'offlineFirst'` when a service worker or HTTP cache may answer without a connection.
- Show paused work: a query with `fetchStatus === 'paused'` is waiting for the network, and a mutation state with `isPaused` is queued.
- When persisting the cache:
  - Use `PersistQueryClientProvider` with `createAsyncStoragePersister`; the sync storage persister is deprecated.
  - Set `gcTime` to at least the persister's `maxAge`, or entries are removed before they can be restored.
  - Set `buster` to the app or schema version, so a release with a new data shape discards the old cache.
  - Use `dehydrateOptions.shouldDehydrateQuery` to exclude sensitive or rapidly changing data.
  - Use `useIsRestoring` to wait for restoration before depending on restored data.

### Rationale

By default, TanStack Query pauses fetches and mutations while the browser reports being offline, which looks like an endless loading state unless the UI says so.
Query functions that do not need the network should not pause.
A persisted cache outlives the code that wrote it and is stored on the device, so it needs versioning and filtering.

### Examples

#### Application: Showing paused work

**Incorrect (counterexample):**

```tsx
const pending = useMutationState({ filters: { status: 'pending' } });
const paused = pending.filter((mutation) => mutation.state.isPaused);
```

Without `select`, `useMutationState` already returns each mutation's state, so `mutation.state` is undefined and this throws.

**Correct:**

```tsx
const pausedCount = useMutationState({
  filters: { status: 'pending' },
  select: (mutation) => mutation.state.isPaused,
}).filter(Boolean).length;
```

#### Application: Persisting the cache

**Correct:**

```tsx
const queryClient = new QueryClient({
  defaultOptions: { queries: { gcTime: 24 * 60 * 60 * 1000 } },
});

const persister = createAsyncStoragePersister({ storage: window.localStorage });

<PersistQueryClientProvider
  client={queryClient}
  persistOptions={{
    persister,
    maxAge: 24 * 60 * 60 * 1000,
    buster: APP_VERSION,
    dehydrateOptions: {
      shouldDehydrateQuery: (query) => query.state.status === 'success' && query.queryKey[0] !== 'session',
    },
  }}
>
  <App />
</PersistQueryClientProvider>;
```

### Validation

Switch the browser to offline mode and check that paused queries and mutations are visible to the user and resume when back online.
Reload with a persisted cache from an older app version and check that it is discarded.
Inspect stored data for sensitive fields.

An app that does not need offline support and keeps the defaults is not a violation.
