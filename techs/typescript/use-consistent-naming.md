---
title: "Use Consistent Naming"
whenToRead: "Before naming TypeScript variables, functions, types, components, props, or hooks."
impact: "LOW"
impactDescription: "keeps code readable by applying consistent names for values, types, generics, React props, and hooks"
tags: "typescript, naming, generics, acronyms, react"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Use Consistent Naming

While it's often hard to find the best name, aim to optimize code for consistency and future readers by following these conventions:

### Variables

- **Locals**
  Camel case
  `products`, `productsFiltered`
- **Booleans**
   Prefixed with `is`, `has` etc.
   `isDisabled`, `hasProduct`
    **Related automated rule:** [Reference](https://typescript-eslint.io/rules/naming-convention)

```js
'@typescript-eslint/naming-convention': [
      'error',
      {
        selector: 'variable',
        types: ['boolean'],
        format: ['PascalCase'],
        prefix: ['is', 'are', 'should', 'has', 'can', 'did', 'will'],
      }
  ]
```

- **Constants**
  Capitalized

  ```ts
  const FEATURED_PRODUCT_ID = '8f47d2a1-b13e-4d5a-a7d8-6ef1234';
  ```

- **Object & Array Constants**

  Singular, capitalized with const assertion.

  ```ts
  const IDLE_ORDER = {
    pending: 'idle',
    fulfilled: true,
    error: 'Shipping Error',
  } as const;

  const DASHBOARD_ACCESS_ROLES = ['admin', 'editor', 'moderator'] as const;
  ```

  If a type exists use [Type-Safe Constants With Satisfies](#type-safe-constants-with-satisfies).

  ```ts
  // Type OrderStatus is predefined (e.g. generated from database schema, API)
  type OrderStatus = {
    pending: 'pending' | 'idle';
    fulfilled: boolean;
    error: string;
  };

  const IDLE_ORDER = {
    pending: 'idle',
    fulfilled: true,
    error: 'Shipping Error',
  } as const satisfies OrderStatus;

  // Type UserRole is predefined
  type UserRole = 'admin' | 'editor' | 'moderator' | 'viewer' | 'guest';

  const DASHBOARD_ACCESS_ROLES = ['admin', 'editor', 'moderator'] as const satisfies ReadonlyArray<UserRole>;
  ```

### Functions

Camel case
`filterProductsByType`, `formatCurrency`

### Types

Pascal case
`OrderStatus`, `ProductItem`

**Related automated rule:** [Reference](https://typescript-eslint.io/rules/naming-convention)

```js
'@typescript-eslint/naming-convention': [
  'error',
  {
    selector: 'typeAlias',
    format: ['PascalCase'],
  },
]
```

### Generics

A generic type parameter must start with the capital letter T followed by a descriptive name `TRequest`, `TFooBar`.

Key reasons and benefits:

- Complex types often involve generics, where clear naming improves readability and maintainability.
- Single letter generics like `T`, `K`, `U` are disallowed, the more parameters we introduce, the easier it is to mistake them.
- Prefixing with `T` makes it immediately obvious that it's a generic type parameter, not a regular type.
- A common scenario is when a generic parameter shadows an existing type due to having the same name e.g. `<Request extends Request>`

**Related automated rule:** [Reference](https://typescript-eslint.io/rules/naming-convention)

```js
'@typescript-eslint/naming-convention': [
    'error',
    {
      // Generic type parameter must start with letter T, followed by any uppercase letter.
      selector: 'typeParameter',
      format: ['PascalCase'],
      custom: { regex: '^T[A-Z]', match: true },
    }
]
```

```ts
// Avoid naming generic parameters with one letter
const createPair = <T, K extends string>(first: T, second: K): [T, K] => {
  return [first, second];
};
const pair = createPair(1, 'a');

// Use descriptive names starting with capital T
const createPair = <TFirst, TSecond extends string>(first: TFirst, second: TSecond): [TFirst, TSecond] => {
  return [first, second];
};
const pair = createPair(1, 'a');

// Avoid naming generic parameters without a prefix - which 'Request' is which?
const handle = <Request extends Request>(req: Request): void => {...

// Prefix generic parameter with capital T
const handle = <TRequest extends Request>(req: TRequest): void => {...
```

### Abbreviations & Acronyms

Treat acronyms as whole words, with capitalized first letter only.

```ts
// Avoid
const FAQList = ['qa-1', 'qa-2'];
const generateUserURL(params) => {...}

// Use
const FaqList = ['qa-1', 'qa-2'];
const generateUserUrl(params) => {...}
```

In favor of readability, strive to avoid abbreviations, unless they are widely accepted and necessary.

```ts
// Avoid
const GetWin(params) => {...}

// Use
const GetWindow(params) => {...}
```

### React Components

Pascal case
 `ProductItem`, `ProductsPage`

### Prop Types

React component name following "Props" postfix
 `[ComponentName]Props` - `ProductItemProps`, `ProductsPageProps`

### Callback Props

Event handler (callback) props are prefixed as `on*` - e.g. `onClick`.
Event handler implementation functions are prefixed as `handle*` - e.g. `handleClick`.

**Related automated rule:** [Reference](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-handler-names.md)

```js
'react/jsx-handler-names': [
    'error',
    {
      eventHandlerPrefix: 'handle',
      eventHandlerPropPrefix: 'on',
    },
]
```

```tsx
// Avoid inconsistent callback prop naming
<Button click={actionClick} />
<MyComponent userSelectedOccurred={triggerUser} />

// Use prop prefix 'on*' and handler prefix 'handle*'
<Button onClick={handleClick} />
<MyComponent onUserSelected={handleUserSelected} />
```

### React Hooks

**Related automated rule:** Camel case, prefixed as 'use' [Reference](https://github.com/facebook/react/tree/main/packages/eslint-plugin-react-hooks)

```js
'react-hooks/rules-of-hooks': 'error'
```
**Related automated rule:** Symmetrically convention as [value, setValue] = useState() [Reference](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/hook-use-state.md#rule-details)

```js
'react/hook-use-state': 'error'
```

```ts
// Avoid inconsistent useState hook naming
const [userName, setUser] = useState();
const [color, updateColor] = useState();
const [isActive, setActive] = useState();

// Use
const [name, setName] = useState();
const [color, setColor] = useState();
const [isActive, setIsActive] = useState();
```

Custom hook must always return an object

```ts
// Avoid
const [products, errors] = useGetProducts();
const [fontSizes] = useTheme();

// Use
const { products, errors } = useGetProducts();
const { fontSizes } = useTheme();
```
