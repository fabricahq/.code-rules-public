---
title: "Stream slow data behind Suspense boundaries"
whenToRead: "Before planning, writing, changing, or reviewing data loading in React Server Components or streaming server rendering, such as a page that awaits data before rendering its layout."
impact: "MEDIUM-HIGH"
impactDescription: "Awaiting data at the top of a page delays everything, including layout that does not need the data."
tags: "react, suspense, streaming, server-components"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/async-suspense-boundaries.md
    description: "Adapted from the Vercel Agent Skills rule async-suspense-boundaries: restructured to the rule template with a rationale and validation."
---

## Stream slow data behind Suspense boundaries

Await data in the component that needs it, and wrap that component in a `Suspense` boundary with a fallback, so the rest of the page can render and stream first.

### Implementation

- Move each slow data read into the smallest component that uses it.
- Wrap that component in `<Suspense fallback={...}>` with a fallback that matches the final content's size, to limit layout shift.
- When several components need the same data, start the request once in the parent without awaiting it, and pass the promise to children that read it with `use`.
- Keep data at the top when it decides the page's structure, such as whether to redirect or which layout to show.
- Keep data out of a boundary when it is small and fast enough that a fallback would only flash.

### Rationale

An `await` at the top of a server component blocks everything that component returns.
With a boundary around the part that needs the data, the server sends the rest of the page immediately and streams the slow part when it resolves.

### Examples

**Incorrect (counterexample):**

```tsx
async function Page() {
  const data = await fetchData();

  return (
    <Layout>
      <Sidebar />
      <DataDisplay data={data} />
    </Layout>
  );
}
```

The layout and sidebar wait for `fetchData` even though they do not use it.

**Correct:**

```tsx
function Page() {
  return (
    <Layout>
      <Sidebar />
      <Suspense fallback={<DataSkeleton />}>
        <DataDisplay />
      </Suspense>
    </Layout>
  );
}

async function DataDisplay() {
  const data = await fetchData();
  return <div>{data.content}</div>;
}
```

### Validation

Load the page with a slowed data source and check that the layout appears before the slow section.

Awaiting data at the top of a page is not a violation when that data decides the page's structure.
