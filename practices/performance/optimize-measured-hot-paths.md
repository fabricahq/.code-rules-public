---
title: "Optimize measured hot paths by removing repeated work"
whenToRead: "Before planning, writing, changing, reviewing, or diagnosing code that is slow or runs very often over collections, such as lookups inside loops, repeated passes over large lists, or computations repeated on every render or request."
impact: "MEDIUM"
impactDescription: "Repeated searches, passes, and recomputation in hot code multiply with input size, while speculative micro-optimizations elsewhere add complexity without measurable gain."
tags: "performance, algorithms, collections, caching"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-set-map-lookups.md
    description: "Adapted from the Vercel Agent Skills rule js-set-map-lookups: merged nine JavaScript performance rules into one language-neutral practice with a measure-first requirement, restructured to the rule template, and removed claims that depended on engine details."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-index-maps.md
    description: "Adapted from the Vercel Agent Skills rule js-index-maps: merged nine JavaScript performance rules into one language-neutral practice with a measure-first requirement, restructured to the rule template, and removed claims that depended on engine details."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-combine-iterations.md
    description: "Adapted from the Vercel Agent Skills rule js-combine-iterations: merged nine JavaScript performance rules into one language-neutral practice with a measure-first requirement, restructured to the rule template, and removed claims that depended on engine details."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-early-exit.md
    description: "Adapted from the Vercel Agent Skills rule js-early-exit: merged nine JavaScript performance rules into one language-neutral practice with a measure-first requirement, restructured to the rule template, and removed claims that depended on engine details."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-hoist-regexp.md
    description: "Adapted from the Vercel Agent Skills rule js-hoist-regexp: merged nine JavaScript performance rules into one language-neutral practice with a measure-first requirement, restructured to the rule template, and removed claims that depended on engine details."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-length-check-first.md
    description: "Adapted from the Vercel Agent Skills rule js-length-check-first: merged nine JavaScript performance rules into one language-neutral practice with a measure-first requirement, restructured to the rule template, and removed claims that depended on engine details."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-min-max-loop.md
    description: "Adapted from the Vercel Agent Skills rule js-min-max-loop: merged nine JavaScript performance rules into one language-neutral practice with a measure-first requirement, restructured to the rule template, and removed claims that depended on engine details."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-cache-function-results.md
    description: "Adapted from the Vercel Agent Skills rule js-cache-function-results: merged nine JavaScript performance rules into one language-neutral practice with a measure-first requirement, restructured to the rule template, and removed claims that depended on engine details."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/js-cache-storage.md
    description: "Adapted from the Vercel Agent Skills rule js-cache-storage: merged nine JavaScript performance rules into one language-neutral practice with a measure-first requirement, restructured to the rule template, and removed claims that depended on engine details."
---

## Optimize measured hot paths by removing repeated work

When measurement shows that code is slow, or code runs very often over large inputs, remove repeated work: index repeated lookups, stop when the answer is known, avoid unnecessary passes, and compute invariant values once.
Leave code that is not measurably hot in its clearest form.

### Implementation

Measure first, with a profiler or timing around the suspected code, and measure again after the change.
Then look for these patterns:

- **Repeated searches:** replace membership checks or `find` calls inside a loop with a `Set` or `Map` built once before the loop.
- **Work after the answer is known:** return or break as soon as the result is determined, and check cheap conditions, such as array lengths, before expensive comparisons.
- **Unnecessary passes:** find a minimum or maximum in one pass instead of sorting, and combine several passes over the same large collection when each is cheap.
- **Invariant work in a loop, render, or request:** compute values that do not change, such as a compiled regular expression, once outside the repeated code.
- **Repeated pure computation with the same inputs:** cache results in a bounded cache, and invalidate it when the inputs can change.
- **Repeated synchronous I/O:** read a value from synchronous storage once per operation rather than once per item, and refresh it when another tab or process may change it.

Keep these limits in mind:

- Small inputs rarely benefit; a linear search over five items is fine.
- A cache needs a size limit and an invalidation rule, or it leaks memory and serves stale data.
- Keep behavior identical, including ordering, duplicate handling, and whether inputs are mutated.

### Rationale

Code that runs inside a loop, on every render, or on every request multiplies its cost by how often it runs.
A lookup inside a loop turns linear work into quadratic work as data grows, and invariant work repeated per iteration adds up in the same way.
Optimizing code that is not hot, however, makes it harder to read without a measurable benefit, which is why measurement comes first.

### Examples

These TypeScript examples illustrate the patterns; they apply in any language.

#### Application: Lookups inside a loop

**Incorrect (counterexample):**

```ts
function attachUsers(orders: ReadonlyArray<Order>, users: ReadonlyArray<User>) {
  return orders.map((order) => ({ ...order, user: users.find((user) => user.id === order.userId) }));
}
```

For 1,000 orders and 1,000 users, this can compare up to a million pairs.

**Correct:**

```ts
function attachUsers(orders: ReadonlyArray<Order>, users: ReadonlyArray<User>) {
  const userById = new Map(users.map((user) => [user.id, user]));
  return orders.map((order) => ({ ...order, user: userById.get(order.userId) }));
}
```

Building the map takes one pass, and each lookup is constant time.

#### Application: Sorting to find one value

**Incorrect (counterexample):**

```ts
const latest = [...projects].sort((a, b) => b.updatedAt - a.updatedAt)[0];
```

**Correct:**

```ts
const latest = projects.reduce<Project | undefined>(
  (current, project) => (current === undefined || project.updatedAt > current.updatedAt ? project : current),
  undefined,
);
```

One pass finds the latest project without copying and sorting the whole list.

#### Application: Code that is not hot

**Correct:**

```ts
const isAdmin = roles.includes('admin');
```

For a short list checked once per request, a `Set` would add code without a measurable gain, so no change is needed.

### Validation

Check that the change is backed by a measurement showing the code was slow or hot, and by a second measurement showing it improved.
Run the existing tests to confirm behavior, ordering, and mutation guarantees did not change.

Straightforward code in paths that are not hot is not a violation.
