#!/usr/bin/env python3
"""Sammelt fertige 1:1-Statics aus den Tryout-Serienordnern,
erzeugt 760px-JPEGs fuer das Portfolio-Grid und schreibt manifest.json."""
import json
import pathlib
import struct
import subprocess

ARBEIT = pathlib.Path.home() / "Desktop/Arbeit"
TRYOUT = ARBEIT / "Tryout"
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets/ads"
OUT.mkdir(parents=True, exist_ok=True)

# folder -> (client, series-label, palette hint)
SOURCES = {
    "GMW_Geldzugriffs_Ads_1x1": ("GeldMehrWert", "Geldzugriffs-Report", "navy/gold"),
    "KH_KI-Bootcamp_Creatives": ("Katja Holzhey", "KI-Bootcamp", "warm"),
    "KH_KI-Bootcamp_Ads_1x1": ("Katja Holzhey", "KI-Bootcamp V1", "warm"),
    "KH_KI-Bootcamp_Ads_1x1_V2": ("Katja Holzhey", "KI-Bootcamp V2", "warm"),
    "KI-Bootcamp Creatives 1x1": ("Katja Holzhey", "KI-Bootcamp Creatives", "warm"),
    "YSO_Patanjali_Ads_1x1": ("Yogastudioonline", "Patanjali", "petrol/mint"),
    "YSO_SneakPeek_Statics_1x1": ("Yogastudioonline", "Sneak Peek", "petrol/mint"),
    "Yogastudioonline_Sommer_Ads_1x1": ("Yogastudioonline", "Sommer V1", "petrol/mint"),
    "Yogastudioonline_Sommer_Ads_1x1_V2": ("Yogastudioonline", "Sommer V2", "petrol/mint"),
    "Yogastudioonline_Sommer_Ads_1x1_V3": ("Yogastudioonline", "Sommer V3", "petrol/mint"),
    "Yogastudioonline_Sommer_Ads_1x1_V4_Stoerer": ("Yogastudioonline", "Sommer V4", "petrol/mint"),
    "apotheken-coach-ads": ("Apotheken Coach", "Apothekenreform 2026", "clean"),
    "UNEQ_AKF_Statics": ("UNEQ", "Anti-Krankentage-Formel", "dark"),
    "UNEQ_Anti-Krankentage-Formel_Creatives": ("UNEQ", "AKF Creatives", "dark"),
    "FZE_Umsatzreport_Ads_1x1": ("Flug zum Erfolg", "Umsatz-Report V1", "blue"),
    "FZE_Umsatzreport_Ads_1x1_V2_Typo": ("Flug zum Erfolg", "Umsatz-Report V2", "blue"),
    "PLK_Umsatzreport_Statics_1x1": ("PLK", "Umsatz-Report Statics", "blue"),
    "PLK_Umsatzreport_Creative_1x1": ("PLK", "Umsatz-Report Creatives", "blue"),
    "PLK_Team_Collage": ("PLK", "Team Collage", "blue"),
    "DK_ComebackDays_Ads_1x1": ("Danny Kroll", "Comeback Days", "gold/dark"),
    "108ideen-creatives": ("108ideen", "Creatives", "clean"),
}


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
n_skipped = 0
for folder, (client, series, palette) in SOURCES.items():
    src = TRYOUT / folder
    if not src.is_dir():
        print(f"!! missing {folder}")
        continue
    files = sorted(p for p in src.rglob("*")
                   if p.suffix.lower() in (".png", ".jpg", ".jpeg"))
    for p in files:
        dims = png_size(p) if p.suffix.lower() == ".png" else jpg_size(p)
        if not dims:
            n_skipped += 1
            continue
        w, h = dims
        if w < 1000 or h < 1000 or abs(w - h) / max(w, h) > 0.02:
            n_skipped += 1
            continue
        slug = f"{folder}__{p.stem}".replace(" ", "_").lower()
        slug = "".join(c if c.isalnum() or c in "-_" else "-" for c in slug)
        dest = OUT / f"{slug}.jpg"
        if not dest.exists():
            subprocess.run(
                ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "78",
                 "-Z", "760", str(p), "--out", str(dest)],
                check=True, capture_output=True)
        manifest.append({
            "file": f"assets/ads/{dest.name}",
            "client": client,
            "series": series,
            "palette": palette,
            "name": p.stem,
        })
    print(f"{folder}: done")

with open(OUT.parent.parent / "manifest.json", "w") as f:
    json.dump(manifest, f, ensure_ascii=False)
print(f"total: {len(manifest)} ads, skipped {n_skipped} non-1:1/small files")
