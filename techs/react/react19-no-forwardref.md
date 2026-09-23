---
title: "Accept ref as a prop in React 19"
whenToRead: "Before writing, changing, or reviewing React 19 or newer components that forward a ref to a child element, or code that uses forwardRef."
impact: "LOW"
impactDescription: "forwardRef adds a wrapper that React 19 no longer needs and plans to deprecate."
tags: "react, react-19, refs"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/composition-patterns/rules/react19-no-forwardref.md
    description: "Adapted from the Vercel Agent Skills rule react19-no-forwardref: narrowed to ref forwarding and restructured to the rule template."
---

## Accept ref as a prop in React 19

In React 19 and newer, accept `ref` as an ordinary prop in function components instead of wrapping them in `forwardRef`.

### Implementation

- Declare `ref` in the component's props type and pass it to the element or child that should receive it.
- Convert existing `forwardRef` components when you change them; `forwardRef` still works in React 19.
- Keep `forwardRef` in code that must also support React 18 or earlier.

### Rationale

React 19 passes `ref` to function components as a prop, so the `forwardRef` wrapper only adds indirection.
The React team has said it plans to deprecate `forwardRef` in a future version.

### Examples

**Incorrect (counterexample):**

```tsx
const SearchInput = forwardRef<HTMLInputElement, SearchInputProps>((props, ref) => (
  <input ref={ref} {...props} />
));
```

**Correct:**

```tsx
function SearchInput({ ref, ...props }: SearchInputProps & { ref?: React.Ref<HTMLInputElement> }) {
  return <input ref={ref} {...props} />;
}
```

### Validation

Search React 19 code for `forwardRef` in new or changed components.

`forwardRef` in a library that supports React 18 is not a violation.
