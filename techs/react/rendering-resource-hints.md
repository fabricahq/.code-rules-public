---
title: "Hint critical resources with React DOM resource APIs"
whenToRead: "Before planning, writing, changing, or reviewing how a React app loads fonts, stylesheets, scripts, or connections to other origins that a page needs early."
impact: "MEDIUM"
impactDescription: "Resources discovered late, after other downloads or code run, delay rendering."
tags: "react, react-dom, preload, performance"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-resource-hints.md
    description: "Adapted from the Vercel Agent Skills rule rendering-resource-hints: restructured to the rule template, corrected the preinit stylesheet example to include the required precedence, and recalibrated impact."
---

## Hint critical resources with React DOM resource APIs

When a page will need a resource that the browser would discover late, call the matching React DOM resource API during render so the browser starts fetching it early.

### Implementation

- `prefetchDNS(href)` resolves a domain you may connect to later.
- `preconnect(href)` opens a connection to an origin you will fetch from soon.
- `preload(href, { as })` fetches a font, stylesheet, script, or image that the current page needs.
- `preloadModule(href)` fetches an ES module that will be imported soon.
- `preinit(href, { as, precedence })` fetches and applies a stylesheet or script; stylesheets require `precedence`.
- Call these in Server Components or during render so the hints appear in the initial HTML; React deduplicates repeated calls.
- Hint only resources the page will use soon; unnecessary preloads compete with critical downloads.

### Rationale

A browser finds a resource only when it parses the reference, such as a font referenced inside a stylesheet or a script imported by another script.
A hint in the initial HTML lets the download start in parallel instead of in sequence.

### Examples

**Incorrect (counterexample):**

```tsx
export default function RootLayout({ children }: { children: ReactNode }) {
  preinit('/styles/critical.css', { as: 'style' });
  return (
    <html>
      <body>{children}</body>
    </html>
  );
}
```

React documents `precedence` as required for stylesheets passed to `preinit`, so this call omits a required option.

**Correct:**

```tsx
import { preconnect, preinit, preload } from 'react-dom';

export default function RootLayout({ children }: { children: ReactNode }) {
  preconnect('https://api.example.com');
  preload('/fonts/inter.woff2', { as: 'font', type: 'font/woff2', crossOrigin: 'anonymous' });
  preinit('/styles/critical.css', { as: 'style', precedence: 'high' });

  return (
    <html>
      <body>{children}</body>
    </html>
  );
}
```

### Validation

Inspect the initial HTML for the expected `<link>` hints, and check in the network panel that the resources start downloading early.
Check the console for warnings about preloaded resources that went unused.

A resource that the browser already discovers early does not need a hint.
