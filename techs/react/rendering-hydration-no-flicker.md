---
title: "Render client-only preferences without a flash or hydration error"
whenToRead: "Before planning, writing, changing, or reviewing server-rendered React UI that depends on client-only data, such as a theme or layout preference stored in localStorage."
impact: "MEDIUM"
impactDescription: "Reading client-only data during server render crashes, and reading it after hydration shows a visible flash of the wrong content."
tags: "react, ssr, hydration, theme"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-hydration-no-flicker.md
    description: "Adapted from the Vercel Agent Skills rule rendering-hydration-no-flicker: restructured to the rule template, added the server-readable cookie option, and corrected the script example to suppress the expected attribute mismatch."
---

## Render client-only preferences without a flash or hydration error

When server-rendered UI depends on a preference the server cannot read, apply it before the first paint with a small inline script, and mark the element the script changes with `suppressHydrationWarning`.
When the server can read the preference, render it on the server instead.

### Implementation

- Prefer storing the preference where the server can read it, such as a cookie, and render the correct value on the server.
  This needs no script and no hydration workaround.
- When the value must come from client-only storage, render a small inline script immediately after the element it affects.
  The script reads the value and sets a class or attribute before the browser paints.
- Put `suppressHydrationWarning` on that element.
  The script intentionally changes an attribute the server rendered, and React would otherwise report the mismatch.
  The prop applies only to that element's own attributes and text, one level deep.
- Keep the script small, wrap storage access in `try` / `catch`, and add a nonce if the site uses a Content Security Policy that restricts inline scripts.
- Do not read `localStorage` during render; it does not exist on the server.

### Rationale

The server cannot see client-only storage, so it renders a default.
Reading the stored value in an Effect corrects the page only after hydration, so users see the default flash first.
An inline script runs while the HTML is parsed, before paint, so the first frame already shows the stored preference.

### Examples

#### Application: Reading storage during render

**Incorrect (counterexample):**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  const theme = localStorage.getItem('theme') ?? 'light';
  return <div className={theme}>{children}</div>;
}
```

Server rendering fails because `localStorage` does not exist there.

#### Application: Correcting the value in an Effect

**Incorrect (counterexample):**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    setTheme(localStorage.getItem('theme') ?? 'light');
  }, []);

  return <div className={theme}>{children}</div>;
}
```

The page first paints with the light theme, then switches, which users see as a flash.

**Correct:**

```tsx
const applyStoredTheme = `
  try {
    document.getElementById('theme-root').className =
      localStorage.getItem('theme') || 'light';
  } catch (error) {}
`;

function ThemeWrapper({ children }: { children: ReactNode }) {
  return (
    <>
      <div id="theme-root" className="light" suppressHydrationWarning>
        {children}
      </div>
      <script dangerouslySetInnerHTML={{ __html: applyStoredTheme }} />
    </>
  );
}
```

The script sets the stored theme before paint.
`suppressHydrationWarning` tells React that the changed `className` is expected.

### Validation

Load the page with a non-default preference stored, using a throttled network, and check that no frame shows the default value.
Check the browser console for hydration warnings.

Using a server-readable cookie instead of a script is not a violation.
