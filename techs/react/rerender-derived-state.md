---
title: "Subscribe to Derived State"
whenToRead: "Before subscribing to a frequently changing value when the UI only needs a derived boolean or threshold."
impact: "MEDIUM"
impactDescription: "Subscribing to every continuous value change can rerender UI whose visible state has not changed."
tags: "react, performance, rerender, derived-state, media-query, optimization"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-derived-state.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Subscribe to Derived State

Subscribe to derived boolean state instead of continuous values to reduce re-render frequency.

**Incorrect (re-renders on every pixel change):**

```tsx
function Sidebar() {
  const width = useWindowWidth()  // updates continuously
  const isMobile = width < 768
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

**Correct (re-renders only when boolean changes):**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery('(max-width: 767px)')
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

Source: [Vercel Agent Skills - react-best-practices/rerender-derived-state.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-derived-state.md). Adapted with attribution.
