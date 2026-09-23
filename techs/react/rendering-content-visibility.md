---
title: "Skip off-screen rendering work in long lists"
whenToRead: "Before writing, changing, reviewing, or diagnosing React UI that renders long scrollable lists or feeds whose items are mostly off screen."
impact: "MEDIUM"
impactDescription: "Laying out and painting every item of a long list slows initial render and scrolling."
tags: "react, css, performance, lists"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-content-visibility.md
    description: "Adapted from the Vercel Agent Skills rule rendering-content-visibility: restructured to the rule template, added the virtualization alternative, and recalibrated impact."
---

## Skip off-screen rendering work in long lists

For long lists whose items are mostly off screen, apply `content-visibility: auto` with a `contain-intrinsic-size` estimate to each item, so the browser skips layout and paint for items outside the viewport.

### Implementation

- Set `contain-intrinsic-size` close to an item's real height, so the scrollbar stays stable as items render.
- When the list is so long that creating its DOM nodes is the cost, such as thousands of rows, use a virtualization library instead; `content-visibility` does not reduce React rendering or DOM size.
- Measure rendering and scrolling before and after; short lists gain nothing.

### Rationale

Browsers lay out and paint every element in the document, including those far off screen.
`content-visibility: auto` lets the browser skip that work for off-screen elements while keeping them in the DOM, so find-in-page and the accessibility tree still include them.

### Examples

**Incorrect (counterexample):**

```css
.message-item {
  /* no containment: every item is laid out and painted */
}
```

**Correct:**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: auto 80px;
}
```

### Validation

Record a performance profile of initial render and scrolling before and after the change.
Check that the scrollbar does not jump noticeably while scrolling.

A short list without `content-visibility` is not a violation.
