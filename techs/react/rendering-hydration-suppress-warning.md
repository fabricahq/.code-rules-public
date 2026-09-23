---
title: "Suppress Expected Hydration Mismatches"
whenToRead: "Before handling an intentional server/client text mismatch in a server-rendered React application."
impact: "LOW-MEDIUM"
impactDescription: "avoids noisy hydration warnings for known differences"
tags: "react, performance, rendering, hydration, ssr, nextjs"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-hydration-suppress-warning.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Suppress Expected Hydration Mismatches

In SSR frameworks (e.g., Next.js), some values are intentionally different on server vs client (random IDs, dates, locale/timezone formatting). For these *expected* mismatches, wrap the dynamic text in an element with `suppressHydrationWarning` to prevent noisy warnings. Do not use this to hide real bugs. Don't overuse it.

**Incorrect (known mismatch warnings):**

```tsx
function Timestamp() {
  return <span>{new Date().toLocaleString()}</span>
}
```

**Correct (suppress expected mismatch only):**

```tsx
function Timestamp() {
  return (
    <span suppressHydrationWarning>
      {new Date().toLocaleString()}
    </span>
  )
}
```

Source: [Vercel Agent Skills - react-best-practices/rendering-hydration-suppress-warning.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-hydration-suppress-warning.md). Adapted with attribution.
