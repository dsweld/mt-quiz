"""Generate data.json for static hosting (e.g. GitHub Pages)."""

import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "washington_top100_union_bulger_400p_summitpost.csv"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

mountains = []
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["mountain_name"]
        image_dir = row["image_dir"]
        dir_path = BASE_DIR / image_dir

        images = []
        if dir_path.is_dir():
            for entry in sorted(dir_path.iterdir()):
                if entry.is_file() and entry.suffix.lower() in IMAGE_EXTS:
                    images.append(f"{image_dir}/{entry.name}")

        if not images:
            continue

        mountains.append({
            "name": name,
            "elevation_ft": int(row["elevation_ft"]) if row["elevation_ft"] else None,
            "prominence_ft": int(row["prominence_ft"]) if row["prominence_ft"] else None,
            "lat": float(row["latitude"]) if row.get("latitude") else None,
            "lon": float(row["longitude"]) if row.get("longitude") else None,
            "images": images,
        })

out = BASE_DIR / "data.json"
out.write_text(json.dumps(mountains, indent=2), encoding="utf-8")
print(f"Wrote {len(mountains)} mountains to {out}")
