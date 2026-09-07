# Unsupported or undocumented runtimes

No runtime-specific Crons documentation was established here for browser, mobile, Bun, Deno, or other undocumented targets. Rust has a dedicated documentation-first boundary in [rust.md](rust.md). For the targets covered here, this is not proof that a runtime cannot emit telemetry; it is a strict boundary against claiming supported Crons capability or porting an API from Go, Python, Node, or Next.js.

Do not copy `withMonitor`, `captureCheckIn`, `monitor`, `capture_checkin`, `MonitorConfig`, scheduler helpers, version gates, or lifecycle behavior into an undocumented runtime. Rust-specific requests must follow [rust.md](rust.md) instead. For other undocumented runtimes, first locate current official platform-specific Crons documentation, confirm SDK/version and runtime scope, then update the plan from that source. If it cannot be established, report it as unknown and request a supported runtime or explicit user decision; do not create a speculative workaround.

- Platform index: <https://docs.sentry.io/platforms/>
- Node Crons reference: <https://docs.sentry.io/platforms/javascript/guides/node/crons/>
- Next.js Crons reference: <https://docs.sentry.io/platforms/javascript/guides/nextjs/crons/>
