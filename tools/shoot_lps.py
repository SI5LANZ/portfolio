#!/usr/bin/env python3
"""Full-page-Screenshots der Live-Landingpages fuer die Funnels-Section."""
import pathlib
import subprocess

from playwright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets/funnels"
OUT.mkdir(parents=True, exist_ok=True)

PAGES = {
    "comeback-days": "https://danny-kroll-8bjs.lpcontent.net/comeback-days",
    "umsatz-report": "https://flug-zum-erfolg-fqmc.lpcontent.net/umsatz-report",
    "abundance-high": "https://corinna-kehl-opdn.lpcontent.net/abundance-high",
    "kgc-workshop": "https://up-lift-iyj8.lpcontent.net/kgc-workshop",
}

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    for name, url in PAGES.items():
        page.goto(url, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(1500)
        raw = OUT / f"{name}-raw.png"
        page.screenshot(path=str(raw), full_page=True)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "72",
                        "--resampleWidth", "640", str(raw), "--out", str(OUT / f"{name}.jpg")],
                       check=True, capture_output=True)
        raw.unlink()
        print(name, "ok")
    browser.close()
