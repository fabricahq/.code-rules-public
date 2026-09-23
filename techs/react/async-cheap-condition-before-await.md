---
title: "Check Cheap Conditions Before Async Flags"
whenToRead: "Before writing a branch that combines a cheap synchronous guard with an awaited flag or remote value."
impact: "HIGH"
impactDescription: "avoids unnecessary async work when a synchronous guard already fails"
tags: "react, performance, async, await, feature-flags, short-circuit, conditional"

attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/async-cheap-condition-before-await.md
    description: "Underlying Vercel Agent Skills rule adapted in the source corpus."
---

## Check Cheap Conditions Before Async Flags

When a branch uses `await` for a flag or remote value and also requires a **cheap synchronous** condition (local props, request metadata, already-loaded state), evaluate the cheap condition **first**. Otherwise you pay for the async call even when the compound condition can never be true.

This specializes deferring an await until its result is needed for `flag && cheapCondition` style checks.

**Incorrect:**

```typescript
const someFlag = await getFlag()

if (someFlag && someCondition) {
  // ...
}
```

**Correct:**

```typescript
if (someCondition) {
  const someFlag = await getFlag()
  if (someFlag) {
    // ...
  }
}
```

This matters when `getFlag` hits the network, a feature-flag service, or `React.cache` / DB work: skipping it when `someCondition` is false removes that cost on the cold path.

Keep the original order if `someCondition` is expensive, depends on the flag, or you must run side effects in a fixed order.

Source: [Vercel Agent Skills - react-best-practices/async-cheap-condition-before-await.md](https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/async-cheap-condition-before-await.md). Adapted with attribution.
