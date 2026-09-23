---
title: "Authenticate and authorize inside every Server Action"
whenToRead: "Before planning, writing, changing, or reviewing a React or Next.js Server Action, or any function marked \"use server\", that reads or changes protected data."
impact: "CRITICAL"
impactDescription: "A Server Action without its own checks is a public endpoint that lets anyone read or change protected data."
tags: "react, nextjs, server-actions, security, authorization"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/server-auth-actions.md
    description: "Adapted from the Vercel Agent Skills rule server-auth-actions: restructured to the rule template, reordered checks to authenticate before validating, and added validation guidance."
---

## Authenticate and authorize inside every Server Action

Treat each Server Action as a public endpoint.
Inside the action itself, verify who the caller is, validate the input, and check that the caller may perform this operation on this data.

### Implementation

- Start each action by verifying the session.
  Reject the call when there is no valid session, unless the action is intentionally public.
- Validate the arguments with a schema or explicit checks; arguments arrive from the network, whatever their TypeScript types say.
- Authorize the specific operation against the specific record, such as checking that the caller owns the record or has the required role.
- Do not rely on middleware, layouts, or page-level checks alone.
  Those protect page rendering, not direct calls to the action's endpoint.
- Put shared checks in a helper that each action calls, rather than skipping them in actions that "only the settings page uses".

### Rationale

A framework exposes each Server Action through an HTTP endpoint that any client can call directly with any arguments.
A check on the page that renders the form does not run when someone calls the action without loading the page.
Only a check inside the action runs on every call.

### Examples

**Incorrect (counterexample):**

```ts
'use server';

export async function deleteUser(userId: string) {
  await db.user.delete({ where: { id: userId } });
}
```

Anyone who finds the action's endpoint can delete any user, even if the page that shows the button is restricted to administrators.

**Correct:**

```ts
'use server';

import { z } from 'zod';

const deleteUserInput = z.object({ userId: z.string().uuid() });

export async function deleteUser(input: unknown) {
  const session = await verifySession();
  if (!session) {
    throw new AuthError('Sign in required');
  }

  const { userId } = deleteUserInput.parse(input);

  if (session.user.role !== 'admin' && session.user.id !== userId) {
    throw new AuthError('Not allowed to delete this user');
  }

  await db.user.delete({ where: { id: userId } });
}
```

The action authenticates, validates, and authorizes on every call, whatever page invoked it.
`verifySession`, `AuthError`, and `db` stand for the project's own helpers.

### Validation

For each function marked `"use server"`, trace the path from entry to the first read or write of protected data.
A session check, input validation, and an authorization check against the target record should all come first.

An action intended to be public, such as a newsletter sign-up, is not a violation when a comment or name states that intent and it touches no protected data.
