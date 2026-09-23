---
title: "Create stores once, outside render"
whenToRead: "Before planning, writing, changing, or reviewing where a Zustand store is created, including stores created in components or hooks, per-instance stores, and stores used with server rendering."
impact: "HIGH"
impactDescription: "A store created during render is recreated on every render and loses its state, while a module-level store on a server is shared by every request."
tags: "zustand, store-creation, ssr, context"
---

## Create stores once, outside render

Create client-side Zustand stores once, at module scope, in a dedicated store module.
When each component instance or server request needs its own store, create a vanilla store once per instance and provide it through React context.

### Implementation

- Call `create` at module scope and export the resulting hook.
- Never call `create` inside a component, custom Hook, or render path.
- For per-instance or per-request state, create the store with `createStore` from `zustand/vanilla` inside a provider, keep it in a ref or `useState` initializer so it is created once, and read it with `useStore(store, selector)`.
- With server rendering, do not put request- or user-specific data in module-level stores, because the server shares modules across requests.
- Keep store initialization deterministic; do not read `window` or storage during creation outside persistence middleware.

### Rationale

`create` builds a new store each time it runs.
Inside a component, every render creates a fresh store with initial state, so updates are lost and subscribers attach to a store nobody else uses.
On a server, a module-level store is shared by concurrent requests, so one user's data can render in another user's page.

### Examples

#### Application: A store created during render

**Incorrect (counterexample):**

```tsx
function Panel() {
  const usePanelStore = create<PanelStore>()((set) => ({
    open: false,
    toggle: () => set((state) => ({ open: !state.open })),
  }));
  const open = usePanelStore((state) => state.open);
  // ...
}
```

Each render creates a new store, so `open` is always `false`.

**Correct:**

```ts
// panel-store.ts
export const usePanelStore = create<PanelStore>()((set) => ({
  open: false,
  toggle: () => set((state) => ({ open: !state.open })),
}));
```

#### Application: A store per instance

**Correct:**

```tsx
const EditorStoreContext = createContext<StoreApi<EditorStore> | null>(null);

function EditorStoreProvider({ initialDocumentId, children }: { initialDocumentId: string; children: ReactNode }) {
  const [store] = useState(() => createEditorStore(initialDocumentId));
  return <EditorStoreContext value={store}>{children}</EditorStoreContext>;
}

function useEditorStore<T>(selector: (state: EditorStore) => T): T {
  const store = useContext(EditorStoreContext);
  if (!store) throw new Error('useEditorStore must be used inside EditorStoreProvider');
  return useStore(store, selector);
}
```

`createEditorStore` calls `createStore` from `zustand/vanilla`, and each editor instance gets its own store, created once.

### Validation

Search components and Hooks for calls to `create` or `createStore` outside a `useState` initializer or ref.
In server-rendered apps, check that module-level stores hold no request- or user-specific data.

A module-level store for client-only UI state is not a violation.
