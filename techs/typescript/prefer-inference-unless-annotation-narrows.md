---
title: "Prefer Inference Unless Explicit Types Narrow"
whenToRead: "Before adding TypeScript annotations to local variables, expressions, or return values."
impact: "MEDIUM"
impactDescription: "keeps annotations useful by adding them when they narrow or clarify instead of restating inference"
tags: "typescript, inference, annotations, narrowing, readability"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Prefer Inference Unless Explicit Types Narrow

As a rule of thumb, explicitly declare types only when it helps to narrow them.

**Note:**

Just because you don't need to add types doesn't mean you shouldn't. In some cases, explicitly declaring types can
  improve code readability and clarify intent.

Explicitly declare types when doing so helps to narrow them:

```ts
// Avoid
const employees = new Map(); // Inferred as wide type 'Map<any, any>'
employees.set('Lea', 17);
type UserRole = 'admin' | 'guest';
const [userRole, setUserRole] = useState('admin'); // Inferred as 'string', not the desired narrowed literal type

// Use explicit type declarations to narrow the types.
const employees = new Map<string, number>(); // Narrowed to 'Map<string, number>'
employees.set('Gabriel', 32);
type UserRole = 'admin' | 'guest';
const [userRole, setUserRole] = useState<UserRole>('admin'); // Explicit type 'UserRole'
```

Avoid explicitly declaring types when they can be inferred:

```ts
// Avoid
const userRole: string = 'admin'; // Inferred as wide type 'string'
const employees = new Map<string, number>([['Gabriel', 32]]); // Redundant type declaration
const [isActive, setIsActive] = useState<boolean>(false); // Redundant, inferred as 'boolean'

// Use type inference.
const USER_ROLE = 'admin'; // Inferred as narrowed string literal type 'admin'
const employees = new Map([['Gabriel', 32]]); // Inferred as 'Map<string, number>'
const [isActive, setIsActive] = useState(false); // Inferred as 'boolean'
```
