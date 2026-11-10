#!/usr/bin/env python3
"""Validate the proposed Landing Camp ASCII navigation plan (not GBA collision)."""
from collections import deque
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/LANDING_CAMP_GRID_48x40_V03.md"
text = SOURCE.read_text(encoding="utf-8")
match = re.search(r"```text\n(.*?)\n```", text, re.S)
if not match:
    raise SystemExit("Missing grid code block")
lines = match.group(1).splitlines()
if len(lines) != 40:
    raise SystemExit(f"Expected 40 rows, got {len(lines)}")
grid = []
allowed = set(".=D+AF12345MLHSQRTC^~")
for y, line in enumerate(lines):
    if not line.startswith(f"{y:02d} "):
        raise SystemExit(f"Invalid row number at {y}")
    row = line[3:]
    if len(row) != 48 or set(row) - allowed:
        raise SystemExit(f"Invalid width or glyph in row {y}: {len(row)}")
    grid.append(row)
walkable = set(".=D+AF12345")
starts = [(x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == "A"]
if len(starts) != 1:
    raise SystemExit(f"Expected one arrival cell, found {len(starts)}")
start = starts[0]
queue = deque([start])
visited = {start}
while queue:
    x, y = queue.popleft()
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < 48 and 0 <= ny < 40 and grid[ny][nx] in walkable and (nx, ny) not in visited:
            visited.add((nx, ny))
            queue.append((nx, ny))
targets = {
    "medical": (18, 17), "lab": (18, 11), "HQ": (28, 10),
    "supply": (34, 14), "quarters": (38, 23),
    "forest": (23, 39), "coast": (44, 29), "cave": (44, 10),
    "ruins": (31, 4), "north trail": (23, 0),
}
for name, (x, y) in targets.items():
    if (x, y) not in visited:
        raise SystemExit(f"Unreachable: {name} at ({x},{y})")
    expected = "+" if name in {"medical", "lab", "HQ", "supply", "quarters"} else {
        "forest": "1", "coast": "2", "cave": "3", "ruins": "4", "north trail": "5"
    }[name]
    if grid[y][x] != expected:
        raise SystemExit(f"Wrong landmark at {name} ({x},{y}): {grid[y][x]}")
print(f"Landing Camp grid validated: 48x40, {len(targets)} reachable landmarks, {len(visited)} connected cells")

# Story-gated optional exits must not prevent reaching core services or Route 1.
# Removing a gate cell models a closed entrance; it does not model GBA scripts.
gated = {(44, 10), (31, 4), (23, 0)}
queue = deque([start])
without_gates = {start}
while queue:
    x, y = queue.popleft()
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nx, ny = x + dx, y + dy
        pos = (nx, ny)
        if (0 <= nx < 48 and 0 <= ny < 40
                and pos not in gated and grid[ny][nx] in walkable
                and pos not in without_gates):
            without_gates.add(pos)
            queue.append(pos)
required_open = ("medical", "lab", "HQ", "supply", "quarters", "forest", "coast")
for name in required_open:
    if targets[name] not in without_gates:
        raise SystemExit(f"Story gate blocks essential route: {name}")
print(f"Closed-gate check passed: {len(required_open)} essential destinations accessible")
