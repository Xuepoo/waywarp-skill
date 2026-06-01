---
name: waywarp
description: Keyboard-driven mouse and cursor control for Wayland compositors (Hyprland, Niri, Sway, River) using hint-based grids and absolute coordinates.
---

# Waywarp Agent Skill

This skill equips AI agents with the capability to programmatically control the mouse cursor, simulate hardware clicks, scrolls, and drag gestures under Wayland compositors (wlroots-based, e.g. Hyprland, Sway, Niri, River).

## Prerequisite
The `waywarp` Rust binary must be installed on the host system and available in the system `$PATH`.

## How to use this Skill

AI Agents should use the non-interactive Agent CLI mode of `waywarp` to control the host system screen efficiently without blocking overlays.

### 1. Retrieve Screen Coordinates of All Grid Hints
To see what clickable areas are currently indexed on the display, list all hints as structured JSON:
```bash
waywarp --list-hints --format json
```
**JSON Schema Output:**
```json
{
  "hints": [
    {"label": "aaa", "x": 45, "y": 25, "screen": 0},
    {"label": "aab", "x": 135, "y": 25, "screen": 0}
  ]
}
```
*Note:* In multi-monitor setups, `label` tags will have 3 characters. The first letter identifies the screen index (e.g. `a` for screen 0, `s` for screen 1).

### 2. Programmatic Hint Selection & Click
To click on a specific visual target matching a hint label:
```bash
waywarp --select "aaa"
```
This warp simulates a physical left click on the selected label coordinates and triggers the post-select action chain defined in the user's config file (e.g., executing callbacks).

### 3. Direct Coordinate Warping & Clicks
If you already possess raw pixel coordinates (e.g., through visual screen parsing or screenshot annotations):
```bash
# Move cursor to absolute pixel coordinates (x=800, y=450) and trigger left click
waywarp --move-to 800 450 --click left

# Move cursor to coordinate (x=1024, y=768) and trigger right click
waywarp --move-to 1024 768 --click right
```

### 4. Relative Cursor Movement & Clicks
If you need to make relative cursor adjustments (e.g., fine-tuning position, moving in small increments, dragging relative distances):
```bash
# Move cursor relative to its current position by X=+50 pixels, Y=-30 pixels, and trigger left click
waywarp --move-by 50 -30 --click left

# Move cursor down by 100 pixels (dx=0, dy=100) and trigger right click
waywarp --move-by 0 100 --click right
```

### 5. Interactive Keyboard Overlay (Human/Co-pilot mode)
To open the transparent, fullscreen interactive overlay layout across connected monitors and grab keyboard focus:
```bash
waywarp
```
*   Type matching letters in sequence to select hints.
*   Type first letter to isolate target monitor in multi-screen environments.
*   Press `Escape` to cancel and exit.
*   Press `Backspace` to undo the last character.
*   Press `Enter` to force selection on matching prefixes.
