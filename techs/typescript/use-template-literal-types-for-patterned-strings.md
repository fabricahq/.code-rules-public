---
title: "Use Template Literal Types for Patterned Strings"
whenToRead: "Before modeling strings with a known prefix, suffix, or finite pattern in TypeScript."
impact: "MEDIUM"
impactDescription: "turns structured strings into typed contracts instead of unchecked string values"
tags: "typescript, template-literal-types, strings, routes, keys"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Use Template Literal Types for Patterned Strings

Embrace template literal types as they allow you to create precise and type-safe string constructs by interpolating values. They are a powerful alternative to using the wide string type, providing better type safety.

Adopting template literal types brings several advantages:

- Prevent errors caused by typos or invalid strings.
- Provide better type safety and autocompletion support.
- Improve code maintainability and readability.

Template literal types are useful in various practical scenarios, such as:

- String Patterns - Use template literal types to enforce valid string patterns.

  ```ts
  // Avoid
  const appVersion = '2.6';
  // Use
  type Version = `v${number}.${number}.${number}`;
  const appVersion: Version = 'v2.6.1';
  ```

- API Endpoints - Use template literal types to restrict values to valid API routes.

  ```ts
  // Avoid
  const userEndpoint = '/api/usersss'; // Type 'string' - Typo 'usersss': the route doesn't exist, leading to a runtime error.
  // Use
  type ApiRoute = 'users' | 'posts' | 'comments';
  type ApiEndpoint = `/api/${ApiRoute}`; // Type ApiEndpoint = "/api/users" | "/api/posts" | "/api/comments"
  const userEndpoint: ApiEndpoint = '/api/users';
  ```

- Internationalization Keys - Avoid relying on raw strings for translation keys, which can lead to typos and missing translations. Use template literal types to define valid translation keys.

  ```ts
  // Avoid
  const homeTitle = 'translation.homesss.title'; // Type 'string' - Typo 'homesss': the translation doesn't exist, leading to a runtime error.
  // Use
  type LocaleKeyPages = 'home' | 'about' | 'contact';
  type TranslationKey = `translation.${LocaleKeyPages}.${string}`; // Type TranslationKey = `translation.home.${string}` | `translation.about.${string}` | `translation.contact.${string}`
  const homeTitle: TranslationKey = 'translation.home.title';
  ```

- CSS Utilities - Avoid raw strings for color values, which can lead to invalid or non-existent colors. Use template literal types to enforce valid color names and values.

  ```ts
  // Avoid
  const color = 'blue-450'; // Type 'string' - Color 'blue-450' doesn't exist, leading to a runtime error.
  // Use
  type BaseColor = 'blue' | 'red' | 'yellow' | 'gray';
  type Variant = 50 | 100 | 200 | 300 | 400;
  type Color = `${BaseColor}-${Variant}` | `#${string}`; // Type Color = "blue-50" | "blue-100" | "blue-200" ... | "red-50" | "red-100" ... | #${string}
  const iconColor: Color = 'blue-400';
  const customColor: Color = '#AD3128';
  ```

- Database queries - Avoid using raw strings for table or column names, which can lead to typos and invalid queries. Use template literal types to define valid tables and column combinations.

```ts
// Avoid
const query = 'SELECT name FROM usersss WHERE age > 30'; // Type 'string' - Typo 'usersss': table doesn't exist, leading to a runtime error.
// Use
type Table = 'users' | 'posts' | 'comments';
type Column<TTableName extends Table> =
  TTableName extends 'users' ? 'id' | 'name' | 'age' :
  TTableName extends 'posts' ? 'id' | 'title' | 'content' :
  TTableName extends 'comments' ? 'id' | 'postId' | 'text' :
  never;

type Query<TTableName extends Table> = `SELECT ${Column<TTableName>} FROM ${TTableName} WHERE ${string}`;
const userQuery: Query<'users'> = 'SELECT name FROM users WHERE age > 30'; // Valid query
const invalidQuery: Query<'users'> = 'SELECT title FROM users WHERE age > 30'; // Error: 'title' is not a column in 'users' table.
```
