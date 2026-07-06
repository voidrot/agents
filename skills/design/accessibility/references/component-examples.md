# Accessibility component examples

## Web: accessible search

```html
<form role="search">
  <label for="search-input" class="sr-only">Search products</label>
  <input type="search" id="search-input" name="q" autocomplete="off" />
  <button type="submit">
    <svg aria-hidden="true" focusable="false">...</svg>
    <span class="sr-only">Submit search</span>
  </button>
</form>
```

## iOS / SwiftUI: destructive icon button

```swift
Button(action: deleteItem) {
    Image(systemName: "trash")
}
.accessibilityLabel("Delete item")
.accessibilityHint("Permanently removes this item from your list")
.accessibilityAddTraits(.isButton)
```

## Android / Compose: labelled toggle

```kotlin
Switch(
    checked = notificationsEnabled,
    onCheckedChange = onToggle,
    modifier = Modifier.semantics {
        contentDescription = "Enable notifications"
        stateDescription = if (notificationsEnabled) "On" else "Off"
    }
)
```

## Modal focus behavior

- Move focus into the modal when it opens.
- Keep keyboard focus inside the modal while open.
- Provide Escape and visible close-button exits where appropriate.
- Return focus to the trigger when the modal closes.
