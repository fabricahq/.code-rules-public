---
title: "Use Activity to hide UI that should keep its state"
whenToRead: "Before writing, changing, or reviewing React UI that is shown and hidden repeatedly and should keep its state while hidden, such as tabs, drawers, or menus, in React 19.2 or newer."
impact: "MEDIUM"
impactDescription: "Unmounting hidden UI discards its state, and hiding it with CSS alone keeps its Effects running."
tags: "react, activity, state"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/blob/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/react-best-practices/rules/rendering-activity.md
    description: "Adapted from the Vercel Agent Skills rule rendering-activity: restructured to the rule template with Effect behavior and version requirements."
---

## Use Activity to hide UI that should keep its state

When UI toggles between visible and hidden and should keep its state while hidden, wrap it in `<Activity mode={visible ? 'visible' : 'hidden'}>` instead of unmounting it.

### Implementation

- Use `Activity` for content that users return to, such as tabs, drawers, or a menu with expensive contents.
- Expect hidden content's Effects to be cleaned up and set up again when it becomes visible, so subscriptions stop while hidden.
- Keep conditional rendering for UI that should start fresh each time it appears.
- `Activity` requires React 19.2 or newer.

### Rationale

Conditional rendering unmounts hidden UI, which discards its state, such as form input and scroll position.
Hiding it with CSS keeps its state but also keeps its Effects running.
`Activity` hides the content with `display: none`, keeps its state, and pauses its Effects.

### Examples

**Incorrect (counterexample):**

```tsx
{activeTab === 'settings' && <SettingsForm />}
```

Switching tabs discards anything the user typed in the settings form.

**Correct:**

```tsx
<Activity mode={activeTab === 'settings' ? 'visible' : 'hidden'}>
  <SettingsForm />
</Activity>
```

### Validation

Enter data in the content, hide it, and show it again; the data should remain.
Check that subscriptions in hidden content stop while it is hidden.

Unmounting content that should reset when it reappears is not a violation.
