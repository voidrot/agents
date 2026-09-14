---
name: screen-reader-testing
description: "Manually test implemented web interfaces with a screen reader and keyboard, and report environment-specific observed behavior; use for assistive-technology validation or diagnosis of names, roles, states, forms, dynamic updates, dialogs, menus, and focus."
---

# Screen Reader Testing

Use this skill to obtain manual evidence for an implemented web interaction with a real screen reader and keyboard. It tests the rendered experience; it does not choose a visual design, prescribe a generic accessibility implementation, certify legal or conformance status, or turn every feature into a coverage matrix.

Treat each screen reader, browser, operating-system, version, and configuration combination as a distinct test environment. A result in one environment is evidence for that environment only.

## Workflow

1. **Define the smallest testable journey.** Read the request, acceptance criteria, affected route or component, and existing known issue. State the starting URL or app state, user goal, required interactions, expected user-observable outcome, and any setup data. Select only the scenarios that exercise the changed or suspected behavior; include failure and recovery only when the journey exposes them.

2. **Record the environment before testing.** Capture the operating system, browser and version, screen reader and version when available, input method, relevant screen-reader mode or settings, zoom, and build or deployment identifier. Use the requested environment. If none is specified, use an environment actually available and label it as such; do not substitute an emulator, accessibility-tree inspection, or automated audit for screen-reader evidence.

3. **Establish a repeatable start state.** Load or reset the journey without leaving stale focus, prior validation messages, or cached transient UI that would alter announcements. Note whether the test starts from page load, direct navigation, or an already-open application state. Stop and report the missing prerequisite if authentication, test data, a device, or the requested assistive technology is unavailable.

4. **Test reading and control discovery.** Navigate both by ordinary keyboard focus and the screen reader's available document or element navigation. For each relevant landmark, heading, link, control, or custom widget, record what is announced—not what the markup was intended to expose. Check that its accessible name identifies its purpose, its role matches how it operates, and its relevant state or value is conveyed. Include expanded/collapsed, selected, checked, unavailable, required, invalid, busy, current, and value information only where the interaction uses them.

5. **Exercise forms as a complete recovery path.** Reach fields using the same navigation a user would use, then verify the label, instructions, required status, current value, and available choices. Submit an invalid but safe input and observe whether the error identifies the field and problem, whether invalid state is exposed, whether focus movement is useful and predictable, and whether entered values and a path to correction remain available. Correct and resubmit when the requested journey includes success. Do not infer an announcement merely because an error is visible.

6. **Trigger dynamic changes deliberately.** Perform the action that loads, saves, filters, validates, or otherwise changes content. Capture the triggering control's before and after state, the spoken result, when it was spoken relative to the action, and whether it was disruptive or absent. Distinguish a required announcement from ordinary content the user can discover through focus or reading; avoid reporting a missing announcement without first identifying the user task it prevents.

7. **Test temporary contexts and composite controls.** For dialogs, menus, popovers, disclosure controls, tabs, comboboxes, and similar interactions, record:
   - the invocation announcement and initial focus destination;
   - keyboard operation, including expected activation, navigation, dismissal, and any screen-reader mode coordination needed to operate it;
   - announced name, role, and changing state while it is open or active;
   - whether focus remains usable inside the temporary context and whether background interaction is prevented when applicable; and
   - the focus destination after close, cancel, selection, or error.
   Test only controls present in the journey. Do not extrapolate findings from one widget instance to unrelated widgets.

8. **Separate observation from diagnosis.** Record exact steps, actual speech or a faithful short transcription, focus location, and visible result. Repeat an unexpected result from a clean state once when practical. Inspect the rendered accessibility tree, DOM, or application code only to form a falsifiable explanation after recording the user-observable result. Hand implementation work to `efficient-web-development`; use `efficient-react` when the fault is specifically in React component behavior. Leave visual hierarchy or interaction-intent decisions to `efficient-web-design`.

9. **Report bounded evidence and next actions.** Mark every scenario as passed, failed, blocked, or inconclusive for the recorded environment. For a failure, provide the smallest reproduction, expected user-observable result, actual result, and a likely boundary only when supported by evidence. State untested environments and scenarios explicitly. Do not claim cross-browser, cross-screen-reader, legal, or conformance coverage from this run.

## Report template

```markdown
## Manual screen-reader test

**Environment:** OS/version; browser/version; screen reader/version; input method; relevant settings; build/URL
**Start state:**

| Scenario | Steps | Expected user-observable result | Observed speech/focus/result | Status |
| --- | --- | --- | --- | --- |
| | | | | pass / fail / blocked / inconclusive |

**Failures or inconclusive results:**
- Reproduction:
- Expected:
- Actual:
- Evidence and suspected boundary, if any:

**Limits:** Untested environments, unavailable prerequisites, and scenarios intentionally excluded.
```

## Completion evidence

Report the tested journey and actual environment; keyboard and screen-reader navigation performed; observed names, roles, states, announcements, and focus behavior; and all blocked, inconclusive, or untested scope. Keep transcripts short enough to identify the behavior, and remove test-account data or other sensitive content before sharing.
