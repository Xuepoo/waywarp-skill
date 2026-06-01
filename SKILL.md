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

### 6. Continuous Keyboard Normal Mode (Cursor Mode)
To enter continuous keyboard-driven cursor control mode directly from the CLI:
```bash
waywarp --normal
```
**Controls in Normal Mode:**
*   `h` / `j` / `k` / `l` or Arrow keys: Move cursor left/down/up/right continuously.
*   `Shift` (hold): Multiply movement speed by 3x (Fast Acceleration).
*   `Control` (hold): Divide movement speed by 4x (Precision Deceleration).
*   `f` or `Return`: Perform a Mouse Left Click.
*   `d`: Perform a Mouse Right Click.
*   `s`: Perform a Mouse Middle Click.
*   `u`: Scroll Up.
*   `e`: Scroll Down.
*   `Escape` or `q`: Exit Normal Mode gracefully.

### 7. AI Visual Screen Scanner (Token-saving GUI Layout Grid)
If you need to analyze the current screen layout dynamically, run the layout scanner (`waywarp-scanner`) to detect GUI controls and output exact coordinates in logical units (extremely token-saving, bypassing large screenshots to VLMs):
```bash
# 1. Download EasyOCR and YOLOv8 models locally (one-time setup)
waywarp-scanner download-models

# 2. Capture screen and output structured text-only GUI JSON grid
waywarp-scanner scan
```
**JSON Output Format:**
```json
{
  "screen_width": 1920,
  "screen_height": 1080,
  "elements": [
    {
      "id": 0,
      "type": "button",
      "text": "Login",
      "center": [100.0, 50.0],
      "bbox": [80.0, 40.0, 40.0, 20.0],
      "monitor_index": 0,
      "confidence": 0.95
    }
  ]
}
```
You can use the returned `center` coordinates directly to warp the cursor and click:
```bash
waywarp --move-to 100.0 50.0 --click left
```
