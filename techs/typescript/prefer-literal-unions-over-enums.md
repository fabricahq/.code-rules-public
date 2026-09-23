---
title: "Prefer Literal Unions Over Enums"
whenToRead: "Before modeling a finite set of TypeScript values with an enum or literal union."
impact: "MEDIUM"
impactDescription: "avoids enum runtime output and favors erased literal types or const data"
tags: "typescript, enum, literal-union, as-const, runtime"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Prefer Literal Unions Over Enums

Enums are discouraged in the TypeScript ecosystem due to their runtime cost and quirks.
The TypeScript documentation outlines several [pitfalls](https://www.typescriptlang.org/docs/handbook/enums.html#const-enum-pitfalls), and recently introduced the [--erasableSyntaxOnly](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-8.html#the---erasablesyntaxonly-option) flag to disable runtime-generating features like enums altogether.

**Related automated rule:** [Reference](https://eslint.org/docs/latest/rules/no-restricted-syntax)

```js
'no-restricted-syntax': [
    'error',
    {
      selector: 'TSEnumDeclaration',
      message: 'Replace enum with a literal type or a const assertion.',
    },
]
```

As rule of a thumb, prefer:

- Literal types whenever possible.
- Const assertion arrays when looping through values.
- Const assertion objects when enumerating arbitrary values.

Examples:

- Use literal types to avoid runtime objects and reduce bundle size.

  ```ts
  // Avoid using enums as they increase the bundle size
  enum UserRole {
    GUEST = 'guest',
    MODERATOR = 'moderator',
    ADMINISTRATOR = 'administrator',
  }

  // Transpiled JavaScript
  ('use strict');
  var UserRole;
  (function (UserRole) {
    UserRole['GUEST'] = 'guest';
    UserRole['MODERATOR'] = 'moderator';
    UserRole['ADMINISTRATOR'] = 'administrator';
  })(UserRole || (UserRole = {}));

  // Use literal types - Types are stripped during transpilation
  type UserRole = 'guest' | 'moderator' | 'administrator';

  const isGuest = (role: UserRole) => role === 'guest';
  ```

- Use const assertion arrays when looping through values.

  ```tsx
  // Avoid using enums
  enum USER_ROLES {
    guest = 'guest',
    moderator = 'moderator',
    administrator = 'administrator',
  }

  // Use const assertions arrays
  const USER_ROLES = ['guest', 'moderator', 'administrator'] as const;
  type UserRole = (typeof USER_ROLES)[number];

  const seedDatabase = () => {
    USER_ROLES.forEach((role) => {
      db.roles.insert(role);
    }
  }
  const insert = (role: UserRole) => {...

  const UsersRoleList = () => {
    return (
      <div>
        {USER_ROLES.map((role) => (
          <Item key={role} role={role} />
        ))}
      </div>
    );
  };
  const Item = ({ role }: { role: UserRole }) => {...
  ```

- Use const assertion objects when enumerating arbitrary values.

  ```ts
  // Avoid using enums
  enum COLORS {
    primary = '#B33930',
    secondary = '#113A5C',
    brand = '#9C0E7D',
  }

  // Use const assertions objects
  const COLORS = {
    primary: '#B33930',
    secondary: '#113A5C',
    brand: '#9C0E7D',
  } as const;

  type Colors = typeof COLORS;
  type ColorKey = keyof Colors; // Type "primary" | "secondary" | "brand"
  type ColorValue = Colors[ColorKey]; // Type "#B33930" | "#113A5C" | "#9C0E7D"

  const setColor = (color: ColorValue) => {...

  setColor(COLORS.primary);
  setColor('#B33930');
  ```
