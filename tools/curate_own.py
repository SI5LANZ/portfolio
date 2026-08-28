#!/usr/bin/env python3
"""Sammelt Julians eigene Statics aus den Kundenordnern in ~/Desktop/Arbeit,
filtert Asset-Dateien raus und schreibt manifest-work.json."""
import json
import pathlib
import struct
import subprocess

ARBEIT = pathlib.Path.home() / "Desktop/Arbeit"
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets/work"
OUT.mkdir(parents=True, exist_ok=True)

SKIP_DIRS = {"Tryout", "Inspo", "Sales presi", "TIM"}
SKIP_NAME = ("illustration", "illusration", "cutout", "icon", "logo", "testimonial",
             "ai image", "profile", "asset", "mockup", "standbild", "freigestellt",
             "hero", "button", "phone", "magnific_", "webinar grafik", "collge",
             "collage", "screenshot", "cover", "jeske", "waage", "patienten",
             "kreisluf", "laptop", "expnd", "remix", "selstbewusstsein", "background",
             "hintergrund", "visual-key", "prompt", "grafik", "bild ")
SKIP_PATH = ("assets", "material", "rohmaterial", "fotos", "bilder", "cutouts")


def png_size(p):
    with open(p, "rb") as f:
        head = f.read(26)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def jpg_size(p):
    with open(p, "rb") as f:
        data = f.read(65536)
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        seglen = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + seglen
    return None


manifest = []
for client_dir in sorted(ARBEIT.iterdir()):
    if not client_dir.is_dir() or client_dir.name in SKIP_DIRS:
        continue
    client = client_dir.name.strip()
    for p in sorted(client_dir.rglob("*")):
        if p.suffix.lower() not in (".png", ".jpg", ".jpeg"):
            continue
        rel_parts = [x.lower() for x in p.relative_to(client_dir).parts[:-1]]
        if any(part in SKIP_PATH for part in rel_parts):
            continue
        name_l = p.stem.lower()
        if any(k in name_l for k in SKIP_NAME):
            continue
        dims = png_size(p) if p.suffix.lower() == ".png" else jpg_size(p)
        if not dims:
            continue
        w, h = dims
        ratio = w / h
        if w < 950 or h < 950 or not (0.78 <= ratio <= 1.05):
            continue
        slug = f"{client}__{p.stem}".replace(" ", "_").lower()
        slug = "".join(c if c.isalnum() or c in "-_" else "-" for c in slug)
        dest = OUT / f"{slug}.jpg"
        if not dest.exists():
            r = subprocess.run(
                ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "78",
                 "-Z", "760", str(p), "--out", str(dest)],
                capture_output=True)
            if r.returncode != 0:
                continue
        manifest.append({
            "file": f"assets/work/{dest.name}",
            "client": client,
            "name": p.stem,
        })

with open(OUT.parent.parent / "manifest-work.json", "w") as f:
    json.dump(manifest, f, ensure_ascii=False)

from collections import Counter
print(f"total: {len(manifest)}")
print(Counter(x["client"] for x in manifest).most_common())
