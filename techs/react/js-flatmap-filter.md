---
title: "Use flatMap to Map and Filter in One Pass"
whenToRead: "When implementing or reviewing mapping and filtering of large arrays in a React app."
impact: "LOW-MEDIUM"
impactDescription: "Intermediate arrays and extra passes add avoidable work on large collections."
tags: "react, performance, javascript, arrays, flatMap, filter"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-flatmap-filter.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Use flatMap to Map and Filter in One Pass

Chaining `.map().filter(Boolean)` creates an intermediate array and iterates twice. Use `.flatMap()` to transform and filter in a single pass.

**Incorrect (2 iterations, intermediate array):**

```typescript
const userNames = users
  .map(user => user.isActive ? user.name : null)
  .filter(Boolean)
```

**Correct (1 iteration, no intermediate array):**

```typescript
const userNames = users.flatMap(user =>
  user.isActive ? [user.name] : []
)
```

**More examples:**

```typescript
// Extract valid emails from responses
// Before
const emails = responses
  .map(r => r.success ? r.data.email : null)
  .filter(Boolean)

// After
const emails = responses.flatMap(r =>
  r.success ? [r.data.email] : []
)

// Parse and filter valid numbers
// Before
const numbers = strings
  .map(s => parseInt(s, 10))
  .filter(n => !isNaN(n))

// After
const numbers = strings.flatMap(s => {
  const n = parseInt(s, 10)
  return isNaN(n) ? [] : [n]
})
```

**When to use:**
- Transforming items while filtering some out
- Conditional mapping where some inputs produce no output
- Parsing/validating where invalid inputs should be skipped

Source: [Vercel Agent Skills - react-best-practices/js-flatmap-filter.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-flatmap-filter.md). Adapted with attribution.
