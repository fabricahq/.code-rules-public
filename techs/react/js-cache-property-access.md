---
title: "Cache Property Access in Loops"
whenToRead: "When implementing or reviewing measured hot loops with repeated property reads in a React app."
impact: "LOW-MEDIUM"
impactDescription: "Repeated property lookups can add avoidable work in a measured hot loop."
tags: "react, performance, javascript, loops, optimization, caching"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-cache-property-access.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Cache Property Access in Loops

Cache object property lookups in hot paths.

**Incorrect (3 lookups x N iterations):**

```typescript
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value)
}
```

**Correct (1 lookup total):**

```typescript
const value = obj.config.settings.value
const len = arr.length
for (let i = 0; i < len; i++) {
  process(value)
}
```

Source: [Vercel Agent Skills - react-best-practices/js-cache-property-access.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-cache-property-access.md). Adapted with attribution.
