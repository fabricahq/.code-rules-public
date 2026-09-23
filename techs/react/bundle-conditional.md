---
title: "Conditional Module Loading"
whenToRead: "Before loading large modules or data used only after a React feature is activated."
impact: "HIGH"
impactDescription: "Eagerly loading optional modules increases initial download and evaluation work."
tags: "react, performance, bundle, conditional-loading, lazy-loading"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/bundle-conditional.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Conditional Module Loading

Load large data or modules only when a feature is activated.

**Example (lazy-load animation frames):**

```tsx
function AnimationPlayer({ enabled, setEnabled }: { enabled: boolean; setEnabled: React.Dispatch<React.SetStateAction<boolean>> }) {
  const [frames, setFrames] = useState<Frame[] | null>(null)

  useEffect(() => {
    if (enabled && !frames && typeof window !== 'undefined') {
      import('./animation-frames.js')
        .then(mod => setFrames(mod.frames))
        .catch(() => setEnabled(false))
    }
  }, [enabled, frames, setEnabled])

  if (!frames) return <Skeleton />
  return <Canvas frames={frames} />
}
```

The browser guard prevents execution during SSR. Whether the module appears in a server or client bundle depends on the bundler; inspect the build output if bundle size matters.

Source: [Vercel Agent Skills - react-best-practices/bundle-conditional.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/bundle-conditional.md). Adapted with attribution.
