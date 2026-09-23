---
title: "CSS content-visibility for Long Lists"
whenToRead: "Before rendering long offscreen lists in a browser-based React UI with CSS content-visibility."
impact: "HIGH"
impactDescription: "Rendering offscreen content in a long list can delay initial display."
tags: "react, performance, rendering, css, content-visibility, long-lists"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-content-visibility.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## CSS content-visibility for Long Lists

Apply `content-visibility: auto` to defer off-screen rendering.

**CSS:**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

**Example:**

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map(msg => (
        <div key={msg.id} className="message-item">
          <Avatar user={msg.author} />
          <div>{msg.content}</div>
        </div>
      ))}
    </div>
  )
}
```

For a long list, the browser can defer layout and paint for off-screen items. Measure the actual improvement and preserve accessible behavior.

Source: [Vercel Agent Skills - react-best-practices/rendering-content-visibility.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-content-visibility.md). Adapted with attribution.
