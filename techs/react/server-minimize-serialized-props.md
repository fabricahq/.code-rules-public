---
title: "Pass only the data Client Components use"
whenToRead: "Before planning, writing, changing, or reviewing props passed from React Server Components to Client Components, especially large objects, lists, or derived copies of the same data."
impact: "MEDIUM"
impactDescription: "Every prop crossing the server-client boundary is serialized into the page, so unused fields and duplicate copies increase page weight and load time."
tags: "react, server-components, serialization, performance"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/server-serialization.md
    description: "Adapted from the Vercel Agent Skills rule server-serialization: merged two rules on serialization size and duplicate props, restructured to the rule template, and recalibrated impact."
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/server-dedup-props.md
    description: "Adapted from the Vercel Agent Skills rule server-dedup-props: merged two rules on serialization size and duplicate props, restructured to the rule template, and recalibrated impact."
---

## Pass only the data Client Components use

When a Server Component renders a Client Component, pass only the fields the client uses, and avoid passing both a value and a derived copy of it.

### Implementation

- Pick the needed fields on the server, such as `name` instead of a whole `user` record.
- Do not pass a list and a transformed copy of it, such as a sorted or filtered version; derive the copy on the client.
- Derive on the server when the client does not need the original, or when the transformation is expensive or needs server-only data.
- Never pass fields the user must not see; everything in props reaches the browser.

### Rationale

React serializes Client Component props into the server response.
Unused fields add to the page's size, and a derived copy is a separate object that is serialized again, so duplicated data is sent twice.
Smaller props mean less to download and parse, and fewer chances to expose data unintentionally.

### Examples

#### Application: A whole record for one field

**Incorrect (counterexample):**

```tsx
async function Page() {
  const user = await fetchUser();
  return <Profile user={user} />;
}
```

If `Profile` shows only the name, every other field of `user` is still sent to the browser.

**Correct:**

```tsx
async function Page() {
  const user = await fetchUser();
  return <Profile name={user.name} />;
}
```

#### Application: A derived copy

**Incorrect (counterexample):**

```tsx
<UserList usernames={usernames} sortedUsernames={usernames.toSorted()} />
```

Both arrays are serialized, so every name is sent twice.

**Correct:**

```tsx
<UserList usernames={usernames} />
```

`UserList` sorts the names on the client.

### Validation

Inspect the serialized payload in the page source or network panel for fields the client does not use and for repeated data.
Check that no sensitive fields cross the boundary.

A server-side derivation passed instead of the original is not a violation.
