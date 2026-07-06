# Accessibility implementation checklist

## POUR implementation checks

### Perceivable

- Text contrast meets WCAG 2.2 AA: 4.5:1 for normal text, 3:1 for large text and UI components.
- Meaningful images and icons have text alternatives; decorative images are hidden from assistive technology.
- Content reflows without loss of function at high zoom and narrow widths.
- Motion and animation respect reduced-motion preferences.

### Operable

- All interactive controls are keyboard reachable and usable.
- Focus order follows the visual and logical task order.
- Focus indicators are visible and not obscured by sticky UI.
- Pointer targets meet the applicable platform baseline, including WCAG 2.2 target-size expectations for web UI.
- Dragging gestures have single-pointer or keyboard alternatives when required.

### Understandable

- Labels, headings, instructions, and link text describe purpose.
- Error messages identify the field, explain the issue, and suggest recovery.
- Navigation and repeated controls remain consistent.
- The UI does not unexpectedly change context on focus or input.

### Robust

- Custom widgets expose correct name, role, value, state, and properties.
- Dynamic status messages are announced through appropriate live-region/status patterns.
- HTML remains valid enough for assistive technologies to parse reliably.

## Anti-patterns

- Clickable `<div>`/`<span>` controls without native semantics and keyboard support.
- Icon-only buttons without an accessible name.
- Error or status states indicated only by color.
- Modals that trap users permanently or allow focus to leak behind the dialog.
- Redundant alt text such as "image of" or "picture of".
- Positive `tabindex` values that create an artificial focus order.

## Verification prompt

Before returning implementation guidance, state:

- The semantic control or platform role used.
- How the control is named and described.
- Keyboard/switch/screen-reader behavior.
- Focus entry, movement, visibility, and restoration behavior.
- Remaining manual checks that cannot be proven from code alone.
