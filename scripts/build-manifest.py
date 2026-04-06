#!/usr/bin/env python3
"""Rebuild public/puzzles/manifest.json from all puzzle JSON files."""

import json
import os
from pathlib import Path

PUZZLES_DIR = Path(__file__).parent.parent / "public" / "puzzles"

ALL_CATEGORIES = [
    {"id": "nature", "label": {"hu": "Természet"}, "icon": "🌿"},
    {"id": "history", "label": {"hu": "Történelem"}, "icon": "🏛️"},
    {"id": "world-history", "label": {"hu": "Világtörténelem"}, "icon": "🌍"},
    {"id": "israel-history", "label": {"hu": "Izrael története"}, "icon": "✡️"},
    {"id": "food", "label": {"hu": "Ételek és italok"}, "icon": "🍲"},
    {"id": "geography", "label": {"hu": "Földrajz"}, "icon": "🗺️"},
    {"id": "culture", "label": {"hu": "Kultúra"}, "icon": "🎭"},
    {"id": "everyday", "label": {"hu": "Hétköznapi élet"}, "icon": "🏠"},
    {"id": "science", "label": {"hu": "Tudomány"}, "icon": "🔬"},
]

def main():
    puzzles = []
    seen_categories = set()

    # Find all JSON files in subdirectories, excluding manifest.json itself
    json_files = sorted(
        p for p in PUZZLES_DIR.rglob("*.json")
        if p.name != "manifest.json"
    )

    print(f"Found {len(json_files)} puzzle files")

    for json_path in json_files:
        rel_path = json_path.relative_to(PUZZLES_DIR)
        try:
            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"ERROR reading {rel_path}: {e}")
            continue

        puzzle_id = data.get("id")
        title = data.get("title")
        category = data.get("category")
        difficulty = data.get("difficulty")
        grid_size = data.get("gridSize")

        if not all([puzzle_id, title, category, difficulty, grid_size]):
            print(f"WARNING: missing fields in {rel_path} — skipping")
            continue

        puzzles.append({
            "id": puzzle_id,
            "file": str(rel_path).replace("\\", "/"),  # normalize on Windows too
            "title": title,
            "category": category,
            "difficulty": difficulty,
            "gridSize": grid_size,
        })
        seen_categories.add(category)

    # Only include categories that have at least one puzzle, preserving original order
    categories = [c for c in ALL_CATEGORIES if c["id"] in seen_categories]

    manifest = {
        "puzzles": puzzles,
        "categories": categories,
    }

    out_path = PUZZLES_DIR / "manifest.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(puzzles)} puzzles across {len(categories)} categories to {out_path}")
    print(f"Categories present: {sorted(seen_categories)}")


if __name__ == "__main__":
    main()
