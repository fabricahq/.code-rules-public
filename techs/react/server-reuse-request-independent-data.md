---
title: "Reuse request-independent server data across requests"
whenToRead: "Before planning, writing, changing, or reviewing server code in a React app that loads the same static files or public data on every request, such as fonts for generated images, templates, configuration, or public reference data."
impact: "MEDIUM"
impactDescription: "Reloading identical data on every request adds latency and load, while caching the wrong data across requests leaks it between users."
tags: "react, server, caching, nextjs"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/tree/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules
    description: "Adapted from two Vercel Agent Skills rules (server-hoist-static-io and server-cache-lru): merged two rules on module-level static I/O and cross-request LRU caches, restructured to the rule template, and added failure handling for module-level promises."
---

## Reuse request-independent server data across requests

Load data that is identical for every request once per server process, and reuse it.
Start static file reads at module level, and keep changing public data in a bounded cache with expiry and invalidation.

### Implementation

- For static assets and configuration that never change while the process runs, start the read at module level and await the stored promise in the handler.
- Handle a failed module-level read so the process does not keep a rejected promise forever; retry on the next request or fail startup clearly.
- For public data that changes occasionally, use a bounded cache, such as an LRU with a maximum size and a time to live, and invalidate entries when the source changes.
- Never cache user- or tenant-specific data across requests unless the key includes the user or tenant and the cache is designed for it.
- Process memory is per instance: other instances do not share it, and it disappears on restart.
  Use an external cache when instances must share state.
- Do not keep very large files in memory for the life of the process.

### Rationale

Reading the same font file or template on every request repeats file-system or network work that always returns the same bytes.
Module code runs once per process, so work started there is shared by every request the process serves.
The same sharing is what makes caching request-specific data dangerous.

### Examples

#### Application: A static asset

**Incorrect (counterexample):**

```ts
export async function GET() {
  const font = await readFile(join(process.cwd(), 'assets/Inter.ttf'));
  return renderImage({ font });
}
```

Every request reads the font from disk again.

**Correct:**

```ts
let fontPromise: Promise<Buffer> | undefined;

function loadFont() {
  fontPromise ??= readFile(join(process.cwd(), 'assets/Inter.ttf')).catch((error) => {
    fontPromise = undefined;
    throw error;
  });
  return fontPromise;
}

export async function GET() {
  return renderImage({ font: await loadFont() });
}
```

The first request starts the read, later requests reuse it, and a failed read is retried.

#### Application: Public data that changes

**Correct:**

```ts
import { LRUCache } from 'lru-cache';

const referenceItems = new LRUCache<string, ReferenceItem>({ max: 1000, ttl: 5 * 60 * 1000 });

export async function getPublicReferenceItem(id: string) {
  const cached = referenceItems.get(id);
  if (cached) return cached;

  const item = await loadPublicReferenceItem(id);
  if (item) referenceItems.set(id, item);
  return item;
}
```

The cache is bounded, entries expire, and it holds only data that is the same for every caller.

### Validation

Check request handlers for reads of static files or public data that repeat on every request.
For each cross-request cache, check that it is bounded, that entries expire or are invalidated, and that it holds no user- or tenant-specific data without the user or tenant in its key.

Data that varies per request, loaded per request, is not a violation.
