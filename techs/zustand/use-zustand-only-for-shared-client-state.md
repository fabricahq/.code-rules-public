---
title: "Use Zustand only for shared client state"
whenToRead: "Before planning, writing, changing, or reviewing where React app state lives, such as adding a Zustand store or field, storing fetched data, adding async store actions, or holding form, filter, or UI state."
impact: "HIGH"
impactDescription: "Server data, URL state, or single-component state kept in a global store goes stale, cannot be shared by link, and couples unrelated components."
tags: "zustand, state-management, server-state, url-state"
---

## Use Zustand only for shared client state

Put state in Zustand only when it is client-owned and shared by components that are not close in the tree.
Keep single-component state local, shareable navigation state in the URL, and server data in the project's server-state layer, such as TanStack Query.

### Implementation

- Use component state for form inputs, toggles, popovers, and drafts owned by one subtree.
- Use URL search params for filters, sorting, pagination, and tabs that users should be able to share, bookmark, or restore with back.
- Use the server-state layer for data fetched from an API, including caching, refetching, and invalidation after mutations.
- Use Zustand for client-only state that several distant components share, such as UI chrome, editor selection, a command palette, or a local draft workflow.
- Use async store actions only for client-owned workflows, such as device APIs, local exports, or multi-step commands.
  Model their progress as a status union, such as `'idle' | 'pending' | 'success' | 'error'`, clear errors when retrying, and handle failures.

### Rationale

A global store has no notion of freshness, so fetched data kept there goes stale and must be refetched and invalidated by hand, which is what a server-state library does for you.
State that belongs in the URL is lost on refresh and cannot be shared when it lives in a store.
State used by one component becomes a global dependency that other code can change unexpectedly.

### Examples

#### Application: Mixed kinds of state in one store

**Incorrect (counterexample):**

```ts
type ProjectsStore = {
  selectedTab: 'active' | 'archived';
  draftName: string;
  projects: Array<Project>;
  loadProjects: () => Promise<void>;
};

export const useProjectsStore = create<ProjectsStore>()((set) => ({
  selectedTab: 'active',
  draftName: '',
  projects: [],
  loadProjects: async () => {
    const response = await fetch('/api/projects');
    set({ projects: await response.json() });
  },
}));
```

The tab cannot be shared by link, the draft is global although one form uses it, and the projects never refresh after another user changes them.

**Correct:**

```tsx
function ProjectListPage() {
  const [draftName, setDraftName] = useState('');
  const { tab } = Route.useSearch();
  const { data: projects } = useSuspenseQuery(projectQueries.byTab(tab));
  const sidebarOpen = useWorkspaceUiStore((state) => state.sidebarOpen);
  // ...
}
```

Each kind of state lives in the layer built for it, and only the shared sidebar state is in Zustand.

#### Application: A client-owned async workflow

**Correct:**

```ts
type ExportStore = {
  status: 'idle' | 'pending' | 'success' | 'error';
  errorMessage: string | null;
  exportDraft: (draftId: string) => Promise<void>;
  resetExport: () => void;
};

export const useExportStore = create<ExportStore>()((set) => ({
  status: 'idle',
  errorMessage: null,
  exportDraft: async (draftId) => {
    set({ status: 'pending', errorMessage: null });
    try {
      await exportLocalDraft(draftId);
      set({ status: 'success' });
    } catch (error) {
      set({ status: 'error', errorMessage: error instanceof Error ? error.message : 'Export failed' });
    }
  },
  resetExport: () => set({ status: 'idle', errorMessage: null }),
}));
```

### Validation

For each store field, check who owns the data and who reads it.
Fields holding fetched server data, URL-worthy navigation state, or state read by one component should move to the matching layer.

An async action for a client-owned workflow, such as a local export, is not a violation.
