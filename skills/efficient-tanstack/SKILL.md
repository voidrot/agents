---
name: efficient-tanstack
description: Plan, implement, review, debug, or validate TanStack Query, Router, Form, Table, Virtual, and Start integrations; use for server-state, routing, form, data-grid, virtualization, or TanStack full-stack boundary work, not general React/UI design or unrelated backend work.
---

# Efficient TanStack

Use this skill for a bounded change or diagnosis involving the TanStack ecosystem. Keep framework ownership explicit: Router owns route structure and URL state; Query owns remote-data lifecycle and cache; Form owns form state and validation coordination; Table owns headless tabular state/models; Virtual owns the rendered window; Start owns its documented full-stack and server boundaries. Read [package-specific considerations](references/packages.md) when the change involves the named package; it identifies package boundaries that require verification against the installed version's official documentation.

Do not use this skill as general React component guidance, visual design direction, CSS work, an accessibility-only review, or a generic backend/API workflow. Use `efficient-testing` for the focused regression-test workflow when a changed TanStack behavior needs one.

## Workflow

1. **Establish the local contract.** Read the request, affected route/component/server boundary, and closest tests. Identify the user-visible result, source of truth, failure behavior, and whether this is a behavior change, defect, or refactor. Inspect the manifest, lockfile, package manager, framework adapter, generated artifacts, and existing providers before choosing APIs.
2. **Confirm the installed package and current documentation.** Match each `@tanstack/*` package, adapter, and version to its current official documentation. Treat imports, option names, generated-route conventions, SSR/hydration behavior, and Start APIs as version-sensitive. Do not copy a snippet between React, Solid, Vue, or Start adapters, or between major versions. If the version or adapter is absent, ask for it or make only version-independent boundary recommendations.
3. **Assign each state to one owner.** Use the smallest owner that matches its lifetime:
   - Put route hierarchy, navigation, path parameters, and shareable/search state in Router. Validate and normalize URL input at the route boundary before application code uses it.
   - Put fetched remote data, cache freshness, refetching, and mutation synchronization in Query. Keep ephemeral UI state out of the query cache.
   - Put editable values, touched/submission state, and client validation in Form. Keep final authorization and validation on the server.
   - Put columns, row models, sorting, filtering, pagination, selection, and expansion in Table. It is headless; the application owns markup and interaction controls.
   - Put visible-range calculation and item measurement in Virtual. It does not fetch data, own table state, or replace semantic interaction behavior.
   - Put Start server functions, server/API routes, middleware, SSR, and streaming at the documented Start boundary. Do not expose server-only credentials or trust client-provided authorization state.
   Keep values derivable from an existing owner derived rather than duplicated.
4. **Choose the narrow integration pattern.** Prefer the existing project pattern and one source of truth.
   - For route data, let Router decide when a route is entered or invalidated and let Query manage remote-data caching when cache behavior is needed. Use the documented Router–Query integration for the installed versions; do not create independent fetches in both a loader and component without a defined cache handoff.
   - Build stable, serializable Query keys from every request input that changes the result. Keep the key shape and request arguments aligned. After a mutation, update or invalidate only the affected key scope; add an optimistic update only when the UX requires it and every failure/cancellation path can restore the prior state.
   - Keep form drafts out of URL/search state unless the product explicitly requires a shareable or restorable value. Submit through the established mutation/server boundary, prevent duplicate submission, and map server validation errors to the relevant fields or form state.
   - For server-side table sorting, filters, and pagination, make the table state the validated request input and include it in the Query key. Do not silently combine server pagination with client-side filtering/sorting over partial data. Keep client-side modes only when the complete dataset is intentionally available.
   - Virtualize only after evidence of a large or unbounded rendered collection, a measured render/scroll problem, or an explicit scale requirement. Start with ordinary rendering for small bounded lists. Combine infinite data and virtualization only when their page, cursor, index, loading, and end-of-list contracts are explicit.
   - Use Start only when the application already uses it or the request requires its full-stack boundary. Keep browser-only code out of server execution paths and reproduce any SSR/hydration issue with a direct request plus client hydration.
5. **Implement one coherent change.** Preserve existing provider placement, route-tree generation ownership, error boundaries, and request conventions. Do not hand-edit generated route output; change its declared inputs and run the project’s documented generator when applicable. Use conventional package APIs for the installed version. Avoid wrappers, shared abstractions, persisted cache, prefetching, manual memoization, and virtualization unless the stated contract or measured evidence requires them.
6. **Model observable states deliberately.** Cover initial pending, successful data, empty data, recoverable fetch error, background refresh, mutation/submission pending, mutation failure, and retry/recovery where applicable. Distinguish an empty successful result from a failed request. Give route failures an appropriate route-level recovery path. Preserve semantic controls, labels, focus order, and keyboard operation when rendering forms, tables, or virtualized content.
7. **Verify at the changed seam.** Run the narrowest repository-supported typecheck, test, lint, build, or route-generation command, then broaden only when shared configuration or the changed boundary requires it. Exercise the relevant behavior:
   - **Router:** direct load, navigation, nested layout/error behavior, reload, and back/forward with malformed and valid URL input.
   - **Query:** first fetch, cache reuse/refetch expectations, failure/recovery, and mutation-driven synchronization without stale or duplicated results.
   - **Form:** client validation, server rejection, successful submit, repeated-submit prevention, and preservation or reset behavior required by the contract.
   - **Table:** sort/filter/page/selection behavior, empty and error states, and server request inputs when data is remote.
   - **Virtual:** long-list scrolling, dynamic-size measurement if used, loading/end boundaries, focus/keyboard behavior, and absence of overlap, gaps, or inaccessible offscreen focus.
   - **Start:** direct SSR request, client navigation/hydration, server failure handling, and absence of server-only data in browser output.
8. **Diagnose failures with a bounded probe.** Reproduce the exact symptom, reduce it to one route/query/form/table/virtual boundary, and test one falsifiable cause at a time. For stale or duplicate data, inspect provider scope, Query key inputs, enabled/precondition logic, route-loader handoff, and mutation synchronization. For lost form values, distinguish draft state from URL state and remount/reset behavior. For table mismatches, inspect whether the dataset is partial and which side owns each transform. For hydration failures, compare server and first-client output before adding guards. Retain a focused regression test for confirmed defects when practical; remove temporary instrumentation.

## Decision rules

- Prefer Router search state for shareable navigation state, not transient widget state.
- Prefer Query for data that came from a remote authority and has freshness or synchronization needs; do not use it as a replacement for ordinary local state.
- Prefer a normal semantic table or list before virtualization. Virtualization is a measured rendering optimization, not a pagination strategy.
- Do not make Table state externally controlled unless another owner must persist, synchronize, or drive it.
- Treat a server response as authoritative for permissions, validation, totals, cursors, and mutations even when client state predicts an outcome.
- Keep one query client and one router arrangement per documented application boundary unless the architecture explicitly requires otherwise; duplicate providers can split cache or navigation state.
- Do not infer exact defaults, persistence behavior, SSR guarantees, or API signatures. The installed version and current official TanStack documentation decide them.

## Completion evidence

Report only what was observed:

- affected TanStack packages, adapters, versions, and the chosen ownership boundaries;
- changed files and the source-of-truth decision for URL, remote, form, table, and virtual state;
- focused commands and manual scenarios run, with pass/fail results;
- the explicit loading, empty, error, mutation, and recovery states covered;
- measured evidence that justified any caching, prefetching, external table control, or virtualization;
- skipped checks, unavailable frontend prerequisites, version/doc uncertainty, and remaining risk.
