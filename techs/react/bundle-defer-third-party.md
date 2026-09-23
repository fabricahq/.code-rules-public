---
title: "Defer Non-Critical Third-Party Libraries"
whenToRead: "Before loading analytics, logging, error tracking, or other noncritical third-party client libraries."
impact: "MEDIUM"
impactDescription: "Eager noncritical scripts can compete with code needed for initial interaction."
tags: "react, performance, bundle, third-party, analytics, defer"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/bundle-defer-third-party.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Defer Non-Critical Third-Party Libraries

Analytics, logging, and error tracking don't block user interaction. Load them after hydration.

**Incorrect (blocks initial bundle):**

```tsx
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

**Correct (loads after hydration):**

```tsx
import dynamic from 'next/dynamic'

const Analytics = dynamic(
  () => import('@vercel/analytics/react').then(m => m.Analytics),
  { ssr: false }
)

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

Source: [Vercel Agent Skills - react-best-practices/bundle-defer-third-party.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/bundle-defer-third-party.md). Adapted with attribution.
