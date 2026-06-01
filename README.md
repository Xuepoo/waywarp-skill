# Waywarp Skill

A dedicated AI Agent Skill package for **Waywarp**, a high-performance, keyboard-driven mouse control tool for Wayland compositors (wlroots-based). 

This skill allows AI Agent systems (like Hermes, Claude Code, or other CLI agent frameworks) to dynamically locate coordinates on screens (including multi-monitor setups) and simulate pointer interactions like warp, clicks, scrolls, and drags.

## Installation

To equip your AI Agent with this skill, you can install it instantly using the `skills` utility CLI, or copy it manually:

### 1. Fast Installation via CLI (Recommended)
Add this skill directly to your Gemini / Antigravity agent CLI environment:
```bash
npx skills add https://github.com/Xuepoo/waywarp-skill
```

### 2. Manual Integration
Alternatively, copy the `SKILL.md` file directly to your local skills directory:
```bash
cp SKILL.md ~/.gemini/antigravity-cli/skills/waywarp/SKILL.md
```

### 2. Manual Integration
For any custom agent orchestrators, point your agent's system prompt reference to the instructions listed in [SKILL.md](./SKILL.md).

## Helper Scripts

A Python helper script `waywarp_helper.py` is included in the `scripts/` folder to facilitate structured programmatic calls:
- Parse `waywarp --list-hints --format json` outputs.
- Offer semantic/fuzzy labeling coordinate searches.
- Warp and trigger dynamic absolute mouse clicks.

For detailed usage, refer to the [scripts/README.md](./scripts/README.md).

## LICENSE
MIT License.
