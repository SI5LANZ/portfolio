#!/usr/bin/env python3
"""Rendert das Branding-PDF via pdf.js (Playwright) zu Kontaktboegen
oder einzelnen Seiten in hoher Aufloesung.

Usage:
  pdf_sheets.py sheets                 -> Kontaktboegen nach /tmp/pdfsheets
  pdf_sheets.py pages 12 45 100 ...    -> Einzelseiten (1400px) nach assets/projects
"""
import base64
import pathlib
import sys

from playwright.sync_api import sync_playwright

PDF = pathlib.Path.home() / "Downloads/Branding presentation compressed.pdf"
MODE = sys.argv[1] if len(sys.argv) > 1 else "sheets"
PAGES = [int(x) for x in sys.argv[2:]]

HTML = """<!doctype html><html><body><script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<script>
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
async function renderPage(pdf, n, width) {
  const page = await pdf.getPage(n);
  const vp1 = page.getViewport({scale: 1});
  const scale = width / vp1.width;
  const vp = page.getViewport({scale});
  const c = document.createElement('canvas');
  c.width = vp.width; c.height = vp.height;
  await page.render({canvasContext: c.getContext('2d'), viewport: vp}).promise;
  return c;
}
window.makeSheets = async function(b64, cols, rows, thumbW) {
  const data = Uint8Array.from(atob(b64), ch => ch.charCodeAt(0));
  const pdf = await pdfjsLib.getDocument({data}).promise;
  const n = pdf.numPages;
  const per = cols * rows;
  const out = [];
  const first = await renderPage(pdf, 1, thumbW);
  const thumbH = first.height;
  for (let s = 0; s < Math.ceil(n / per); s++) {
    const sheet = document.createElement('canvas');
    sheet.width = cols * thumbW; sheet.height = rows * (thumbH + 14);
    const ctx = sheet.getContext('2d');
    ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, sheet.width, sheet.height);
    ctx.fillStyle = '#c00'; ctx.font = '11px sans-serif';
    for (let i = 0; i < per; i++) {
      const p = s * per + i + 1;
      if (p > n) break;
      const c = await renderPage(pdf, p, thumbW);
      const x = (i % cols) * thumbW, y = Math.floor(i / cols) * (thumbH + 14);
      ctx.drawImage(c, x, y);
      ctx.fillText('p' + p, x + 3, y + thumbH + 11);
    }
    out.push(sheet.toDataURL('image/jpeg', 0.72));
  }
  return out;
};
window.makePages = async function(b64, pages, width) {
  const data = Uint8Array.from(atob(b64), ch => ch.charCodeAt(0));
  const pdf = await pdfjsLib.getDocument({data}).promise;
  const out = {};
  for (const p of pages) {
    const c = await renderPage(pdf, p, width);
    out[p] = c.toDataURL('image/jpeg', 0.82);
  }
  return out;
};
</script></body></html>"""

b64 = base64.b64encode(PDF.read_bytes()).decode()

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_content(HTML, wait_until="networkidle")
    if MODE == "sheets":
        out = pathlib.Path("/tmp/pdfsheets")
        out.mkdir(exist_ok=True)
        sheets = page.evaluate("([b]) => makeSheets(b, 6, 7, 190)", [b64])
        for i, d in enumerate(sheets):
            (out / f"sheet{i:02d}.jpg").write_bytes(base64.b64decode(d.split(",", 1)[1]))
        print(f"{len(sheets)} sheets -> {out}")
    else:
        out = pathlib.Path(__file__).resolve().parent.parent / "assets/projects"
        out.mkdir(parents=True, exist_ok=True)
        res = page.evaluate("([b, ps]) => makePages(b, ps, 1400)", [b64, PAGES])
        for p, d in res.items():
            (out / f"pdf-p{int(p):03d}.jpg").write_bytes(base64.b64decode(d.split(",", 1)[1]))
        print(f"{len(res)} pages -> {out}")
    browser.close()
