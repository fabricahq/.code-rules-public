---
title: "Keep Async Actions Client-Owned"
whenToRead: "Before adding asynchronous actions to a Zustand store, especially when server data or HTTP calls are involved."
impact: "MEDIUM-HIGH"
impactDescription: "keeps server data in the data layer while making client-only async workflows explicit"
tags: "zustand, async-actions, server-state, status, errors"
---

## Keep Async Actions Client-Owned

Async Zustand actions should coordinate client-owned workflows, not replace the server-state layer. When an async action is appropriate, model status and errors explicitly and reset them deliberately.

**Incorrect:**

```ts
type ProductsStore = {
  products: Array<Product>;
  loading: boolean;
  loadProducts: () => Promise<void>;
};

export const useProductsStore = create<ProductsStore>()((set) => ({
  products: [],
  loading: false,
  loadProducts: async () => {
    set({ loading: true });
    const response = await fetch("/api/products");
    set({ products: await response.json(), loading: false });
  },
}));
```

**Correct:**

```ts
type ExportDraftStore = {
  status: "idle" | "pending" | "success" | "error";
  errorMessage: string | null;
  exportDraft: (draftId: string) => Promise<void>;
  resetExportStatus: () => void;
};

export const useExportDraftStore = create<ExportDraftStore>()((set) => ({
  status: "idle",
  errorMessage: null,
  exportDraft: async (draftId) => {
    set({ status: "pending", errorMessage: null });
    try {
      await exportLocalDraft(draftId);
      set({ status: "success" });
    } catch (error) {
      set({
        status: "error",
        errorMessage: error instanceof Error ? error.message : "Export failed",
      });
    }
  },
  resetExportStatus: () => set({ status: "idle", errorMessage: null }),
}));
```

**Guidelines:**

- Use TanStack Query or the existing API layer for HTTP reads, mutations, caching, and invalidation.
- Use async Zustand actions for local device APIs, optimistic client drafts, command flows, or other client-owned workflows.
- Represent async state with discriminated statuses such as `idle`, `pending`, `success`, and `error`.
- Clear stale errors when retrying, closing, or resetting the workflow.

References: Synthesized from the Zustand guidance sources listed in the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
