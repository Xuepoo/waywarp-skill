# Waywarp Agent Scripts Helper

This folder contains dynamic script utilities assisting AI agents in interacting with **Waywarp**.

## Files

- `waywarp_helper.py`: A Python CLI script serving high-speed query tasks.

## Usage Instructions

Make sure the script is marked executable:
```bash
chmod +x waywarp_helper.py
```

### 1. List Available Screen Grid Hints
Retrieves coordinates and labels of screen cells in standard format:
```bash
./waywarp_helper.py --list
```

### 2. Locate Nearest Hint Cell
If you have a raw pixel target (e.g. from an OCR output or image target bounding box) and want to map it to the closest grid hint label:
```bash
./waywarp_helper.py --nearest 1024 768
```
**Sample JSON Output:**
```json
{
  "label": "sab",
  "x": 1018,
  "y": 765,
  "screen": 1
}
```
You can optionally filter coordinates by screen:
```bash
./waywarp_helper.py --nearest 800 600 --screen 0
```

### 3. Programmatically click a matched label
Invokes cursor warping and clicks:
```bash
./waywarp_helper.py --select "sab"
```
