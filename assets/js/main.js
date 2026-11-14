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
  // "/" and "/index.html" are the same page
  const samePage = (u) => u.pathname.replace(/index\.html$/, "") === location.pathname.replace(/index\.html$/, "");

  /* ---------- Page load / leave transition ---------- */
  requestAnimationFrame(() => document.body.classList.add("loaded"));
  setTimeout(() => document.body.classList.add("loaded"), 600); // never leave the page faded out
  window.addEventListener("pageshow", (e) => { if (e.persisted) document.body.classList.remove("leaving"); });
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (!a || reduce) return;
    const href = a.getAttribute("href");
    if (!href || href.startsWith("#") || a.target === "_blank" || e.metaKey || e.ctrlKey || e.shiftKey) return;
    if (/^(https?:|mailto:|tel:)/.test(href)) return;
    // a link to a section on this same page (e.g. Projects on the home page) doesn't leave — no fade-out
    const to = new URL(a.href, location.href);
    if (samePage(to) && to.hash) return;
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

  /* ---------- Case studies: each section fades up as it scrolls in, only the first time a page is opened ---------- */
  const cs = document.querySelector("main.sila");
  if (cs) {
    const key = "seen:" + location.pathname.replace(/index\.html$/, "");
    let seen = false;
    try { seen = localStorage.getItem(key) === "1"; localStorage.setItem(key, "1"); } catch (e) {}
    // these pages use the block reveal below instead of the per-card one
    cs.querySelectorAll("[data-reveal]").forEach((el) => el.removeAttribute("data-reveal"));
    if (!seen && !reduce) {
      // each whole section appears as one piece when its top comes into view
      const blocks = [...cs.querySelectorAll(":scope > section, :scope > .sl-main > section")];
      const rvIO = new IntersectionObserver((entries) => {
        entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("rv-in"); rvIO.unobserve(en.target); } });
      }, { threshold: 0, rootMargin: "0px 0px -12% 0px" });
      blocks.forEach((el) => { el.classList.add("rv"); rvIO.observe(el); });
    }
  }

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

  /* ---------- Arriving with a #section in the link (e.g. Projects from a case study): jump straight there ---------- */
  if (location.hash.length > 1) {
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (target) {
      if ("scrollRestoration" in history) history.scrollRestoration = "manual";
      const jump = () => target.scrollIntoView({ behavior: "instant", block: "start" });
      jump();
      addEventListener("load", () => { jump(); setTimeout(jump, 250); }, { once: true });
    }
  }

  /* ---------- Links to a section on this same page (e.g. Projects on the home page): scroll to it ---------- */
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[href*='#']");
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || a.target === "_blank") return;
    const url = new URL(a.href, location.href);
    if (!samePage(url) || url.hash.length < 2) return;
    const target = document.getElementById(decodeURIComponent(url.hash.slice(1)));
    if (!target) return;
    e.preventDefault();
    const startY = scrollY;
    target.scrollIntoView({ behavior: reduce ? "instant" : "smooth", block: "start" });
    history.pushState(null, "", url.hash);
    // if the browser skipped the smooth scroll (e.g. a background tab), jump straight there
    setTimeout(() => { if (scrollY === startY) target.scrollIntoView({ behavior: "instant", block: "start" }); }, 400);
  });

  /* ---------- Footer year ---------- */
  $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();

/* =========================================================
   WHAT I BRING TO THE TABLE
   ========================================================= */
(() => {
  const wrap = document.querySelector(".gt-wrap");
  if (!wrap) return;
  const gt = wrap.querySelector(".gt"), panel = wrap.querySelector(".panel");
  const obs = [...gt.querySelectorAll(".ob")];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const touch = matchMedia("(hover: none)").matches;
  const DATA = [
    { title: "I ask why before how.", text: "I want to understand the problem before jumping into solutions. The right question saves weeks of the wrong screens.",
      proof: "Before designing SILA, I read through App Store and Play Store reviews of the biggest transfer apps in the UAE." },
    { title: "I think in systems.", text: "I look at the bigger picture, not just the screen in front of me: flows, edge cases, states, and how it all scales.",
      proof: "At CityLockers I designed one ecosystem across four surfaces: app, website, kiosk and client portal." },
    { title: "I like getting my hands dirty.", text: "From Figma to prototypes to code, I enjoy bringing ideas to life myself. With AI, concept and shipped product sit closer than ever.",
      proof: "This portfolio was designed and coded by me, with Claude Code." },
    { title: "I value honest collaboration.", text: "Good work comes from curiosity, trust and challenging each other's thinking, with founders, developers and users alike.",
      proof: "Built and led a design team from scratch at Kilopoints, side by side with founders and developers." },
    { title: "My toolkit, AI included.", text: "AI is my thinking partner, not my replacement. I use Claude to pressure-test flows, write UX copy and build faster, getting from idea to prototype sooner. The decisions stay human.",
      proof: "From messy brief to working prototype, faster.",
      tools: ["Figma", "Claude", "ChatGPT", "Notion", "GitHub", "Vercel", "Canva", "Spotify"] },
    { title: "I design with a clinician's care.", text: "Years as a dentist taught me to look beneath the surface, explain clearly, and earn trust before asking for it.",
      proof: "That's why I'm drawn to health-tech and fintech, where trust is the product." },
  ];

  /* ---- detail window ---- */
  const $ = (s) => panel.querySelector(s), swap = $(".swap");
  let cur = -1;
  const fill = (i) => {
    const d = DATA[i];
    $(".p-num").textContent = String(i + 1).padStart(2, "0") + " / " + String(DATA.length).padStart(2, "0");
    $("h3").textContent = d.title; $(".p-text").textContent = d.text; $(".p-proof span").textContent = d.proof;
    $(".p-tools").innerHTML = (d.tools || []).map((t) => `<span>${t}</span>`).join("");
  };
  const open = (i) => {
    i = (i + DATA.length) % DATA.length;
    const was = wrap.classList.contains("has-open");
    obs.forEach((o) => o.classList.toggle("on", +o.dataset.k === i));
    wrap.classList.add("has-open");
    if (was && i !== cur) { swap.classList.add("out"); setTimeout(() => { fill(i); swap.classList.remove("out"); }, 220); } else fill(i);
    cur = i;
  };
  const close = () => { wrap.classList.remove("has-open"); obs.forEach((o) => o.classList.remove("on")); cur = -1; };
  obs.forEach((o) => {
    o.addEventListener("click", (e) => { if (e.target.closest(".tool")) return; e.stopPropagation(); +o.dataset.k === cur ? close() : open(+o.dataset.k); });
    o.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); o.click(); } });
  });
  $(".panel-close").addEventListener("click", (e) => { e.stopPropagation(); close(); });
  $(".p-next").addEventListener("click", (e) => { e.stopPropagation(); open(cur + 1); });
  $(".p-prev").addEventListener("click", (e) => { e.stopPropagation(); open(cur - 1); });
  panel.addEventListener("click", (e) => e.stopPropagation());
  gt.addEventListener("click", close);
  document.addEventListener("keydown", (e) => { if (cur < 0) return; if (e.key === "Escape") close(); if (e.key === "ArrowRight") open(cur + 1); if (e.key === "ArrowLeft") open(cur - 1); });

  /* ---- light streak + checks follow the cursor (smoothed) ---- */
  let tx = 0, ty = 0, mx = 0, my = 0, running = false;
  const tick = () => {
    mx += (tx - mx) * .14; my += (ty - my) * .14;
    gt.style.setProperty("--mx", mx + "px"); gt.style.setProperty("--my", my + "px");
    if (Math.abs(tx - mx) + Math.abs(ty - my) > .3) requestAnimationFrame(tick); else running = false;
  };
  gt.addEventListener("pointerenter", (e) => { const r = gt.getBoundingClientRect(); mx = tx = e.clientX - r.left; my = ty = e.clientY - r.top; });
  gt.addEventListener("pointermove", (e) => { const r = gt.getBoundingClientRect(); tx = e.clientX - r.left; ty = e.clientY - r.top; if (!running) { running = true; requestAnimationFrame(tick); } });

  /* ---- gift box: confetti burst of tool logos ---- */
  const box = gt.querySelector(".o-box");
  if (!box) return;
  const TOOLS = [
    { slug: "figma", name: "Figma", use: "where ideas take shape" }, { slug: "claude", name: "Claude", use: "my thinking partner" },
    { slug: "chatgpt", name: "ChatGPT", use: "untangling the brief" }, { slug: "notion", name: "Notion", use: "my second brain" },
    { slug: "github", name: "GitHub", use: "where the code lives" }, { slug: "vercel", name: "Vercel", use: "where this site lives" },
    { slug: "canva", name: "Canva", use: "quick visuals" }, { slug: "spotify", name: "Spotify", use: "focus mode on" },
  ];
  const tw = box.querySelector(".tools"), sw = box.querySelector(".sparks");
  const tiles = TOOLS.map((t) => {
    const el = document.createElement("div"); el.className = "tool";
    el.innerHTML = `<img src="assets/icons/${t.slug}.svg" alt="${t.name}"><span class="tip"><b>${t.name}</b><span>${t.use}</span></span>`;
    tw.appendChild(el); return el;
  });
  const rand = (s) => { const x = Math.sin(s * 99.13) * 43758.5453; return x - Math.floor(x); };
  const STAR = '<svg viewBox="0 0 20 20"><path d="M10 0 C11 7 13 9 20 10 C13 11 11 13 10 20 C9 13 7 11 0 10 C7 9 9 7 10 0Z" fill="currentColor"/></svg>';
  const colors = ["#f3cf6a", "#f6dc93", "#fff2c6", "#e9c25c", "#d9cdf5", "#f7c9d6"];
  for (let k = 0; k < 16; k++) {
    const sp = document.createElement("span"); sp.className = "spark"; sp.innerHTML = STAR; const r = (a) => rand(k * 13 + a);
    sp.style.cssText = `--s:${6 + r(1) * 11}px;--c:${colors[k % colors.length]};--x0:${(r(2) - .5) * 180}px;--drift:${(r(3) - .5) * 100}px;--h:${180 + r(4) * 200}px;--d:${2.6 + r(5) * 2.4}s;--dl:${r(6) * 3}s`;
    sw.appendChild(sp);
  }
  let slots = [], popY = 0, isOpen = false, anims = [];
  const layout = () => {
    const w = box.offsetWidth, ts = Math.round(Math.max(26, Math.min(60, gt.offsetWidth * .05)));
    box.style.setProperty("--ts", ts + "px");
    const rows = [3, 3, 2], dx = ts * 1.42, dy = ts * 1.22, baseY = -w * .5 - ts * .6; popY = -w * .25;
    slots = []; let i = 0;
    rows.forEach((count, r) => { for (let c = 0; c < count; c++, i++) {
      slots.push({ x: (c - (count - 1) / 2) * dx + (r % 2 ? dx * .32 : -dx * .18) + (rand(i + 1) - .5) * ts * .22,
        y: baseY - r * dy + (rand(i + 7) - .5) * ts * .28, r: (rand(i + 3) - .5) * 30, spin: (rand(i + 5) > .5 ? 1 : -1) * (180 + rand(i + 9) * 200) });
    } });
    tiles.forEach((t, k) => { t.style.zIndex = k + 1; t.style.setProperty("--rot", slots[k].r + "deg"); });
  };
  const openBox = () => {
    if (isOpen) return; isOpen = true; box.classList.add("is-open");
    anims.forEach((a) => a.cancel());
    anims = tiles.map((t, i) => { const s = slots[i]; return t.animate(reduce ? [
      { transform: `translate(${s.x}px, ${s.y}px) rotate(${s.r}deg)`, opacity: 1 }, { transform: `translate(${s.x}px, ${s.y}px) rotate(${s.r}deg)`, opacity: 1 }] : [
      { transform: `translate(0px, ${popY}px) scale(.3) rotate(0deg)`, opacity: 0 },
      { transform: `translate(${s.x * 1.35}px, ${s.y - 70}px) scale(1.1) rotate(${s.r + s.spin}deg)`, opacity: 1, offset: .5 },
      { transform: `translate(${s.x}px, ${s.y + 6}px) scale(.98) rotate(${s.r - 4}deg)`, opacity: 1, offset: .82 },
      { transform: `translate(${s.x}px, ${s.y}px) scale(1) rotate(${s.r}deg)`, opacity: 1 }
    ], { duration: reduce ? 1 : 950, delay: reduce ? 0 : 240 + i * 115, easing: "cubic-bezier(.2,.8,.3,1)", fill: "both" }); });
  };
  const closeBox = () => {
    if (!isOpen) return; isOpen = false; box.classList.remove("is-open");
    anims.forEach((a) => a.cancel());
    anims = tiles.map((t, i) => { const s = slots[i]; return t.animate([
      { transform: `translate(${s.x}px, ${s.y}px) scale(1) rotate(${s.r}deg)`, opacity: 1 },
      { transform: `translate(${s.x * .4}px, ${s.y - 20}px) scale(.9) rotate(${s.r + s.spin * .4}deg)`, opacity: 1, offset: .4 },
      { transform: `translate(0px, ${popY}px) scale(.3) rotate(0deg)`, opacity: 0 }
    ], { duration: reduce ? 1 : 520, delay: reduce ? 0 : (tiles.length - 1 - i) * 50, easing: "cubic-bezier(.55,0,.45,1)", fill: "both" }); });
  };
  layout(); addEventListener("resize", () => { layout(); if (isOpen) { isOpen = false; openBox(); } });
  if (!touch) { box.addEventListener("mouseenter", openBox); box.addEventListener("mouseleave", closeBox); }
  else box.addEventListener("click", () => (isOpen ? closeBox : openBox)());
  box.addEventListener("focus", openBox); box.addEventListener("blur", closeBox);
})();
