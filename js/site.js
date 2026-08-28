/* Julian Lanz portfolio */
(async function () {
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  // phones get a much shorter wall; desktop keeps the full flood
  const SAMPLE = matchMedia("(max-width: 720px)").matches ? 150 : 600;
  const PILLS = 10;        // client filters shown

  /* ---------- hero entrance stagger ---------- */
  document.querySelectorAll("[data-w]").forEach((w, i) => w.style.setProperty("--i", i));
  requestAnimationFrame(() => document.body.classList.add("loaded"));

  /* ---------- load manifests ---------- */
  let work = [], pipeline = [];
  try {
    [work, pipeline] = await Promise.all([
      fetch("manifest-work.json").then((r) => r.json()),
      fetch("manifest.json").then((r) => r.json()),
    ]);
  } catch (e) {
    console.error("manifest missing", e);
    return;
  }

  const displayName = (c) => c.charAt(0).toUpperCase() + c.slice(1);
  const shuffled = (arr) => [...arr].sort(() => Math.random() - 0.5);

  /* ---------- the wall (Julian's own statics, sampled) ---------- */
  const wall = document.getElementById("wallGrid");
  const countEl = document.querySelector("[data-count]");
  const totalEl = document.querySelector("[data-total]");
  totalEl.textContent = work.length.toLocaleString("en-US");

  const byCount = {};
  work.forEach((a) => (byCount[a.client] = (byCount[a.client] || 0) + 1));
  // Flipper is the favourite: pinned as the first client tab
  const topClients = [
    "Flipper",
    ...Object.keys(byCount)
      .filter((c) => c !== "Flipper")
      .sort((a, b) => byCount[b] - byCount[a]),
  ].slice(0, PILLS);

  let activeFilter = "all";

  function renderWall() {
    // in "all": every Flipper static is guaranteed in, the rest is sampled
    const flipper = work.filter((a) => a.client === "Flipper");
    const rest = work.filter((a) => a.client !== "Flipper");
    const pool = activeFilter === "all"
      ? shuffled([...flipper, ...shuffled(rest).slice(0, Math.max(0, SAMPLE - flipper.length))])
      : shuffled(work.filter((a) => a.client === activeFilter));
    wall.dataset.pool = JSON.stringify(pool.map((a) => work.indexOf(a)));
    const frag = document.createDocumentFragment();
    pool.forEach((a) => {
      const b = document.createElement("button");
      b.className = "tile";
      b.type = "button";
      b.dataset.index = work.indexOf(a);
      b.setAttribute("aria-label", `${displayName(a.client)}: ${a.name}`);
      b.innerHTML = `<img src="${a.file}" alt="Ad for ${displayName(a.client)}" loading="lazy" decoding="async">`;
      frag.appendChild(b);
    });
    wall.replaceChildren(frag);
    countEl.textContent = pool.length.toLocaleString("en-US");
    if (!reduceMotion) {
      // pixel effect: some tiles start "off" (cream squares in the grid)
      wall.querySelectorAll(".tile").forEach((t) => {
        if (Math.random() < 0.24) t.classList.add("off");
      });
    }
  }
  renderWall();

  /* pixel patterns shift while the wall moves through the viewport */
  if (!reduceMotion) {
    let lastShift = 0;
    const pixelObs = new IntersectionObserver(
      () => {
        const now = performance.now();
        if (now - lastShift < 350) return;
        lastShift = now;
        const tiles = wall.querySelectorAll(".tile:not(.hidden)");
        const n = Math.max(6, Math.floor(tiles.length * 0.05));
        for (let k = 0; k < n; k++) {
          const t = tiles[Math.floor(Math.random() * tiles.length)];
          // biased toggle so the wall settles around ~25% gaps instead of drifting to 50%
          if (t.classList.contains("off")) t.classList.remove("off");
          else if (Math.random() < 0.35) t.classList.add("off");
        }
      },
      { threshold: Array.from({ length: 21 }, (_, i) => i / 20) }
    );
    pixelObs.observe(wall);
  }

  // keep hover zoom inside the viewport: set transform-origin per tile position
  wall.addEventListener("pointerover", (e) => {
    const tile = e.target.closest(".tile");
    if (!tile) return;
    const r = tile.getBoundingClientRect();
    const x = r.left < 140 ? "left" : window.innerWidth - r.right < 140 ? "right" : "center";
    const y = r.top < 200 ? "top" : window.innerHeight - r.bottom < 160 ? "bottom" : "center";
    tile.querySelector("img").style.transformOrigin = `${x} ${y}`;
  });

  /* ---------- filters ---------- */
  const filterWrap = document.querySelector(".wall-filters");
  const mkPill = (label, value) => {
    const p = document.createElement("button");
    p.className = "fpill";
    p.type = "button";
    p.textContent = label;
    p.dataset.value = value;
    p.setAttribute("aria-pressed", value === "all" ? "true" : "false");
    return p;
  };
  filterWrap.appendChild(mkPill("All", "all"));
  topClients.forEach((c) => filterWrap.appendChild(mkPill(displayName(c), c)));

  filterWrap.addEventListener("click", (e) => {
    const pill = e.target.closest(".fpill");
    if (!pill) return;
    activeFilter = pill.dataset.value;
    filterWrap.querySelectorAll(".fpill").forEach((p) =>
      p.setAttribute("aria-pressed", p === pill ? "true" : "false"));
    renderWall();
  });

  /* ---------- shuffle: resample + FLIP on survivors ---------- */
  document.getElementById("shuffleBtn").addEventListener("click", () => {
    if (reduceMotion || activeFilter !== "all") {
      renderWall();
      return;
    }
    const tiles = [...wall.children];
    const first = new Map(tiles.map((t) => [t, t.getBoundingClientRect()]));
    tiles.sort(() => Math.random() - 0.5).forEach((t) => wall.appendChild(t));
    tiles.forEach((t) => {
      const a = first.get(t);
      const b = t.getBoundingClientRect();
      const dx = a.left - b.left;
      const dy = a.top - b.top;
      if (!dx && !dy) return;
      t.animate(
        [{ transform: `translate(${dx}px, ${dy}px)` }, { transform: "none" }],
        { duration: 550, easing: "cubic-bezier(0.16, 1, 0.3, 1)" }
      );
    });
  });

  /* ---------- lightbox ---------- */
  const lb = document.getElementById("lightbox");
  const lbImg = lb.querySelector(".lb-img");
  const lbCap = lb.querySelector(".lb-caption");
  let lbList = [];
  let lbIdx = 0;

  function lbShow(idx) {
    lbIdx = (idx + lbList.length) % lbList.length;
    const a = work[lbList[lbIdx]];
    lbImg.src = a.file;
    lbImg.alt = `Ad for ${displayName(a.client)}`;
    lbCap.innerHTML = `<strong>${displayName(a.client)}</strong> &nbsp;${a.name}&nbsp; ${lbIdx + 1}/${lbList.length}`;
  }
  wall.addEventListener("click", (e) => {
    const tile = e.target.closest(".tile");
    if (!tile) return;
    lbList = [...wall.querySelectorAll(".tile")].map((t) => +t.dataset.index);
    lbShow(lbList.indexOf(+tile.dataset.index));
    lb.showModal();
  });
  lb.querySelector(".lb-close").addEventListener("click", () => lb.close());
  lb.querySelector(".lb-prev").addEventListener("click", () => lbShow(lbIdx - 1));
  lb.querySelector(".lb-next").addEventListener("click", () => lbShow(lbIdx + 1));
  lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); });
  lb.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") lbShow(lbIdx - 1);
    if (e.key === "ArrowRight") lbShow(lbIdx + 1);
  });

  /* ---------- process: system mini-grid + iteration strip (GMW series) ---------- */
  const gmw = pipeline.filter(
    (a) => a.series === "Geldzugriffs-Report" && !a.name.includes("V2")
  ).slice(0, 9);
  document.getElementById("systemGrid").innerHTML = gmw
    .map((a) => `<img src="${a.file}" alt="Layout from the GeldMehrWert report series" loading="lazy">`)
    .join("");

  const iterFiles = [
    ["assets/ads/gmw_geldzugriffs_ads_1x1__gmw_geldzugriffs-report_01_4-ebenen-modell_1080x1080.jpg", "v1"],
    ["assets/ads/gmw_geldzugriffs_ads_1x1__gmw_geldzugriffs-report_v2-01_4-ebenen-modell_1080x1080.jpg", "v2"],
  ];
  document.getElementById("iterStrip").innerHTML = iterFiles
    .map(([f, v]) => `<figure><img src="${f}" alt="Version ${v} of the same ad" loading="lazy"><figcaption>${v}</figcaption></figure>`)
    .join("");

  /* ---------- hero: cursor image trail ---------- */
  const trailLayer = document.getElementById("trailLayer");
  const hero = document.querySelector(".hero");
  if (trailLayer && !reduceMotion && matchMedia("(hover: hover)").matches) {
    const trailPool = shuffled(work).slice(0, 24).map((a) => a.file);
    // warm the cache so the first trail images do not pop in late
    trailPool.slice(0, 8).forEach((f) => { const i = new Image(); i.src = f; });
    let last = { x: -999, y: -999 };
    let ti = 0;
    hero.addEventListener("pointermove", (e) => {
      const r = hero.getBoundingClientRect();
      const x = e.clientX - r.left;
      const y = e.clientY - r.top;
      if (Math.hypot(x - last.x, y - last.y) < 160) return;
      last = { x, y };
      const img = document.createElement("img");
      img.className = "trail-img";
      img.src = trailPool[ti++ % trailPool.length];
      img.alt = "";
      img.style.left = `${x}px`;
      img.style.top = `${y}px`;
      trailLayer.appendChild(img);
      while (trailLayer.children.length > 6) trailLayer.firstChild.remove();
      const rot = (Math.random() - 0.5) * 14;
      img.animate(
        [
          { transform: `translate(-50%,-50%) scale(.4) rotate(${rot * 2}deg)`, opacity: 0 },
          { transform: `translate(-50%,-50%) scale(1) rotate(${rot}deg)`, opacity: 1, offset: 0.25 },
          { transform: `translate(-50%,-46%) scale(1) rotate(${rot}deg)`, opacity: 1, offset: 0.75 },
          { transform: `translate(-50%,-38%) scale(.92) rotate(${rot}deg)`, opacity: 0 },
        ],
        { duration: 1300, easing: "cubic-bezier(0.16, 1, 0.3, 1)" }
      ).onfinish = () => img.remove();
    });
  }

  /* ---------- compare slider ---------- */
  const compare = document.getElementById("compare");
  const range = compare.querySelector(".compare-range");
  const setPos = (v) => compare.style.setProperty("--pos", `${v}%`);
  setPos(range.value);
  range.addEventListener("input", () => setPos(range.value));

  /* ---------- motion: play only while in view ---------- */
  const vids = document.querySelectorAll("[data-autoplay]");
  const vidObs = new IntersectionObserver(
    (entries) => {
      entries.forEach((en) => {
        const v = en.target;
        if (en.isIntersecting && !reduceMotion) {
          v.play().catch(() => {});
        } else {
          v.pause();
        }
      });
    },
    { threshold: 0.35 }
  );
  vids.forEach((v) => vidObs.observe(v));

  /* ---------- hero leopard: composite each frame onto the page color ----------
     iOS does not blend CSS over <video> layers, so we do the math in canvas:
     draw the frame, lift the whites past 255 (additive pass), then multiply
     the exact page cream on top. Paper becomes the page, ink stays indigo. */
  const leoVideo = document.querySelector(".leo-src");
  const leoCanvas = document.querySelector(".leo-canvas");
  if (leoVideo && leoCanvas) {
    const ctx = leoCanvas.getContext("2d");
    const cream = getComputedStyle(document.documentElement).getPropertyValue("--bg").trim() || "#f9f7ee";
    const desktopMq = matchMedia("(min-width: 901px)");
    let running = false;
    const draw = () => {
      // crop the clip's paper fold at top and bottom edges
      const cropY = Math.round(leoVideo.videoHeight * 0.05);
      const srcH = leoVideo.videoHeight - cropY * 2;
      if (leoVideo.videoWidth && leoCanvas.width !== leoVideo.videoWidth) {
        leoCanvas.width = leoVideo.videoWidth;
        leoCanvas.height = srcH;
      }
      if (leoCanvas.width) {
        ctx.globalCompositeOperation = "source-over";
        ctx.globalAlpha = 1;
        ctx.drawImage(leoVideo, 0, cropY, leoVideo.videoWidth, srcH, 0, 0, leoCanvas.width, leoCanvas.height);
        ctx.globalCompositeOperation = "lighter";
        ctx.globalAlpha = 0.3; // ~x1.3 brightness: the paper clips to clean white
        ctx.drawImage(leoVideo, 0, cropY, leoVideo.videoWidth, srcH, 0, 0, leoCanvas.width, leoCanvas.height);
        if (desktopMq.matches) {
          // desktop: white becomes the exact page cream, fully seamless
          ctx.globalCompositeOperation = "multiply";
          ctx.globalAlpha = 1;
          ctx.fillStyle = cream;
          ctx.fillRect(0, 0, leoCanvas.width, leoCanvas.height);
        }
      }
      if (running) requestAnimationFrame(draw);
    };
    leoVideo.addEventListener("play", () => {
      if (!running) { running = true; requestAnimationFrame(draw); }
    });
    leoVideo.addEventListener("pause", () => { running = false; });
    // paint the first frame even before autoplay kicks in
    leoVideo.addEventListener("loadeddata", () => { running || draw(); }, { once: true });
  }

  /* ---------- up & down: 3d tilt toward the cursor ---------- */
  const tiltCard = document.getElementById("tiltCard");
  if (tiltCard && !reduceMotion && matchMedia("(hover: hover)").matches) {
    const img = tiltCard.querySelector("img");
    tiltCard.addEventListener("pointermove", (e) => {
      const r = tiltCard.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width - 0.5;
      const py = (e.clientY - r.top) / r.height - 0.5;
      img.style.transform =
        `rotateY(${px * 14}deg) rotateX(${py * -14}deg) scale(1.03)`;
      img.style.boxShadow = `${-px * 30}px ${28 - py * 16}px 60px rgba(20, 22, 90, .35)`;
    });
    tiltCard.addEventListener("pointerleave", () => {
      img.style.transform = "";
      img.style.boxShadow = "";
    });
  }

  /* ---------- journey map: link stops and legend ---------- */
  const journey = document.getElementById("journey");
  if (journey) {
    const hot = (n, on) => {
      journey.querySelectorAll(`[data-stop="${n}"]`).forEach((el) =>
        el.classList.toggle("hot", on));
    };
    journey.querySelectorAll("[data-stop]").forEach((el) => {
      el.addEventListener("mouseenter", () => hot(el.dataset.stop, true));
      el.addEventListener("mouseleave", () => hot(el.dataset.stop, false));
    });
  }

  /* ---------- portrait fallback ---------- */
  const aboutPortrait = document.querySelector("#aboutPortrait img");
  aboutPortrait.addEventListener("error", () => document.getElementById("aboutPortrait").remove());

  /* ---------- scroll reveals ---------- */
  const revealables = document.querySelectorAll(
    ".sec-giant, .wall-lede, .compare-lede, .personal-lede, .about-body, .about-list"
  );
  revealables.forEach((el) => el.classList.add("reveal"));
  const revObs = new IntersectionObserver(
    (entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          en.target.classList.add("in");
          revObs.unobserve(en.target);
        }
      });
    },
    { threshold: 0.2 }
  );
  revealables.forEach((el) => revObs.observe(el));
})();
