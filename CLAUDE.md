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
- GitHub Pages braucht die `.nojekyll`-Datei im Root. Nie löschen. Der Legacy-Builder meldet gelegentlich „Page build failed“ ohne Grund
  (06.11.: drei Fehlschläge in Folge, danach lief derselbe Commit durch) → einfach neu anstoßen:
  `gh api -X POST repos/SI5LANZ/portfolio/pages/builds`. Ein Actions-Workflow-Deploy wäre robuster, aber der `gh`-Token hat
  keinen `workflow`-Scope; dafür müsste Julian einmal `gh auth refresh -h github.com -s workflow` im Terminal ausführen.
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

### Sections in Reihenfolge (seit 2026-11-06: Creative Direction vorn, Paid Ads hinten)
hero (Typo + laufender Leopard) → marquee → **worlds** (Yantra-Accordion + Mosaik, Up & Down mit Tilt + Accordion) → **endo** (zwei Centerpieces: Clubroom-Teaser-Video + Cocktail-Invite, Accordion aus 6 Metall-Finals, Trio) → **motion** (4 aktuelle Reels: APO Workshop/Report, UNEQ Trailer/Match-Cut) → **the ai part, honestly** (Prozess: 4 Panels, KEIN Code/Terminal mehr – Panel 03 „scale the series" = Fleet-Grid aus 24 Flipper-Thumbs) → **a vs. b** (Compare, Flipper) → **paid ads, the proof** (kompakte Wall, 360 Desktop / 120 mobil) → **funnels** → **off the clock** (nur noch paper works) → **about** → footer

### Endo-Quellen
`~/Desktop/Arbeit/endo/Art Direction 1.pdf` (EINE große Board-Seite → `assets/endo/board.jpg` 2600px, Crops `board-*.jpg` per sips), `~/Desktop/Arbeit/UNEQ/Ordner/endo/` (Insta-Posts, Slides, Backgrounds, Logos), `~/Downloads/endo – Clubroom animation 3.mp4` (→ assets/motion/endo-clubroom.mp4). Instagram: @weare.endo. Figma-Sandbox `u4bnooPXCPldbkpabV8UHG` nur erreichbar, wenn in der Figma-App „Enable Dev Mode MCP Server" aktiv ist.

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
- **Keine Vibe-Coding-Indizien:** keine Fake-Terminals, keine Code-Blöcke, keine `<pre>`-Snippets als Deko.
  Claude darf im Text als Werkzeug vorkommen (Prozess-Intro, Motion-Lede, Toolbox), aber nie als Optik.
- Positionierung: **Creative Direction / Brand Worlds zuerst**, Paid Ads sind der Beleg weiter unten.
- **Keine quippigen Riesen-Headlines an Projekten** („a night in budapest", „it also moves" …) – Julian findet die cringe.
  Projekte bekommen nur die Speisekarten-Zeile (`.project-head`: Titel ···· Meta) + beschreibenden Text; die Elemente erzählen.
  Große `.sec-giant`-Zeilen nur noch im Hero, bei „a vs. b" und im About.
- **Keine Brand-Asset-Boards** (Farbchips, Type-Specimen, Logo-Konstruktion) in Projekten – wirkt zusammengewürfelt. Lieber wenige, ruhige Finals, editorial.
- Yantra ist KEIN Accordion mehr (16:9-Spreads in Hochkant-Streifen = Text abgeschnitten, zusammengewürfelt), sondern `.ystack`: Spreads ganz oder auf ihren Fotoanteil gecroppt (`assets/projects/y-*.jpg` per sips aus pdf-pNNN), Rhythmus Vollbreite / Zweierreihe. Nie durch Text croppen; Deck-Seiten mit Titel+Fließtext (p004, p009, p017-Text, p018) nicht zeigen.
- Endo: keine Dubletten (slide-1≈post-1, post-4≈slide-6, slide-5≈post-3) – Accordion zeigt 6 unterschiedliche Motive, kein Trio darunter.
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

- Videos komprimieren geht lokal nicht (kein ffmpeg; avconvert vergrößert Dateien). Deshalb nur Finals ≤ ~17 MB
  einbauen; der 121-MB-Tim-VSL (`Ami/Video-Ads/TimVSL-Cinematic 2026-11`) braucht erst einen HandBrake-Export (~5 MB).
- Weitere Motion-Kandidaten (zu groß im Original): YIF Erfolgspyramide 01 (30 MB), VTR MatchCut 01 (19 MB), UNEQ 108 Ideen Explainer (97 MB).
- Eigene Domain (z. B. julianlanz.design): Domain kaufen, dann CNAME in Pages + `og:url` anpassen.
- Weitere Statics: Kundenordner → `python3 tools/curate_own.py`, dann Thumbs nachziehen
  (`sips -s format jpeg -s formatOptions 68 -Z 220 <src> --out assets/thumbs/<name>`), Manifest bleibt dedupliziert.
