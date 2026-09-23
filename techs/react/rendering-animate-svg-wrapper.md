---
title: "Animate SVG Wrapper Instead of SVG Element"
whenToRead: "Before animating an SVG element in a browser-based React UI."
impact: "LOW"
impactDescription: "Animating some SVG properties can require more browser work than animating a wrapper."
tags: "react, performance, rendering, svg, css, animation"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-animate-svg-wrapper.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Animate SVG Wrapper Instead of SVG Element

Many browsers don't have hardware acceleration for CSS3 animations on SVG elements. Wrap SVG in a `<div>` and animate the wrapper instead.

**Incorrect (animating SVG directly - no hardware acceleration):**

```tsx
function LoadingSpinner() {
  return (
    <svg
      className="animate-spin"
      width="24"
      height="24"
      viewBox="0 0 24 24"
    >
      <circle cx="12" cy="12" r="10" stroke="currentColor" />
    </svg>
  )
}
```

**Correct (animating wrapper div - hardware accelerated):**

```tsx
function LoadingSpinner() {
  return (
    <div className="animate-spin">
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
      >
        <circle cx="12" cy="12" r="10" stroke="currentColor" />
      </svg>
    </div>
  )
}
```

A wrapper may let browsers handle transforms more efficiently. Rendering behavior varies by browser and animated property, so profile the actual animation.

Source: [Vercel Agent Skills - react-best-practices/rendering-animate-svg-wrapper.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-animate-svg-wrapper.md). Adapted with attribution.
