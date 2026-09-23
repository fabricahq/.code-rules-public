---
title: "Do not define components inside components"
whenToRead: "Before planning, writing, changing, reviewing, or diagnosing React components that declare other components during render, or when inputs lose focus or state resets on every render."
impact: "HIGH"
impactDescription: "A component defined during render is a new type each time, so React remounts it and loses its state, focus, and DOM on every parent render."
tags: "react, components, remount, state"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rerender-no-inline-components.md
    description: "Adapted from the Vercel Agent Skills rule rerender-no-inline-components: restructured to the rule template with a rationale, exceptions, and validation."
---

## Do not define components inside components

Declare components at module level and pass them the data they need as props.
Do not create a component function or class inside another component's render.

### Implementation

- Move nested component definitions to module level, and pass the parent values they read as props.
- When a nested component exists only to reuse some JSX, call a plain function that returns JSX, or inline the JSX, instead of rendering it as a component.
- Creating an element such as `<Avatar />` inside render is fine; the problem is creating the component type itself inside render.

### Rationale

React decides whether to keep a component's state by comparing its type with the previous render.
A component defined inside another is a new function on every render, so React treats it as a different type, unmounts the old instance, and mounts a new one.
The child loses its state, focus, and DOM nodes, and its Effects run cleanup and setup again.

### Examples

**Incorrect (counterexample):**

```tsx
function UserProfile({ user, theme }: { user: User; theme: Theme }) {
  const Avatar = () => (
    <img src={user.avatarUrl} className={theme === 'dark' ? 'avatar-dark' : 'avatar-light'} />
  );

  return (
    <div>
      <Avatar />
    </div>
  );
}
```

`Avatar` is recreated each time `UserProfile` renders, so it remounts every time.
If it held an input, the input would lose focus on every keystroke.

**Correct:**

```tsx
function Avatar({ src, theme }: { src: string; theme: Theme }) {
  return <img src={src} className={theme === 'dark' ? 'avatar-dark' : 'avatar-light'} />;
}

function UserProfile({ user, theme }: { user: User; theme: Theme }) {
  return (
    <div>
      <Avatar src={user.avatarUrl} theme={theme} />
    </div>
  );
}
```

### Validation

Search component bodies for function or arrow declarations that start with a capital letter and are rendered as JSX elements.
Symptoms that point to this bug include inputs losing focus on each keystroke, animations restarting, and Effects re-running on every parent render.

A lowercase helper that returns JSX and is called as a function, not rendered as `<Helper />`, is not a violation.
