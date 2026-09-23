---
title: "Prefer Required Object Properties"
whenToRead: "Before designing a TypeScript object shape with properties that may be optional."
impact: "HIGH"
impactDescription: "keeps object shapes predictable and avoids optional-property states that should be modeled explicitly"
tags: "typescript, object-types, optional, required, discriminated-unions"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Prefer Required Object Properties

**Strive to have the majority of object properties required and use optional properties sparingly.**

This approach reflects designing type-safe and maintainable code:

- Clarity and Predictability - Required properties make it explicit which data is always expected. This reduces ambiguity for developers using or consuming the object, as they know exactly what must be present.
- Type Safety - When properties are required, TypeScript can enforce their presence at compile time. This prevents runtime errors caused by missing properties.
- Avoids Overuse of Optional Chaining - If too many properties are optional, it often leads to extensive use of optional chaining (`?.`) to handle potential undefined values. This clutters the code and obscures its intent.

If introducing many optional properties truly can't be avoided, utilize **discriminated union types**.

```ts
// Avoid optional properties when possible, as they increase complexity and ambiguity
type User = {
  id?: number;
  email?: string;
  dashboardAccess?: boolean;
  adminPermissions?: ReadonlyArray<string>;
  subscriptionPlan?: 'free' | 'pro' | 'premium';
  rewardsPoints?: number;
  temporaryToken?: string;
};

// Prefer required properties. If optional properties are unavoidable,
// use a discriminated union to make object usage explicit and predictable.
type AdminUser = {
  role: 'admin';
  id: number;
  email: string;
  dashboardAccess: boolean;
  adminPermissions: ReadonlyArray<string>;
};

type RegularUser = {
  role: 'regular';
  id: number;
  email: string;
  subscriptionPlan: 'free' | 'pro' | 'premium';
  rewardsPoints: number;
};

type GuestUser = {
  role: 'guest';
  temporaryToken: string;
};

// Discriminated union type 'User' ensures clear intent with no optional properties
type User = AdminUser | RegularUser | GuestUser;

const regularUser: User = {
  role: 'regular',
  id: 212,
  email: 'lea@user.com',
  subscriptionPlan: 'pro',
  rewardsPoints: 1500,
  dashboardAccess: false, // Error: 'dashboardAccess' property does not exist
};
```
