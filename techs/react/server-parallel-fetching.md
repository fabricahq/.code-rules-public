---
title: "Compose independent server data fetches as siblings"
whenToRead: "Before planning, writing, changing, or reviewing React Server Components that fetch data, such as a page whose sections each need their own data."
impact: "HIGH"
impactDescription: "A parent that awaits data before rendering a fetching child turns independent requests into a sequential waterfall."
tags: "react, server-components, data-fetching, waterfalls"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/server-parallel-fetching.md
    description: "Adapted from the Vercel Agent Skills rule server-parallel-fetching: restructured to the rule template and recalibrated impact."
---

## Compose independent server data fetches as siblings

When sections of a server-rendered page need independent data, give each section its own async Server Component and render them as siblings, instead of awaiting one section's data in a parent that renders the other.

### Implementation

- Move each `await` into the component that uses the data.
- Render components with independent data side by side, so they start fetching at the same time.
- When one fetch depends on another's result, keep them in sequence; this rule is about independent data.
- Combine this with `Suspense` boundaries so each section can stream when its data arrives.

### Rationale

A child Server Component does not start rendering until its parent returns it.
If the parent awaits its own data first, the child's fetch waits for the parent's, even when the two are unrelated.
Siblings start rendering together, so their fetches overlap.

### Examples

**Incorrect (counterexample):**

```tsx
export default async function Page() {
  const header = await fetchHeader();
  return (
    <div>
      <div>{header}</div>
      <Sidebar />
    </div>
  );
}

async function Sidebar() {
  const items = await fetchSidebarItems();
  return <nav>{items.map(renderItem)}</nav>;
}
```

`fetchSidebarItems` starts only after `fetchHeader` finishes.

**Correct:**

```tsx
async function Header() {
  const header = await fetchHeader();
  return <div>{header}</div>;
}

export default function Page() {
  return (
    <div>
      <Header />
      <Sidebar />
    </div>
  );
}
```

`Header` and `Sidebar` render as siblings, so both fetches start together.

### Validation

Trace the page's data requests with server timing or logs and check that independent requests overlap.

Sequential fetches where one needs the other's result are not a violation.
