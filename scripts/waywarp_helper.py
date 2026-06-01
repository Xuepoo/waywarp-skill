#!/usr/bin/env python3
"""
Waywarp Agent Helper Script
Provides structured helper functions to find nearest hints, query coordinates,
and execute actions using the waywarp CLI.
"""

import argparse
import json
import math
import subprocess
import sys


def run_waywarp(args):
    """Execute waywarp command and return stdout/stderr"""
    try:
        result = subprocess.run(
            ["waywarp"] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing waywarp: {e.stderr}", file=sys.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(
            "Error: 'waywarp' binary not found in PATH. Please install it first.",
            file=sys.stderr,
        )
        sys.exit(127)


def get_hints():
    """Query list of active hints from waywarp as a list of dicts"""
    raw_json = run_waywarp(["--list-hints", "--format", "json"])
    try:
        data = json.loads(raw_json)
        return data.get("hints", [])
    except json.JSONDecodeError:
        print("Error parsing waywarp JSON outputs.", file=sys.stderr)
        sys.exit(1)


def find_nearest_hint(x, y, screen=None):
    """Find the hint label closest to the given coordinates (x, y)"""
    hints = get_hints()
    if not hints:
        print("No active hints retrieved from screen grid.", file=sys.stderr)
        return None

    min_dist = float("inf")
    nearest = None

    for hint in hints:
        if screen is not None and hint.get("screen") != screen:
            continue

        hx, hy = hint.get("x", 0), hint.get("y", 0)
        dist = math.sqrt((x - hx) ** 2 + (y - hy) ** 2)
        if dist < min_dist:
            min_dist = dist
            nearest = hint

    return nearest


def main():
    parser = argparse.ArgumentParser(
        description="Helper utility for Waywarp Agent Skill integration."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--list", action="store_true", help="List all hints with coordinates as JSON"
    )
    group.add_argument(
        "--nearest",
        nargs=2,
        type=int,
        metavar=("X", "Y"),
        help="Find the nearest hint label for the target coordinates X Y",
    )
    group.add_argument(
        "--select", metavar="LABEL", help="Programmatically select and click a label"
    )

    parser.add_argument(
        "--screen", type=int, help="Filter search to specific screen index"
    )
    args = parser.add_args = parser.parse_args()

    if args.list:
        hints = get_hints()
        print(json.dumps({"hints": hints}, indent=2))

    elif args.nearest:
        tx, ty = args.nearest
        nearest = find_nearest_hint(tx, ty, screen=args.screen)
        if nearest:
            print(json.dumps(nearest, indent=2))
        else:
            print("No matching hint found.", file=sys.stderr)
            sys.exit(1)

    elif args.select:
        print(f"Selecting hint label: {args.select}")
        run_waywarp(["--select", args.select])
        print("Successfully warped and clicked.")


if __name__ == "__main__":
    main()
