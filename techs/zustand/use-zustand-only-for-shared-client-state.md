---
title: "Use Zustand Only for Shared Client State"
whenToRead: "Before choosing Zustand for new state or moving local, URL, or server state into a shared store."
impact: "HIGH"
impactDescription: "prevents global stores from duplicating local, URL, or server-owned state"
tags: "zustand, state-ownership, server-state, local-state, url-state"
---

## Use Zustand Only for Shared Client State

Use Zustand for client state that is genuinely shared across unrelated components. Keep one-component interaction state local, keep shareable navigation state in the URL, and keep fetched server data in the project's server-state layer.

**Incorrect:**

```tsx
type ProjectsStore = {
  selectedTab: "active" | "archived";
  draftName: string;
  projects: Array<Project>;
  setProjects: (projects: Array<Project>) => void;
};

export const useProjectsStore = create<ProjectsStore>()((set) => ({
  selectedTab: "active",
  draftName: "",
  projects: [],
  setProjects: (projects) => set({ projects }),
}));
```

**Correct:**

```tsx
function ProjectListPage() {
  const [draftName, setDraftName] = useState("");
  const selectedTab = Route.useSearch({ select: (search) => search.tab ?? "active" });
  const projectsQuery = useSuspenseQuery(projectQueries.byTab(selectedTab));
  const sidebarOpen = useWorkspaceUiStore((state) => state.sidebarOpen);

  return (
    <ProjectList
      draftName={draftName}
      onDraftNameChange={setDraftName}
      projects={projectsQuery.data}
      sidebarOpen={sidebarOpen}
    />
  );
}
```

**Guidelines:**

- Use component state for ephemeral form inputs, toggles, popovers, and draft values owned by one subtree.
- Use URL search params for filters, pagination, tabs, and state users should be able to share or restore.
- Use TanStack Query or the existing API layer for server data, cache invalidation, and background refetching.
- Use Zustand for shared client-only state such as UI chrome, editor state, command palette state, and local draft workflows.

References: Synthesized from the Zustand guidance sources listed in the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
