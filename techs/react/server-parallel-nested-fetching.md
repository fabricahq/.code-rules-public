---
title: "Parallel Nested Data Fetching"
whenToRead: "Before fetching several nested collections with dependencies within each item on the server."
impact: "CRITICAL"
impactDescription: "One slow nested fetch can delay independent work for other items."
tags: "react, performance, server, rsc, parallel-fetching, promise-chaining"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/server-parallel-nested-fetching.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Parallel Nested Data Fetching

When fetching nested data in parallel, chain dependent fetches within each item's promise so a slow item doesn't block the rest.

**Incorrect (a single slow item blocks all nested fetches):**

```tsx
const chats = await Promise.all(
  chatIds.map(id => getChat(id))
)

const chatAuthors = await Promise.all(
  chats.map(chat => getUser(chat.author))
)
```

If one `getChat(id)` out of 100 is extremely slow, the authors of the other 99 chats can't start loading even though their data is ready.

**Correct (each item chains its own nested fetch):**

```tsx
const chatAuthors = await Promise.all(
  chatIds.map(id => getChat(id).then(chat => getUser(chat.author)))
)
```

Each item independently chains `getChat` -> `getUser`, so a slow chat doesn't block author fetches for the others.

Source: [Vercel Agent Skills - react-best-practices/server-parallel-nested-fetching.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/server-parallel-nested-fetching.md). Adapted with attribution.
