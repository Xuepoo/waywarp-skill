---
name: waywarp
description: Keyboard-driven mouse and cursor control for Wayland compositors (Hyprland, Niri, Sway, River) using hint-based grids and absolute coordinates.
read_when:
  - Controlling mouse cursor on Wayland compositors
  - Programmatic cursor warping, clicking, scrolling, dragging
  - AI agent GUI automation without VLM screenshots
  - Visual screen scanning for GUI element detection
---

# Waywarp Agent Skill

This skill equips AI agents with the capability to programmatically control the mouse cursor, simulate hardware clicks, scrolls, and drag gestures under Wayland compositors (wlroots-based, e.g. Hyprland, Sway, Niri, River).

## Prerequisite
The `waywarp` Rust binary must be installed on the host system and available in the system `$PATH`.

## Testing Results
See `references/testing-results-2026-06-02.md` for comprehensive testing results and bug documentation.

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

### 8. Integrated Desktop Vimium Visual Click Mode
If you want to instantly click on a visual GUI element (button, text field, link) without sending a heavy screenshot to a VLM:
```bash
waywarp --scan
```
This single command automatically captures the Wayland screen, detects all interactive elements, overlays unique prefix-free characters over them, matches the keystroke, and left-clicks the matched target!

### 9. Combined Vision + Waywarp Workflow (for elements scanner can't detect)
When waywarp-scanner can't detect an element (system tray icons, image-based buttons), use vision_analyze + waywarp:
```bash
# 1. Screenshot
grim /tmp/screen.png

# 2. Use vision_analyze to identify element position
#    Returns approximate coordinates — often 50-200px off!

# 3. Get window geometry for coordinate conversion
hyprctl activewindow -j | python3 -c "import json,sys;w=json.load(sys.stdin);print(f'at={w[\"at\"]} size={w[\"size\"]}')"

# 4. Calculate absolute coordinates: window_at + vision_relative
# 5. Click with waywarp
waywarp --move-to ABS_X ABS_Y --click left
```

**Pitfall**: Vision model coordinate estimation is unreliable (±50-200px). Use waywarp-scanner first (more accurate), fall back to vision only for icons/images scanner can't detect. If click misses, try adjusting Y by ±50px increments.

### 10. Browser Automation Workflow (Chrome + waywarp + wtype)
For web browsing tasks (search, navigate, click links):
```bash
# Focus browser
hyprctl dispatch focuswindow "class:google-chrome"
sleep 0.3

# Navigate to URL directly (most reliable)
wtype -M ctrl -k l -m ctrl   # Ctrl+L focuses address bar
sleep 0.3
wtype "https://example.com"
sleep 0.2
wtype -k Return              # Enter to navigate
sleep 3                      # Wait for page load

# Search via address bar (Ctrl+L → type query → Enter)
wtype -M ctrl -k l -m ctrl
sleep 0.3
wtype "search query here"
sleep 0.2
wtype -k Return
sleep 3

# Open new tab
wtype -M ctrl -k t -m ctrl
sleep 1
```

**Pitfall — Web link clicking is unreliable**: Clicking links in web pages with `waywarp --move-to` often misses because:
1. Scanner detects text labels but not clickable link boundaries
2. Vision model coordinates are ±50-200px off
3. Links have small hit targets

**Workaround**: Instead of clicking links, use Ctrl+L + direct URL navigation. If you must click a link, use `waywarp --select` with hint grid (more precise than coordinate guessing), or use keyboard Tab navigation + Enter.

**Pitfall — wtype input sometimes not received**: Chrome's new tab page and some Electron apps may not receive wtype input. Always `sleep 0.3` after focusing a window before sending keystrokes. If input is ignored, try clicking the target input field first with `waywarp --move-to X Y --click left` before typing.

### 11. Complete Google Search Workflow (tested 2026-06-03)
```bash
# 1. Launch Chrome
hyprctl dispatch exec "google-chrome-stable"
sleep 3

# 2. Focus Chrome and open new tab
hyprctl dispatch focuswindow "class:google-chrome"
sleep 0.3
wtype -M ctrl -k t -m ctrl
sleep 1

# 3. Click the search box (center of new tab page)
# Chrome window at (807, 49), search box ~center at (1195, 400)
waywarp --move-to 1195 400 --click left
sleep 0.3

# 4. Type search query and search
wtype "Hermes Agent"
sleep 0.2
wtype -k Return
sleep 5  # Wait for search results

# 5. Screenshot and analyze results
grim /tmp/search.png
# Use vision_analyze to identify result positions

# 6. Navigate to result (Ctrl+L + URL is most reliable)
wtype -M ctrl -k l -m ctrl
sleep 0.3
wtype "https://github.com/NousResearch/hermes-agent"
sleep 0.2
wtype -k Return
sleep 5
```

**Lesson learned**: Direct URL navigation (Ctrl+L) is 100% reliable. Clicking links in search results is unreliable (~30% success rate). Always prefer Ctrl+L + URL over clicking links.

### 12. System Tray Icon Interaction (Limited Support)
System tray icons (QQ, Discord, etc.) are **NOT reliably clickable** via waywarp because:
1. Tray icons are rendered by the compositor, not as standard GUI elements
2. Scanner cannot detect tray icons (they're not text or standard widgets)
3. Vision model coordinates are often inaccurate for small icons

**Workarounds**:
```bash
# Option A: Use hyprctl to launch the app directly
hyprctl dispatch exec "/opt/QQ/qq --no-sandbox"

# Option B: Use wtype keyboard shortcuts if the app supports them
# (e.g., Ctrl+Alt+Q for QQ)

# Option C: If you must click a tray icon, use vision + trial-and-error
# 1. Screenshot the waybar area
grim -g "0,0 1600x50" /tmp/waybar.png
# 2. Use vision to estimate icon position (±20px error)
# 3. Try clicking at estimated position
# 4. If miss, adjust by ±10px and retry
```

**Lesson learned**: For QQ login, `hyprctl dispatch exec "/opt/QQ/qq --no-sandbox"` is more reliable than trying to click the tray icon.

## Version Status

**waywarp:** v0.1.7 (`cargo install waywarp`)
**waywarp-scanner:** v0.2.0 (`uv tool install waywarp-scanner`)

### waywarp v0.1.7 — All Agent CLI commands working
- ✅ `--select`, `--move-to`, `--move-by`, `--click`, `--print-coords` all functional
- ✅ INFO logs go to stderr (stdout is clean JSON)
- ✅ Out-of-bounds coordinates clamped to screen edges
- ✅ `--move-by` correctly calculates relative offsets and executes

### waywarp-scanner v0.2.0 — Major improvements
- ✅ Auto-serve daemon: `scan` auto-starts warm daemon (fixes cold-start inconsistency)
- ✅ Threading instead of multiprocessing (shares cached EasyOCR Reader)
- ✅ `--timing` flag for performance diagnostics
- ✅ `--no-serve` flag to force cold scan mode
- ✅ Screen resolution correct (1600x1000 logical)
- ✅ OCR text quality improved, button/menu/tab classification
- ✅ Coordinates clamped to screen bounds

### Known Remaining Issues
- ⚠️ Scanner OCR reads terminal/editor content (heuristic filters mitigate but don't eliminate)
- ⚠️ Scanner element types: mostly 'text' + some 'button' (no custom YOLO GUI model yet)
- ⚠️ System tray icons NOT clickable via waywarp (use `hyprctl dispatch exec` instead)

## Hyprland Window Management (Essential for GUI Automation)

```bash
# List all windows with geometry
hyprctl clients -j | python3 -c "
import json, sys
for c in json.load(sys.stdin):
    print(f'{c[\"class\"]:30s} at={c[\"at\"]} size={c[\"size\"]} ws={c[\"workspace\"][\"id\"]}')
"

# Focus window by class
hyprctl dispatch focuswindow "class:firefox"

# Launch application (on current workspace)
hyprctl dispatch exec "/opt/QQ/qq --no-sandbox"

# Get cursor position (verify clicks)
hyprctl cursorpos  # Returns "X, Y"

# Window-relative → absolute coordinate conversion
# Window at (807, 48), target at window-relative (388, 328)
# Absolute: (807+388, 48+328) = (1195, 376)
```

### Fullscreen Workspace Pattern (Recommended for Complex GUI Tasks)

For better scanning accuracy and easier interaction, move target app to a dedicated workspace and maximize it:

```bash
# 1. Move target app to dedicated workspace
hyprctl dispatch movetoworkspace 3 "class:google-chrome"

# 2. Switch to that workspace
hyprctl dispatch workspace 3

# 3. Maximize the window (fullscreen)
hyprctl dispatch fullscreen 0
sleep 0.3

# 4. Now operate in fullscreen mode
# - Scanner detects more elements (111 vs 40-60 in windowed mode)
# - Coordinates are more precise (window coords = screen coords)
# - No offset calculation needed
waywarp-scanner scan 2>/dev/null > /tmp/scan.json
waywarp --move-to 800 500 --click left

# 5. When done, restore and return
hyprctl dispatch fullscreen 0  # Exit fullscreen
hyprctl dispatch workspace 1   # Return to original workspace
```

**Benefits of fullscreen workspace pattern:**
- Scanner detects 2-3x more elements (larger visible area)
- Coordinates are absolute (no window offset calculation)
- Click targets are larger and easier to hit
- Screenshots are cleaner for vision analysis

**Pitfall**: Some apps may not move to other workspaces cleanly. If `movetoworkspace` fails, try:
```bash
# Use special workspace instead
hyprctl dispatch movetoworkspace special:magic "class:app"
hyprctl dispatch togglespecialworkspace magic
```

---

## Known Pitfalls

### ⚠️ P1: waywarp v0.1.6 had RefCell panic regression
v0.1.6 panicked with "RefCell already borrowed" on all cursor commands (`--select`, `--move-to`, `--move-by`). Fixed in v0.1.7. If user reports this, they need to `cargo install waywarp` to update.

### ⚠️ P2: Scanner reads terminal/editor content
OCR captures everything visible on screen, including terminal output and code. The `filters.py` module applies heuristic noise filtering but may still include some code fragments.

**Mitigation**: Focus agent attention on elements with `type: "button"` or `type: "menu_item"` which are more reliable. Run `waywarp-scanner scan --no-serve` to test without daemon.

### ✅ FIXED: Multiprocessing cold-start overhead (#45/#46)
The original scanner used `multiprocessing.Process` with `fork`, which re-imported torch/easyocr in child processes (~3s overhead). Fixed in v0.2.0 by using `threading.Thread` which shares the cached Reader instance.

### ✅ FIXED: Scanner consistency regression (#42)
v0.1.6 had severe inconsistency (22, 3, 41 elements across runs). Fixed in v0.2.0 with auto-serve daemon — now returns 98, 98, 98 consistently.

---

## Agent Testing Checklist (waywarp v0.1.7 + scanner v0.2.0)

```bash
# 1. Clean JSON parsing
waywarp --list-hints --format json 2>/dev/null | python3 -c "import json,sys; json.load(sys.stdin)"

# 2. Hint selection + click
waywarp --select "aa" 2>/dev/null | grep -q "ok"

# 3. Absolute move + verify position
waywarp --move-to 800 500 2>/dev/null
hyprctl cursorpos 2>/dev/null  # Should show ~800, 500

# 4. Relative move + verify position
waywarp --move-to 500 500 2>/dev/null
sleep 0.2
waywarp --move-by 200 100 2>/dev/null
sleep 0.2
hyprctl cursorpos 2>/dev/null  # Should show ~700, 600

# 5. Out-of-bounds clamping
waywarp --move-to 9999 9999 2>&1 | grep -q "clamping"

# 6. Print coordinates
waywarp --select "aa" --print-coords 2>/dev/null | head -1  # "75 47"

# 7. Scanner with timing
waywarp-scanner scan --timing 2>&1 1>/dev/null  # Shows capture/inference/merge breakdown

# 8. Scanner consistency (run 3 times)
for i in 1 2 3; do
  waywarp-scanner scan 2>/dev/null | python3 -c "import json,sys;print(len(json.load(sys.stdin)['elements']))"
done

# 9. Scanner element types
waywarp-scanner scan 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
types = {}
for e in d['elements']:
    types[e['type']] = types.get(e['type'], 0) + 1
print(types)
"

# 10. Cold scan (--no-serve)
waywarp-scanner scan --no-serve --timing 2>&1 1>/dev/null
```

---

## Helper Script

A Python helper is included at `scripts/waywarp_helper.py` for structured Agent calls:
```bash
python3 ~/.hermes/skills/devops/waywarp/scripts/waywarp_helper.py --list
python3 ~/.hermes/skills/devops/waywarp/scripts/waywarp_helper.py --nearest 800 500
python3 ~/.hermes/skills/devops/waywarp/scripts/waywarp_helper.py --select "aa"
```

## Support Files

- `references/agent-cli-testing-guide.md` — Systematic test script, Agent integration patterns, issue tracker summary
- `references/testing-results-2026-06-02.md` — Detailed testing results from initial testing session
- `references/cli-testing-methodology.md` — Reusable CLI tool testing methodology for Agent automation
- `references/iterative-testing-workflow.md` — Iterative testing + issue lifecycle + Python optimization patterns
- `references/auto-serve-daemon-pattern.md` — Auto-serve daemon pattern for Python CLI tools with model caching
- `references/python-package-release-workflow.md` — Hotfix → PR → PyPI release workflow
- `references/browser-gui-automation.md` — Browser & Electron app automation patterns, link clicking pitfalls, Ctrl+L navigation
- `scripts/waywarp_helper.py` — Python helper for structured hint queries
