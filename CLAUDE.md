# Julian Lanz — Portfolio-Site

Persönliche Portfolio-Website von Julian Lanz (Creative Designer, automadeit GmbH).
Vanilla HTML/CSS/JS, **kein Build-Step, kein Node**. Live auf GitHub Pages.

- **Live:** https://si5lanz.github.io/portfolio/
- **Repo:** https://github.com/SI5LANZ/portfolio (public, Account `SI5LANZ`, `gh` CLI ist autorisiert)
- **Lokal:** `~/Desktop/Arbeit/Portfolio` (dieser Ordner)
- **Sprache der Seite:** Englisch, komplett lowercase. Kommunikation mit Julian: Deutsch.

## Arbeiten & deployen

```bash
# lokal ansehen (kein npm nötig)
python3 -m http.server 4173        # dann http://localhost:4173
```

```bash
# deployen = einfach pushen, Pages baut in ~1 Minute
git add -A && git commit -m "…" && git push origin main
gh api repos/SI5LANZ/portfolio/pages/builds/latest --jq .status   # "built" = fertig
```

- **Cache-Busting:** nach jeder CSS/JS-Änderung die `?v=N` an `css/site.css?v=…` und
  `js/site.js?v=…` in `index.html` hochzählen, sonst sieht Julian alte Versionen (sein Handy cached hart).
- Nach Änderungen immer **Desktop (≥901px) und Mobil (375px)** prüfen. Die meisten Bugs der
  Vergangenheit waren Mobil-Bugs (Overflow, zerquetschte Galerien, iOS-Video-Eigenheiten).

## Struktur

```
index.html              eine Seite, alle Sections (Reihenfolge unten)
css/site.css            komplettes Styling, Mobile-Blöcke am Ende (@media max-width 720/900)
js/site.js              Wall, Filter, Shuffle, Lightbox, Leopard-Canvas, Lazy-Videos, Accordion, Tilt, Karte
manifest-work.json      Liste der Wall-Statics (client, file, name) – 1.961 unique Einträge
manifest.json           Pipeline-Renders für die Prozess-Section (assets/ads/)
assets/work/            Originale der eigenen Statics (760px, ~125KB) – nur Lightbox
assets/thumbs/          220px-Thumbs derselben Dateien – Wall-Grid + Cursor-Trail
assets/ads/             Claude-gerenderte Tryout-Serien (Prozess-Section)
assets/motion/          leopard-walk.mp4 (Hero), ami-reel, uneq-ad3, funnel-reel (+ Poster-JPGs)
assets/projects/        Yantra-Branding-PDF-Seiten (pdf-pNNN.jpg)
assets/updown/          Up & Down Theater-Kampagne (Mockups)
assets/personal/        Instagram-Poster (ig-XX.jpg), lamp.jpg
assets/funnels/         Full-Page-Screenshots der Live-Landingpages
assets/tools/           figma.svg, claude.svg (Toolbox)
assets/portrait.jpg     Porträt (About), og-image.jpg, favicon-*.png
tools/curate_own.py     sammelt eigene Statics aus ~/Desktop/Arbeit/<Kunde>/ → assets/work + manifest-work.json
tools/pdf_sheets.py     rendert PDF-Seiten via pdf.js in Playwright (kein poppler auf dem Mac)
tools/shoot_lps.py      Playwright-Full-Page-Shots von Landingpages (mit Scroll-Durchlauf für Reveal-Animationen)
```

### Sections in Reihenfolge
hero (Typo + laufender Leopard) → marquee (schräges Indigo-Band) → **the wall** (Statics-Grid, Filter, Shuffle, Lightbox) → **the ai part, honestly** (Prozess, desktop sideways-scroll, mobil vertikal) → **a vs. b** (Compare-Slider, Flipper-Paar) → **motion** (3 Reels) → **funnels** (4 LP-Shots, hover scrollt) → **off the clock** (Yantra-Accordion + Mosaik, Up & Down mit Tilt + Accordion, paper works) → **about** (Headline, Foto, „julian", Texte, Toolbox, Seekarten-Route) → footer (say hi, instagram, linkedin)

## Designregeln (Julians Geschmack – bitte einhalten)

- **Palette:** Papier `#f9f7ee` (var(--bg)), Indigo `#2226c9` (var(--ink)). Nur diese zwei Welten.
  Indigo-Vollflächen nur für Marquee, Prozess, Motion. Keine automadeit-Farben (Neongelb).
- **Typo:** Neue-Haas-Grotesk-Stack (`"Neue Haas Grotesk Display Pro", "Helvetica Neue", "Inter Tight"`)
  + EB Garamond *italic nur als Akzentwort in Headlines*, Garamond-Kapitälchen für Captions/Filter.
  **Alles lowercase.** Space Mono NUR in echten Code-Blöcken. Kein Caveat/Script mehr.
- **Keine Outline-Typo**, keine Rahmen/Karten/Boxen um Elemente (wirkt für Julian veraltet).
  Ausnahme: die feinen Trattoria-Doppellinien (.orn-Divider, Hero-Rule, Karte).
- **Keine ↗-Pfeile / Link-Icons / Emojis** (U+2197 rendert auf iOS als Emoji).
- **Nav nicht sticky** (position:absolute, scrollt weg).
- **Porträt natürlich lassen** – keine Filter, Duotone, Masken, Overlays, Captions darüber.
- **Wall:** kein Hover-Zoom, Klick öffnet Lightbox. Flipper = Lieblingsserie → erste Filter-Pill,
  alle Flipper-Statics immer im Sample. Mobil nur 150 Tiles (Scrollweg kurz halten).
- Prozess-Beispiele aus GMW/Flipper, **nicht** die Yoga-Serien (findet Julian nicht schön).
- Textur ja (Papierkorn, Büttenpapier), aber nie als Rahmen-Effekt.
- Copy: kein „for coaches" – „for personal brands across DACH".

## Technische Fallen (gelernt, nicht nochmal reinlaufen)

- **iOS + Video:** `mix-blend-mode` wirkt weder auf `<video>` noch auf Overlays darüber. Der Leopard
  läuft deshalb über `<canvas class="leo-canvas">`, das jeden Frame selbst komponiert
  (drawImage → `lighter`-Pass ×1.3 brennt das Papier weiß → Desktop zusätzlich `multiply` mit var(--bg)).
  Das Quellvideo muss in voller Größe hinter dem Canvas liegen (iOS startet „unsichtbare" Videos nicht).
  Mobil ist der weiße Block gewollt: zentriert, Headline schneidet ihn an.
- Alle Videos: `muted playsinline autoplay loop` + `data-autoplay` (IO pausiert offscreen).
  Motion-Reels haben `data-src`, ein IntersectionObserver (700px Vorlauf) setzt `src` erst beim Näherkommen.
- `html, body { overflow-x: clip }` (nicht `hidden` – das bricht sticky und erlaubt Quer-Wischen).
- Sideways-Prozess (`animation-timeline: view()`) nur ≥901px; mobil vertikaler Stack.
- Accordions mobil = natürlicher Bildstapel (`height:auto`, `img position:static`), sonst zerquetscht.
- Overlap-Checks in h1/span: `getBoundingClientRect` ist blockbreit → `Range.selectNodeContents` nutzen.
- Browser-Pane in der Desktop-App: bei verstecktem Pane ist `document.hidden=true`, IO feuert nicht,
  Screenshots nach programmatischem Scroll sind stale → Sections per `display:none` ausblenden und bei Scroll 0 shooten.
- Kein ffmpeg/poppler/Node auf dem Mac. Bilder: `sips`. PDFs: `tools/pdf_sheets.py`. Videos komprimieren: HandBrake/Premiere (manuell).
- Drive-Ordner von Julians privatem Gmail sieht der Connector nicht → Datei-IDs aus der Drive-UI (Chrome),
  Download über `https://drive.google.com/uc?export=download&id=…` (nur bei link-shared).

## Offen / Ideen

- `assets/motion/ami-reel.mp4` ist 19,5 MB → auf ~3–4 MB (720p, 9:16) exportieren und austauschen.
- Eigene Domain (z. B. julianlanz.design): Domain kaufen, dann CNAME in Pages + `og:url` anpassen.
- Weitere Statics: Kundenordner → `python3 tools/curate_own.py`, dann Thumbs nachziehen
  (`sips -s format jpeg -s formatOptions 68 -Z 220 <src> --out assets/thumbs/<name>`), Manifest bleibt dedupliziert.
