---
title: "Optimize SVG Precision"
whenToRead: "Before optimizing a large SVG asset used in a React interface."
impact: "LOW"
impactDescription: "Excess SVG coordinate precision increases transferred asset bytes without visible benefit."
tags: "react, performance, rendering, svg, optimization, svgo"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-svg-precision.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Optimize SVG Precision

Reduce SVG coordinate precision to decrease file size. The optimal precision depends on the viewBox size, but in general reducing precision should be considered.

**Incorrect (excessive precision):**

```svg
<path d="M 10.293847 20.847362 L 30.938472 40.192837" />
```

**Correct (1 decimal place):**

```svg
<path d="M 10.3 20.8 L 30.9 40.2" />
```

**Automate with SVGO:**

```bash
npx svgo --precision=1 --multipass icon.svg
```

Source: [Vercel Agent Skills - react-best-practices/rendering-svg-precision.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-svg-precision.md). Adapted with attribution.
