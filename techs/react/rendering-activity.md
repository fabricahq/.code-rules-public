---
title: "Use Activity Component for Show/Hide"
whenToRead: "Before toggling an expensive React component when preserving hidden state matters; check support for Activity in the installed React version."
impact: "MEDIUM"
impactDescription: "Hidden content can retain component state when toggled back into view."
tags: "react, performance, rendering, activity, visibility, state-preservation"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-activity.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Use Activity Component for Show/Hide

When the installed React version supports `<Activity>`, use it for content that frequently toggles visibility and should retain state while hidden. Hidden Activity content may be removed from layout while its component state is preserved; verify effects and performance in the actual app.

**Usage:**

```tsx
import { Activity } from 'react'

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveMenu />
    </Activity>
  )
}
```

This preserves component state across visibility changes. Measure render cost before treating it as a performance optimization.

Source: [Vercel Agent Skills - react-best-practices/rendering-activity.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-activity.md). Adapted with attribution.
