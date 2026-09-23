---
title: "Lift shared component state into a provider behind an interface"
whenToRead: "Before planning, writing, changing, or reviewing React components whose state is needed by siblings outside the component, or reusable UI that must work with different state sources such as local state, a store, or server sync."
impact: "MEDIUM"
impactDescription: "State trapped inside one component forces siblings to sync through Effects or refs, and UI coupled to one state source cannot be reused with another."
tags: "react, state, context, providers, composition"
attribution:
  - url: https://github.com/vercel-labs/agent-skills/tree/4ec6f84b61cd3c931046c3e6e398f3ae7de372f7/skills/composition-patterns/rules
    description: "Adapted from three Vercel Agent Skills rules (state-lift-state, state-context-interface, and state-decouple-implementation): merged three overlapping rules on lifting state, generic context interfaces, and decoupling state from UI, and restructured to the rule template."
---

## Lift shared component state into a provider behind an interface

When components outside a piece of UI need its state or actions, move that state into a provider component.
Expose it through a context with a stable interface, such as `state`, `actions`, and `meta`, so the UI parts depend on the interface rather than on how the state is stored.

### Implementation

- Define the context value as an interface: the state the UI reads, the actions it calls, and supporting references such as an input ref.
- Write one provider per state source, such as local `useState` for an ephemeral form and a store hook for synchronized data, each implementing the same interface.
- Have UI parts read the context, not a specific store hook.
- Place any component that needs the state, including buttons or previews outside the main UI, inside the provider.
- Keep state local when only one component uses it; a provider adds indirection that must pay for itself.

### Rationale

When sibling components need state owned by another component, the usual workarounds are Effects that copy state upward or refs read at submit time, both of which drift or miss updates.
A provider places the state above everyone who needs it.
A shared interface also lets the same UI parts work with different state sources, because only the provider knows how state is stored.

### Examples

#### Application: Siblings that need the state

**Incorrect (counterexample):**

```tsx
function ForwardMessageDialog() {
  const [input, setInput] = useState('');
  return (
    <Dialog>
      <ForwardMessageComposer onInputChange={setInput} />
      <MessagePreview input={input} />
    </Dialog>
  );
}

function ForwardMessageComposer({ onInputChange }: { onInputChange: (input: string) => void }) {
  const [state, setState] = useState(initialState);
  useEffect(() => {
    onInputChange(state.input);
  }, [state.input, onInputChange]);
  // ...
}
```

The dialog keeps a copy of the composer's state that an Effect syncs after each render.

**Correct:**

```tsx
function ForwardMessageProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState(initialState);
  const submit = useForwardMessage();
  const inputRef = useRef<HTMLTextAreaElement>(null);

  return (
    <ComposerContext value={{ state, actions: { update: setState, submit }, meta: { inputRef } }}>
      {children}
    </ComposerContext>
  );
}

function ForwardMessageDialog() {
  return (
    <ForwardMessageProvider>
      <Dialog>
        <ForwardMessageComposer />
        <MessagePreview />
        <ForwardButton />
      </Dialog>
    </ForwardMessageProvider>
  );
}
```

`MessagePreview` and `ForwardButton` read the context directly, even though they are outside the composer.

#### Application: The same UI with a different state source

**Correct:**

```tsx
function ChannelProvider({ channelId, children }: { channelId: string; children: ReactNode }) {
  const { state, update, submit } = useSyncedChannel(channelId);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  return (
    <ComposerContext value={{ state, actions: { update, submit }, meta: { inputRef } }}>
      {children}
    </ComposerContext>
  );
}
```

The composer parts work unchanged inside either provider.

### Validation

Search for Effects that copy a child's state into a parent, and for refs read only to extract another component's state on submit.
Check that reusable UI parts read the shared context rather than importing a specific store hook.

State used by a single component and kept local is not a violation.
