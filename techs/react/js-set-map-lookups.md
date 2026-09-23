---
title: "Use Set/Map for O(1) Lookups"
whenToRead: "Before repeatedly checking array membership or looking up items by key in React code."
impact: "LOW-MEDIUM"
impactDescription: "Repeated linear searches can make lookups slow as collections grow."
tags: "react, performance, javascript, set, map, data-structures"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-set-map-lookups.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Use Set/Map for O(1) Lookups

Convert arrays to Set/Map for repeated membership checks.

**Incorrect (O(n) per check):**

```typescript
const allowedIds = ['a', 'b', 'c', ...]
items.filter(item => allowedIds.includes(item.id))
```

**Correct (O(1) per check):**

```typescript
const allowedIds = new Set(['a', 'b', 'c', ...])
items.filter(item => allowedIds.has(item.id))
```

Source: [Vercel Agent Skills - react-best-practices/js-set-map-lookups.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-set-map-lookups.md). Adapted with attribution.
