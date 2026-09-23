---
title: "Keep Store State Serializable"
whenToRead: "Before storing runtime resources or non-serializable values in Zustand state."
impact: "MEDIUM"
impactDescription: "keeps state safe for persistence, debugging, snapshots, and lifecycle cleanup"
tags: "zustand, serializable-state, persistence, devtools, runtime-resources"
---

## Keep Store State Serializable

Store plain client state by default. Keep DOM nodes, promises, sockets, timers, abort controllers, and other runtime resources outside Zustand state.

**Incorrect:**

```ts
type UploadStore = {
  inputElement: HTMLInputElement | null;
  socket: WebSocket | null;
  retryTimer: ReturnType<typeof setTimeout> | null;
  pendingUpload: Promise<void> | null;
};

export const useUploadStore = create<UploadStore>()(() => ({
  inputElement: null,
  socket: null,
  retryTimer: null,
  pendingUpload: null,
}));
```

**Correct:**

```ts
type UploadStore = {
  selectedFileId: string | null;
  connectionStatus: "idle" | "connecting" | "connected" | "error";
  uploadStatus: "idle" | "pending" | "success" | "error";
  selectFile: (fileId: string | null) => void;
  setConnectionStatus: (status: UploadStore["connectionStatus"]) => void;
};

export const useUploadStore = create<UploadStore>()((set) => ({
  selectedFileId: null,
  connectionStatus: "idle",
  uploadStatus: "idle",
  selectFile: (selectedFileId) => set({ selectedFileId }),
  setConnectionStatus: (connectionStatus) => set({ connectionStatus }),
}));
```

**Guidelines:**

- Store IDs, statuses, preferences, and plain data instead of live runtime objects.
- Keep DOM nodes in refs, sockets and timers in effects or services, and promises in the async code that owns their lifecycle.
- Serializability matters more for persisted stores, devtools, tests, and long-lived shared state.
- Non-serializable values may be acceptable in narrow, non-persisted vanilla stores only when lifecycle ownership is explicit and documented.

References: Synthesized from the Zustand guidance sources listed in the [public library notice](https://github.com/fabricahq/.code-rules-public/blob/main/NOTICE.md).
