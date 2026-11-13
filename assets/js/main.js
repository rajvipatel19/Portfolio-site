/* =========================================================
   SITE SETTINGS — edit these, nothing else needs touching
   ========================================================= */
const SITE = {
  // Cal.com username/event, e.g. "rajvipatel/30min". Leave "" to show the preview calendar.
  calLink: "rajvi-patel-3l0bak/30min",
  // Spotify track ID (from the share link) played by the CD
  spotifyTrack: "5MPLeS9KdZlA04OOCUb5Bt",
};

(() => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* ---------- Page load / leave transition ---------- */
  requestAnimationFrame(() => document.body.classList.add("loaded"));
  window.addEventListener("pageshow", (e) => { if (e.persisted) document.body.classList.remove("leaving"); });
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (!a || reduce) return;
    const href = a.getAttribute("href");
    if (!href || href.startsWith("#") || a.target === "_blank" || e.metaKey || e.ctrlKey || e.shiftKey) return;
    if (/^(https?:|mailto:|tel:)/.test(href)) return;
    e.preventDefault();
    document.body.classList.add("leaving");
    setTimeout(() => (window.location.href = href), 320);
  });

  /* ---------- Nav: hide on scroll down, mobile menu ---------- */
  const nav = $(".nav");
  if (nav) {
    let last = scrollY;
    addEventListener("scroll", () => {
      const y = scrollY;
      nav.classList.toggle("is-hidden", y > last && y > 240 && !nav.classList.contains("is-open"));
      last = y;
    }, { passive: true });
    // Phone/tablet: full-screen menu. Opens/closes on the ☰/× button,
    // closes on Escape or when a link is tapped; page can't scroll behind it.
    const toggle = $(".nav-toggle", nav);
    const setMenu = (open) => {
      nav.classList.toggle("is-open", open);
      document.documentElement.classList.toggle("menu-open", open);
      toggle?.setAttribute("aria-expanded", open);
      toggle?.setAttribute("aria-label", open ? "Close menu" : "Menu");
    };
    toggle?.addEventListener("click", () => setMenu(!nav.classList.contains("is-open")));
    $$(".nav-links a", nav).forEach((a) => a.addEventListener("click", () => setMenu(false)));
    addEventListener("keydown", (e) => { if (e.key === "Escape" && nav.classList.contains("is-open")) { setMenu(false); toggle?.focus(); } });
    matchMedia("(min-width: 861px)").addEventListener("change", (e) => { if (e.matches) setMenu(false); });
  }

  /* ---------- Split headings into words ---------- */
  $$(".split").forEach((el) => {
    let i = 0;
    const walk = (node) => {
      [...node.childNodes].forEach((n) => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(" ")); return; }
            const w = document.createElement("span"); w.className = "w";
            const inner = document.createElement("span"); inner.textContent = part; inner.style.setProperty("--i", i++);
            w.appendChild(inner); frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== "BR") walk(n);
      });
    };
    walk(el);
  });

  /* ---------- Reveal on scroll ---------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
  }, { threshold: 0.15, rootMargin: "0px 0px -6% 0px" });
  $$("[data-reveal], .split").forEach((el) => io.observe(el));

  /* ---------- Count-up numbers ---------- */
  const countIO = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      const el = en.target; countIO.unobserve(el);
      const end = parseFloat(el.dataset.count); const pre = el.dataset.pre || ""; const suf = el.dataset.suf || "";
      if (reduce) { el.textContent = pre + end.toLocaleString() + suf; return; }
      const t0 = performance.now(), dur = 1400;
      const tick = (t) => {
        const p = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3);
        el.textContent = pre + Math.round(end * e).toLocaleString() + suf;
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }, { threshold: 0.6 });
  $$("[data-count]").forEach((el) => countIO.observe(el));

  /* ---------- Custom cursor ---------- */
  if (fine && !reduce) {
    const c = document.createElement("div"); c.className = "cursor"; document.body.appendChild(c);
    let x = 0, y = 0, cx = 0, cy = 0;
    addEventListener("mousemove", (e) => { x = e.clientX; y = e.clientY; c.classList.add("on"); });
    document.addEventListener("mouseleave", () => c.classList.remove("on"));
    const loop = () => { cx += (x - cx) * 0.18; cy += (y - cy) * 0.18; c.style.transform = `translate(${cx}px, ${cy}px)`; requestAnimationFrame(loop); };
    loop();
    document.addEventListener("mouseover", (e) => c.classList.toggle("big", !!e.target.closest("a, button, .cd, .desk-item, .shot")));
  }

  /* ---------- Magnetic buttons ---------- */
  if (fine && !reduce) {
    $$(".magnetic").forEach((b) => {
      b.addEventListener("mousemove", (e) => {
        const r = b.getBoundingClientRect();
        b.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.22}px, ${(e.clientY - r.top - r.height / 2) * 0.3}px)`;
      });
      b.addEventListener("mouseleave", () => (b.style.transform = ""));
    });
  }

  /* ---------- Card tilt ---------- */
  if (fine && !reduce) {
    $$(".tilt").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = `perspective(1200px) rotateY(${px * 4}deg) rotateX(${-py * 4}deg) translateY(-4px)`;
      });
      card.addEventListener("mouseleave", () => (card.style.transform = ""));
    });
  }

  /* ---------- Case study card videos (add data-video="assets/media/x.mp4") ---------- */
  $$(".card[data-video]").forEach((card) => {
    const src = card.dataset.video; if (!src) return;
    const media = $(".card-media", card);
    const v = document.createElement("video");
    Object.assign(v, { muted: true, loop: true, playsInline: true, preload: "metadata", src });
    v.setAttribute("muted", ""); v.setAttribute("playsinline", "");
    v.addEventListener("loadeddata", () => v.classList.add("ready"));
    v.addEventListener("error", () => v.remove());
    media.appendChild(v);
    new IntersectionObserver(([en]) => { en.isIntersecting ? v.play().catch(() => {}) : v.pause(); }, { threshold: 0.35 }).observe(card);
  });

  /* ---------- Hero video (falls back to soft mesh if missing) ---------- */
  const hv = $(".hero-media video");
  if (hv) {
    hv.addEventListener("loadeddata", () => { $(".hero-media .mesh")?.remove(); $(".hero-media .video-note")?.remove(); });
    hv.addEventListener("error", () => hv.remove(), true);
    hv.querySelector("source")?.addEventListener("error", () => hv.remove());
  }

  /* ---------- Hero scroll: video drifts down + fades as the next section slides over it ---------- */
  const hero = $(".hero");
  if (hero && !reduce) {
    let ticking = false;
    const update = () => {
      ticking = false;
      const p = Math.min(Math.max(scrollY / hero.offsetHeight, 0), 1); // 0 at top → 1 when hero has scrolled away
      hero.style.setProperty("--hero-p", p.toFixed(3));
    };
    addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  /* ---------- CD player (Spotify iFrame API) ---------- */
  const stage = $(".cd-stage");
  if (stage) {
    const cd = $(".cd", stage), dock = $(".spotify-dock"), np = $(".now-playing");
    let controller = null, ready = false, playing = false, pendingPlay = false;
    const setPlaying = (p) => { playing = p; stage.classList.toggle("is-playing", p); np?.classList.toggle("is-playing", p);
      if (np) np.querySelector("span").textContent = p ? "Now playing" : "Paused — tap the CD"; };
    window.onSpotifyIframeApiReady = (IFrameAPI) => {
      const el = document.createElement("div"); dock.appendChild(el);
      IFrameAPI.createController(el, { uri: `spotify:track:${SITE.spotifyTrack}`, width: "100%", height: 80, theme: "light" }, (ctrl) => {
        controller = ctrl; ready = true;
        ctrl.addListener("playback_update", (e) => setPlaying(!e.data.isPaused));
        if (pendingPlay) { ctrl.togglePlay(); }
      });
    };
    let loaded = false;
    const loadApi = () => { if (loaded) return; loaded = true;
      const s = document.createElement("script"); s.src = "https://open.spotify.com/embed/iframe-api/v1"; s.async = true;
      s.onerror = () => { dock.innerHTML = `<a class="btn btn--sm" href="https://open.spotify.com/track/${SITE.spotifyTrack}" target="_blank" rel="noopener">Open the song on Spotify ↗</a>`; dock.style.height = "auto"; };
      document.head.appendChild(s); };
    // Preload the API when the CD gets close to view so the first tap is instant
    new IntersectionObserver(([en], o) => { if (en.isIntersecting) { loadApi(); o.disconnect(); } }, { rootMargin: "400px" }).observe(stage);
    const toggle = () => {
      dock.classList.add("open");
      if (ready && controller) controller.togglePlay();
      else { pendingPlay = true; loadApi(); setPlaying(!playing); }
    };
    cd.addEventListener("click", toggle);
    cd.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); } });
  }

  /* ---------- Book a call: Cal.com embed or preview calendar ---------- */
  const cal = $(".cal-frame");
  if (cal) {
    if (SITE.calLink) {
      cal.innerHTML = `<iframe src="https://cal.com/${SITE.calLink}?embed=true&theme=light&layout=month_view" title="Book a call with Rajvi" loading="lazy"></iframe>`;
      $$("[data-cal]").forEach((a) => (a.href = `https://cal.com/${SITE.calLink}`));
    } else {
      // Preview calendar so the layout reads right until a real link is added
      const grid = $(".cal-grid", cal), slots = $(".cal-slots", cal), title = $(".cal-month", cal);
      const now = new Date(), y = now.getFullYear(), m = now.getMonth();
      title.textContent = now.toLocaleString("en", { month: "long", year: "numeric" });
      const first = (new Date(y, m, 1).getDay() + 6) % 7, days = new Date(y, m + 1, 0).getDate();
      grid.innerHTML = ["M", "T", "W", "T", "F", "S", "S"].map((d) => `<b>${d}</b>`).join("") + "<span></span>".repeat(first);
      for (let d = 1; d <= days; d++) {
        const dow = (first + d - 1) % 7, past = d < now.getDate(), weekend = dow > 4;
        grid.insertAdjacentHTML("beforeend", `<span class="${past || weekend ? "off" : "av"}">${d}</span>`);
      }
      grid.addEventListener("click", (e) => {
        const s = e.target.closest(".av"); if (!s) return;
        $$(".on", grid).forEach((x) => x.classList.remove("on")); s.classList.add("on");
        slots.innerHTML = ["10:00", "11:30", "14:00", "16:30"].map((t) => `<button type="button">${t} GST</button>`).join("");
      });
    }
  }

  /* ---------- Draggable coffee desk ---------- */
  const desk = $(".desk");
  if (desk) {
    $$(".desk-item", desk).forEach((item) => {
      let sx, sy, ox, oy, rot = parseFloat(item.dataset.rot || 0);
      item.style.rotate = rot + "deg";
      item.addEventListener("pointerdown", (e) => {
        item.setPointerCapture(e.pointerId); item.classList.add("dragging");
        sx = e.clientX; sy = e.clientY;
        const t = new DOMMatrix(getComputedStyle(item).translate === "none" ? "" : `translate(${getComputedStyle(item).translate})`);
        ox = t.e || 0; oy = t.f || 0;
      });
      item.addEventListener("pointermove", (e) => {
        if (!item.classList.contains("dragging")) return;
        const dx = e.clientX - sx, dy = e.clientY - sy;
        item.style.translate = `${ox + dx}px ${oy + dy}px`;
        item.style.rotate = `${rot + dx * 0.04}deg`;
      });
      const end = () => { if (!item.classList.contains("dragging")) return; item.classList.remove("dragging"); rot = parseFloat(item.style.rotate) || rot; };
      item.addEventListener("pointerup", end); item.addEventListener("pointercancel", end);
    });
  }

  /* ---------- Case study roadmap scrollspy ---------- */
  $$(".roadmap").forEach((roadmap) => {
    const items = $$("li", roadmap), secs = items.map((li) => $(li.querySelector("a").getAttribute("href"))).filter(Boolean);
    const prog = $(".progress", roadmap), ol = $("ol", roadmap);
    const update = () => {
      const mid = innerHeight * 0.35; let idx = 0;
      secs.forEach((s, i) => { if (s.getBoundingClientRect().top < mid) idx = i; });
      items.forEach((li, i) => { li.classList.toggle("active", i === idx); li.classList.toggle("done", i < idx); });
      if (prog && items[idx]) {
        const node = items[idx].querySelector(".node");
        prog.style.height = node.getBoundingClientRect().top - ol.getBoundingClientRect().top - 6 + "px";
      }
      // keep the active pill visible on mobile
      if (getComputedStyle(roadmap).position === "sticky" && items[idx] && roadmap.scrollWidth > roadmap.clientWidth) {
        const li = items[idx];
        roadmap.scrollTo({ left: li.offsetLeft - roadmap.clientWidth / 2 + li.offsetWidth / 2, behavior: "smooth" });
      }
      // SILA side nav: show once past the hero, hide again over the footer
      if (roadmap.classList.contains("sl-side")) {
        const band = $(".sl-hero-band"), foot = $(".footer");
        const past = band ? band.getBoundingClientRect().bottom < innerHeight * 0.6 : true;
        const atFoot = foot ? foot.getBoundingClientRect().top < innerHeight * 0.85 : false;
        roadmap.classList.toggle("is-shown", past && !atFoot);
      }
    };
    let raf; addEventListener("scroll", () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(update); }, { passive: true });
    addEventListener("resize", update); update();
  });

  /* ---------- Case study videos: play only while on screen ---------- */
  const autoVids = $$("video[data-autoplay]");
  if (autoVids.length && "IntersectionObserver" in window) {
    const vio = new IntersectionObserver((entries) => entries.forEach((en) => {
      const v = en.target;
      if (en.isIntersecting) { if (v.preload === "none") v.preload = "auto"; if (!reduce) v.play().catch(() => {}); }
      else v.pause();
    }), { rootMargin: "200px 0px" });
    autoVids.forEach((v) => vio.observe(v));
  }

  /* ---------- Before / after slider ---------- */
  $$("[data-ba]").forEach((box) => {
    const r = $("input", box); if (!r) return;
    const set = () => box.style.setProperty("--pos", r.value + "%");
    r.addEventListener("input", set); set();
  });

  /* ---------- Footer: "Let's …" typing effect ---------- */
  const typeEl = $(".ft-type");
  if (typeEl && !reduce) {
    const words = typeEl.dataset.type.split("|"); let w = 0, i = words[0].length, del = true;
    const tick = () => {
      const word = words[w];
      if (del) { i--; if (i <= 0) { del = false; w = (w + 1) % words.length; } }
      else { i++; if (i >= words[w].length) { del = true; typeEl.textContent = words[w]; return setTimeout(tick, 1800); } }
      typeEl.textContent = words[w].slice(0, Math.max(i, 0));
      setTimeout(tick, del ? 45 : 85);
    };
    setTimeout(tick, 1800);
  }

  /* ---------- Footer year ---------- */
  $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
