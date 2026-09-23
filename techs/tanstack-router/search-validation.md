---
title: "Validate search params with defaults at the route"
whenToRead: "Before planning, writing, changing, or reviewing TanStack Router routes or components that read or update URL search params, such as filters, sorting, pagination, or a custom search param format."
impact: "HIGH"
impactDescription: "Search params come from the URL and can hold anything, so unvalidated reads produce NaN, invalid options, and runtime errors from edited or outdated links."
tags: "tanstack-router, search-params, validation, zod"
attribution:
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/search-validation.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule search-validation (MIT, notice retained in NOTICE.md): merged the custom-serializer rule, restructured to the rule template, corrected the serializer API to parseSearch and stringifySearch, and fixed a manual validator that turned zero into undefined."
  - url: https://github.com/DeckardGer/tanstack-agent-skills/blob/0e8bcdc6af4959739e0f6a2dfb35dc70d513940a/skills/tanstack-router/rules/search-custom-serializer.md
    description: "Adapted from Deckard Gerritsen TanStack Agent Skills rule search-custom-serializer (MIT, notice retained in NOTICE.md): merged the custom-serializer rule, restructured to the rule template, corrected the serializer API to parseSearch and stringifySearch, and fixed a manual validator that turned zero into undefined."
---

## Validate search params with defaults at the route

Give every route that reads search params a `validateSearch` that parses them, rejects or replaces invalid values, and supplies defaults.
Read them only through the route's typed APIs, such as `Route.useSearch()`.

### Implementation

- Use a schema library, such as Zod or Valibot, with a fallback or `catch` for each field, so an invalid value falls back to its default instead of failing the route.
  Recent router versions accept Standard Schema validators directly in `validateSearch`.
- Write a manual validator only for a few simple fields, and check each value's type explicitly.
- Read search params with `Route.useSearch()` or `getRouteApi(...).useSearch()`, never from `window.location`.
- Update them with `navigate({ search: (prev) => ({ ...prev, ...changes }) })` or `Link`'s `search`, resetting dependent values such as `page` when filters change.
- Search params are inherited by child routes, so validate shared ones in the parent.
- To change how search params appear in the URL, set the router's `parseSearch` and `stringifySearch` options together, built with `parseSearchWith` and `stringifySearchWith` so parsing and writing stay inverses.
  Validation still runs on the parsed values.

### Rationale

Users edit URLs, share old links, and follow links from other sites, so a search param may be missing, malformed, or out of range.
Validating at the route turns every URL into a known, typed shape once, instead of each component guessing, and gives every param a sensible default.

### Examples

#### Application: Reading raw search params

**Incorrect (counterexample):**

```tsx
function ProductsPage() {
  const params = new URLSearchParams(window.location.search);
  const page = parseInt(params.get('page') ?? '1');
  const sort = params.get('sort') as 'asc' | 'desc';
  // ...
}
```

`?page=abc` produces `NaN`, and `sort` can be any string despite its type.

**Correct:**

```tsx
const productSearchSchema = z.object({
  page: z.number().int().min(1).catch(1),
  sort: z.enum(['asc', 'desc']).catch('asc'),
  category: z.string().optional().catch(undefined),
});

export const Route = createFileRoute('/products')({
  validateSearch: productSearchSchema,
  component: ProductsPage,
});

function ProductsPage() {
  const { page, sort, category } = Route.useSearch();
  // ...
}
```

#### Application: A manual validator

**Incorrect (counterexample):**

```tsx
validateSearch: (search: Record<string, unknown>) => ({
  minPrice: Number(search.minPrice) || undefined,
}),
```

A minimum price of `0` becomes `undefined`, because `0` is falsy.

**Correct:**

```tsx
validateSearch: (search: Record<string, unknown>) => ({
  minPrice: typeof search.minPrice === 'number' && search.minPrice >= 0 ? search.minPrice : undefined,
}),
```

### Validation

Open the route with missing, malformed, and out-of-range search params, such as `?page=abc&sort=sideways`, and check that it renders with defaults.
Search components for reads from `window.location.search` or `URLSearchParams`.

A route that reads no search params does not need `validateSearch`.
