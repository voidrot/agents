# Common validation and capture-path triage

Validation must preserve application behavior and data safety. A test event is a remote transmission and requires explicit authorization. A deliberate hard crash, deployment, or Sentry/cloud change needs separate explicit authorization.

## Local-first checks

1. Record runtime/framework and installed SDK version without exposing configuration values.
2. Inspect initialization and boundary order, existing automatic integrations, manual capture calls, filters, scopes, and shutdown hooks.
3. Trace one representative unhandled path and one handled path. Confirm one owner per path and unchanged response/fallback/rethrow/exit behavior.
4. Run repository-native formatting, lint, type, build, and tests. Prefer mocks/fakes that assert capture call count, original exception identity/cause, scoped allowlisted context, filter outcomes, and preserved propagation.
5. Exercise expected validation/control-flow errors locally and assert they are not reported unless policy explicitly says otherwise.

Do not assert network delivery from a returned event ID, a flush return, SDK debug text, or lack of local exceptions.

## Authorized controlled capture

Only after explicit authorization, use a safe non-production environment and one synthetic exception with a non-sensitive unique marker such as a random opaque test label plus UTC time. Put no customer, request, credential, or production payload data in it. Prefer a handled synthetic exception over a process crash. Do not add a public debug route; if a temporary route/harness is explicitly authorized, protect it and remove it immediately.

Observe and record without copying raw event content:

- expected project/environment and bounded time window;
- error event exists and is an exception, not merely a Log, breadcrumb, message, or Issue search result;
- expected exception type, stack, cause chain, and mechanism;
- safe intended tags/context only, with forbidden data absent;
- exactly one event for one action;
- original UI/HTTP/job behavior is unchanged;
- expected errors are filtered while an unexpected synthetic exception passes;
- default grouping or the explicitly intended fingerprint behavior;
- async/worker/serverless/mobile/native lifecycle result and any loss caveat;
- readable frames, or a statement that matching source maps/debug symbols are a prerequisite outside this skill.

An event observed remotely is positive evidence for that path only. It does not prove all crashes are captured or future delivery is guaranteed.

## Temporary diagnostics

Enable SDK diagnostics only when needed and authorized if it changes configuration. Keep them local, time-bounded, and free of raw payloads. Never paste production SDK debug output into evidence. Remove temporary handlers, routes, markers, debug options, and test-only context; rerun local checks afterward.

## Symptom to check map

| Symptom | First checks |
|---|---|
| No error event | Exact runtime docs; SDK initialized before failure; DSN presence without printing it; disabled integration/filter; boundary consumes error; lifecycle ends before handoff; network policy. |
| Message/Log exists but no exception event | Code used logger/message/breadcrumb instead of exception capture; verify the event API and preserve the original exception. |
| Duplicate events | Manual capture plus rethrow; nested/overlapping boundaries; client plus server; native plus managed bridge; dev double invocation; repeated retries. Assign one owner. |
| Missing stack or cause | Stringified/reconstructed exception; missing explicit stack where the exact SDK requires one; wrapping lost cause; non-Error throw; mismatched source map/debug symbol prerequisite. |
| Wrong or leaked context | Global scope used for request/user data; async/thread/goroutine/isolate context not propagated or cleared; native/managed scope sync assumptions; broad automatic request collection. |
| Expected noise | Filter at semantic boundary; check status/type taxonomy; avoid broad message substring rules; test an unexpected neighbor still passes. |
| Over-grouped or fragmented | Remove custom fingerprint first; inspect stack/cause stability and build artifacts; define merge/split invariant before a bounded override. |
| Missing worker/serverless event | Handler/wrapper ordering; async completion ownership; platform wait/flush guidance; abrupt exit. Never add arbitrary sleeps. |
| Missing mobile/native crash | Correct managed/native layer enabled; crash persisted for next launch if current docs say so; app restarted; matching debug symbols prerequisite. Do not promise capture of OOM/kill cases. |
| Capture changed user behavior | Restore original throw/response/fallback first; isolate telemetry errors; remove capture-driven retry/exit/return changes. |

## Completion record

Report files/config reviewed or changed, exact runtime reference and current URLs checked, local commands/results, authorization obtained, controlled marker and time window (not payload), observed count and event characteristics, original behavior, context/filter/grouping/lifecycle results, temporary diagnostics removed, skipped remote/deploy/cloud/crash checks, and remaining unconfirmed behavior.
