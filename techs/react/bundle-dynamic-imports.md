---
title: "Dynamic Imports for Heavy Components"
whenToRead: "When planning, implementing, or reviewing optional heavy components in a Next.js application."
impact: "CRITICAL"
impactDescription: "Loading optional large components in the initial bundle delays first use of the page."
tags: "react, performance, bundle, dynamic-import, code-splitting, next-dynamic"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/bundle-dynamic-imports.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Dynamic Imports for Heavy Components

Use `next/dynamic` to lazy-load large components not needed on initial render.

**Incorrect (optional editor included in the initial bundle):**

```tsx
import { MonacoEditor } from './monaco-editor'

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

**Correct (Monaco loads on demand):**

```tsx
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(
  () => import('./monaco-editor').then(m => m.MonacoEditor),
  { ssr: false }
)

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

Source: [Vercel Agent Skills - react-best-practices/bundle-dynamic-imports.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/bundle-dynamic-imports.md). Adapted with attribution.
