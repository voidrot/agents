# Package-specific considerations

Read the relevant section before selecting an integration pattern for that package. Confirm all behavior against the official documentation for the installed `@tanstack/*` version and framework adapter; package APIs, generated artifacts, SSR behavior, and defaults are not interchangeable across versions or adapters.

## Query

Read when changing query keys, cache lifecycle, mutations, cancellation, invalidation, optimistic updates, or SSR hydration. Verify the installed adapter's provider and hydration boundary, how request cancellation reaches the query function, and the documented rollback and error behavior for mutations.

## Router

Read when changing route declarations, search or path validation, loaders, route generation, navigation, or Router–Query handoff. Verify whether the project uses generated routes, the installed adapter's route-tree ownership, and its documented server-rendering and error-boundary behavior.

## Form

Read when changing field state, validation timing, submission, server-error mapping, or form reset/persistence. Verify the installed adapter's field/subscription model and the contract for async validation or submission; retain server-side validation and authorization.

## Table

Read when changing columns, row models, sorting, filtering, pagination, selection, or expansion. Verify which row-model features the installed package provides and whether each transform is client-side or supplied by the remote data contract.

## Virtual

Read when adding or changing virtualized list or table rendering, measurement, scrolling, or infinite-data coordination. Verify the installed adapter's measurement and scroll-container requirements, then test dynamic content and keyboard focus in the rendered application.

## Start

Read when changing server functions, server/API routes, middleware, SSR, streaming, or client/server data boundaries. Verify the installed Start version's execution boundaries and serialization rules; keep secrets and authorization decisions on the server.
