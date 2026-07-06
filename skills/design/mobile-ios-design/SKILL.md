---
name: mobile-ios-design
description: Use when designing or implementing native iOS interfaces with Apple HIG, SwiftUI, SF Symbols, Dynamic Type, navigation, gestures, accessibility, or platform-native polish.
---

# iOS Mobile Design

Use this skill for focused design work in this task family. Keep the active guidance concise, and open supporting references only when their detail is needed.

## When to use

- Designing iPhone or iPad flows that should feel native to Apple platforms.
- Implementing SwiftUI layout, navigation, controls, sheets, gestures, or adaptive behavior.
- Checking iOS accessibility, Dynamic Type, dark mode, SF Symbols, and HIG alignment.

## Workflow

1. Identify device classes, OS targets, user task, navigation model, and Apple platform conventions.
2. Choose SwiftUI and HIG patterns that fit the content hierarchy and interaction model.
3. Check Dynamic Type, VoiceOver, contrast, touch targets, safe areas, orientation, and iPad adaptation.
4. Specify component, navigation, typography, symbol, and state guidance with implementation notes.
5. List simulator/device checks and any trade-offs against HIG recommendations.

## Constraints

- Prefer system controls, materials, SF Symbols, typography, and gestures before custom replacements.
- Do not assume fixed text sizes or layouts; support Dynamic Type and localization.
- Avoid Android/web interaction patterns when an established iOS convention is clearer.

## References

Read only the sections needed for the task:

- [references/hig-patterns.md](references/hig-patterns.md) — Apple HIG-aligned interface, control, and interaction patterns.
- [references/ios-navigation.md](references/ios-navigation.md) — iOS navigation patterns and hierarchy guidance.
- [references/swiftui-components.md](references/swiftui-components.md) — SwiftUI component and layout examples.
- [references/full-guidance.md](references/full-guidance.md) — Source guidance preserved from the original skill.

## Output

Return iOS design recommendations with SwiftUI/HIG notes, accessibility checks, and device validation cases.
