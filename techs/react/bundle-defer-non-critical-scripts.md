---
title: "Keep non-critical scripts off the critical path"
whenToRead: "Before planning, adding, changing, or reviewing third-party or non-critical scripts and libraries in a React app, such as analytics, error tracking, chat widgets, or external script tags."
impact: "MEDIUM-HIGH"
impactDescription: "Scripts that block parsing or ship in the initial bundle delay rendering and interactivity for work the user does not need yet."
tags: "react, scripts, third-party, performance, nextjs"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/tree/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules
    description: "Adapted from two Vercel Agent Skills rules (bundle-defer-third-party and rendering-script-defer-async): merged two rules on third-party libraries and script loading attributes, restructured to the rule template, and corrected the Next.js example so ssr false is used only in a Client Component."
---

## Keep non-critical scripts off the critical path

Load scripts and libraries that the first render does not need, such as analytics and error tracking, without blocking parsing and outside the initial bundle.

### Implementation

- For external `<script>` tags, add `async` to independent scripts such as analytics, and `defer` to scripts that need the parsed document or must run in order.
- In Next.js, use `next/script` with a `strategy` such as `afterInteractive` or `lazyOnload` instead of a raw script tag.
- Load non-critical npm libraries with a dynamic import after hydration.
  In Next.js, `next/dynamic` with `ssr: false` must be called from a Client Component.
- Keep scripts that the page cannot function without, such as a required polyfill, on the critical path.
- Load error tracking early enough to capture errors during startup when that matters; decide this per tool rather than deferring everything.

### Rationale

A script tag without `async` or `defer` stops HTML parsing until it downloads and runs.
A library imported normally joins the initial bundle, which must load before the app is interactive.
Deferring work the user does not need yet lets the page render and respond sooner.

### Examples

#### Application: External script tags

**Incorrect (counterexample):**

```tsx
<head>
  <script src="https://example.com/analytics.js" />
</head>
```

Parsing stops until the analytics script downloads and runs.

**Correct:**

```tsx
<head>
  <script src="https://example.com/analytics.js" async />
</head>
```

#### Application: A third-party library in Next.js

**Incorrect (counterexample):**

```tsx
// app/layout.tsx, a Server Component
const Analytics = dynamic(() => import('@vercel/analytics/react').then((module) => module.Analytics), {
  ssr: false,
});
```

`ssr: false` is not allowed in Server Components, so this fails.

**Correct:**

```tsx
// app/deferred-analytics.tsx
'use client';

import dynamic from 'next/dynamic';

export const DeferredAnalytics = dynamic(
  () => import('@vercel/analytics/react').then((module) => module.Analytics),
  { ssr: false },
);
```

The root layout renders `<DeferredAnalytics />`, and the library loads in the browser after hydration.

### Validation

Check the page's HTML for script tags without `async`, `defer`, or `type="module"`, and check the initial bundle for third-party libraries not needed on first render.

A required polyfill or critical script loaded synchronously is not a violation.
