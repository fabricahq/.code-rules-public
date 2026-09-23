---
title: "cache-stale-time: Set Appropriate staleTime Based on Data Volatility"
whenToRead: "Before configuring freshness and refetch behavior for TanStack Query data with different rates of change."
impact: "MEDIUM"
impactDescription: "reduces unnecessary refetches while keeping data freshness explicit"
tags: "tanstack-query, cache, stale-time, freshness, refetching"
attribution: [{"url":"https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/cache-stale-time.md","description":"Underlying tanstack-agent-skills material at skills/tanstack-query/rules/cache-stale-time.md, commit 0e8bcdc6af4959739e0f6a2dfb35dc70d513940a; adapted under MIT, with notice retained in the public library."}]
---

## cache-stale-time: Set Appropriate staleTime Based on Data Volatility

## Explanation

`staleTime` determines how long data is considered fresh. The default is 0ms, meaning data is immediately stale and will refetch on every new query mount. Set appropriate staleTime based on how often your data actually changes to reduce unnecessary network requests.

## Bad Example

```tsx
// Default staleTime of 0 - refetches on every component mount
const { data } = useQuery({
  queryKey: ['user-profile', userId],
  queryFn: () => fetchUserProfile(userId),
  // No staleTime set - always considered stale
})

// User profile probably doesn't change every second
// This causes unnecessary API calls on navigation

// Setting same staleTime everywhere regardless of data type
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,  // 1 minute for everything - too simple
    },
  },
})
```

## Good Example

```tsx
// Match staleTime to data volatility
const { data: profile } = useQuery({
  queryKey: ['user-profile', userId],
  queryFn: () => fetchUserProfile(userId),
  staleTime: 5 * 60 * 1000,  // 5 minutes - profile rarely changes
})

const { data: notifications } = useQuery({
  queryKey: ['notifications'],
  queryFn: fetchNotifications,
  staleTime: 30 * 1000,  // 30 seconds - changes more frequently
})

const { data: stockPrice } = useQuery({
  queryKey: ['stock', symbol],
  queryFn: () => fetchStockPrice(symbol),
  staleTime: 0,  // Real-time data - always refetch
})

// Set sensible defaults, override per-query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,  // 1 minute default
    },
  },
})
```

## Recommended staleTime Values

| Data Type | staleTime | Rationale |
|-----------|-----------|-----------|
| Real-time (stocks, live feeds) | 0 | Must always be current |
| Frequently changing (notifications) | 30s - 1min | Balance freshness and requests |
| User-generated content | 1 - 5min | Changes on user action |
| Reference data (categories, config) | 10 - 30min | Rarely changes |
| Static content | Infinity | Never changes |

## Context

- `staleTime: 0` (default) triggers background refetch on every mount
- `staleTime: Infinity` never considers data stale (manual invalidation only)
- Stale data is still returned instantly - refetch happens in background
- For SSR, set higher staleTime to avoid immediate client refetch
- Consider using `queryOptions` factory to centralize staleTime per data type

Source: [TanStack Agent Skills - tanstack-query/cache-stale-time.md](https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-query/rules/cache-stale-time.md). Adapted with attribution; see the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
