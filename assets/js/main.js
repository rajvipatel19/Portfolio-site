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

  /* ---------- Light / Dark: the glass switch in the nav. Starts light; the choice is remembered ---------- */
  const themeBtns = $$(".ts-btn");
  const setThemeUI = () => {
    const dark = document.documentElement.dataset.theme === "dark";
    themeBtns.forEach((b) => b.setAttribute("aria-pressed", String((b.dataset.setTheme === "dark") === dark)));
    const meta = $('meta[name="theme-color"]'); if (meta) meta.content = dark ? "#2c2a46" : "#fdfcff";
  };
  setThemeUI();
  // the hero view for the other theme loads once the page is ready (or straight away when the theme is switched)
  const loadAllViews = () => $$(".hero-view[data-src]").forEach((i) => { if (!i.getAttribute("src")) i.src = i.dataset.src; });
  addEventListener("load", () => setTimeout(loadAllViews, 1500), { once: true });
  themeBtns.forEach((b) => b.addEventListener("click", () => {
    loadAllViews();
    const dark = b.dataset.setTheme === "dark";
    if (dark === (document.documentElement.dataset.theme === "dark")) return;
    document.documentElement.classList.add("theme-switching");
    if (dark) document.documentElement.dataset.theme = "dark"; else delete document.documentElement.dataset.theme;
    try { sessionStorage.setItem("theme", dark ? "dark" : "light"); } catch (e) {} // remembered for this visit only
    setThemeUI();
    setTimeout(() => document.documentElement.classList.remove("theme-switching"), 450);
  }));
  // "/" and "/index.html" are the same page
  const samePage = (u) => u.pathname.replace(/index\.html$/, "") === location.pathname.replace(/index\.html$/, "");

  /* ---------- Page load / leave transition ---------- */
  // First home visit: the single-colour cover stays until the hero pictures have loaded, then opens up to reveal the site
  // (a shimmer skeleton and "just a minute" show only if that takes a while; never longer than 3 seconds). Every other page: a quick fade, as before.
  const reveal = () => document.body.classList.add("loaded");
  if (document.documentElement.classList.contains("first-reveal")) {
    // wait only for the hero pictures (not every picture on the page), and never more than 3 seconds
    const waits = [], room = $(".hero-room");
    if (room) { const cs = getComputedStyle(room);
      [cs.backgroundImage, cs.webkitMaskImage || cs.maskImage].forEach((v) => { const m = /url\("?(.*?)"?\)/.exec(v || "");
        if (m) waits.push(new Promise((ok) => { const im = new Image(); if (/mask/.test(m[1])) im.crossOrigin = "anonymous"; /* same mode as the preload, so it is not fetched twice */ im.onload = im.onerror = ok; im.src = m[1]; })); }); }
    const view = $(document.documentElement.dataset.theme === "dark" ? ".hero-view--night" : ".hero-view--day");
    if (view) { view.loading = "eager"; waits.push(view.decode().catch(() => {})); }
    Promise.all(waits).then(() => requestAnimationFrame(reveal));
    setTimeout(reveal, 1800);
  } else {
    requestAnimationFrame(reveal); setTimeout(reveal, 600);
  }
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

  /* ---------- Offline: register the service worker that shows the firefly game when there's no internet ---------- */
  if ("serviceWorker" in navigator && location.protocol.startsWith("http")) {
    addEventListener("load", () => navigator.serviceWorker.register("/sw.js").catch(() => {}), { once: true });
  }

  /* ---------- Comments, like Figma: pick the speech bubble (or press C), click anywhere, write, post ----------
     Comments are saved in Supabase (a free online database). A new comment arrives with approved = false,
     so nobody sees it until Rajvi ticks "approved" in the Supabase dashboard (Table Editor → comments).
     The URL and publishable key below are meant to be public; the database rules decide what visitors can do. */
  const cBar = $(".cmt-bar");
  if (cBar) {
    const DB = "https://bstlylauvpcwlubqzpbk.supabase.co/rest/v1/comments", KEY = "sb_publishable_ax6mrJDyFHZrHxG9r0BR6A_mpLrgpAS";
    let cache = [];
    const store = {
      // only approved comments come back: the database hides the rest
      async load(pg) {
        try {
          const r = await fetch(DB + "?select=id,created_at,path,fx,fy,x,y,name,body&page=eq." + encodeURIComponent(pg) + "&order=created_at", { headers: { apikey: KEY } });
          if (!r.ok) return [];
          return (await r.json()).map((c) => ({ id: c.id, path: c.path, fx: c.fx, fy: c.fy, x: c.x, y: c.y, name: c.name, text: c.body, time: c.created_at }));
        } catch (e) { return []; }
      },
      async add(c) {
        try {
          const r = await fetch(DB, { method: "POST", headers: { apikey: KEY, "Content-Type": "application/json", Prefer: "return=minimal" },
            body: JSON.stringify({ page: c.page, path: c.path, fx: c.fx, fy: c.fy, x: c.x, y: c.y, name: c.name || null, body: c.text }) });
          return r.ok;
        } catch (e) { return false; }
      },
    };
    const toast = (msg) => {
      const t = document.createElement("div"); t.className = "cmt-toast"; t.setAttribute("role", "status"); t.textContent = msg;
      document.body.appendChild(t); setTimeout(() => t.classList.add("is-out"), 4200); setTimeout(() => t.remove(), 4700);
    };
    const layer = $(".cmt-layer");
    const moveBtn = $(".cmt-move"), addBtn = $(".cmt-add"), eyeBtn = $(".cmt-eye");
    const page = location.pathname.replace(/\/index(\.html)?$/, "/").replace(/\.html$/, "") || "/";
    const esc = (t) => t.replace(/[&<>"']/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
    const initial = (n) => (n || "Guest").trim().charAt(0).toUpperCase() || "G";
    const when = (t) => new Date(t).toLocaleString([], { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
    let mode = false, draft = null;

    // where a comment sits: the element under the click (a path from <body>) and the spot inside it, so it stays put when the layout changes
    const pathOf = (el) => { const parts = []; while (el && el !== document.body) { const p = el.parentElement; if (!p) break; parts.unshift(el.tagName.toLowerCase() + ":nth-child(" + ([...p.children].indexOf(el) + 1) + ")"); el = p; } return "body>" + parts.join(">"); };
    const anchorAt = (x, y) => {
      layer.style.display = "none"; let el = document.elementFromPoint(x, y); layer.style.display = "";
      el = el && (el.closest("section, header, footer, article, figure, .card, img, video") || el);
      const r = el.getBoundingClientRect();
      return { path: pathOf(el), fx: (x - r.left) / (r.width || 1), fy: (y - r.top) / (r.height || 1), x: x + scrollX, y: y + scrollY };
    };
    const placeOf = (c) => {
      let el = null; try { el = document.querySelector(c.path); } catch (e) {}
      if (!el) return { x: c.x, y: c.y };
      const r = el.getBoundingClientRect();
      return { x: r.left + scrollX + c.fx * r.width, y: r.top + scrollY + c.fy * r.height };
    };
    const mine = () => cache;

    const closePops = () => $$(".cmt-pop", layer).forEach((p) => p.remove());
    const openPop = (c, pin) => {
      closePops();
      const pop = document.createElement("div"); pop.className = "cmt-pop cmt-glass"; pop.setAttribute("role", "dialog"); pop.setAttribute("aria-label", "Comment by " + (c.name || "Guest"));
      pop.innerHTML = `<div class="cmt-who"><span class="cmt-av">${esc(initial(c.name))}</span><b>${esc(c.name || "Guest")}</b><time>${when(c.time)}</time></div><p>${esc(c.text)}</p>
        <div class="cmt-actions"><button type="button" class="cmt-close">Close</button></div>`;
      pop.style.left = pin.style.left; pop.style.top = pin.style.top; layer.appendChild(pop);
      $(".cmt-close", pop).addEventListener("click", closePops);
      $(".cmt-close", pop).focus();
    };
    const render = () => {
      $$(".cmt-pin:not(.cmt-pin--draft)", layer).forEach((p) => p.remove());
      const list = mine();
      list.forEach((c, i) => {
        const p = placeOf(c), pin = document.createElement("button");
        pin.type = "button"; pin.className = "cmt-pin"; pin.dataset.id = c.id;
        pin.style.left = p.x + "px"; pin.style.top = p.y + "px"; pin.textContent = initial(c.name);
        pin.setAttribute("aria-label", "Comment " + (i + 1) + " by " + (c.name || "Guest"));
        pin.addEventListener("click", (e) => { e.stopPropagation(); openPop(c, pin); });
        layer.appendChild(pin);
      });
    };

    const setMode = (on) => {
      mode = on; addBtn.setAttribute("aria-pressed", String(on)); moveBtn.setAttribute("aria-pressed", String(!on));
      document.documentElement.classList.toggle("cmt-mode", on);
      if (!on) cancelDraft();
    };
    const cancelDraft = () => { if (draft) { draft.pin.remove(); draft.box.remove(); draft = null; } };
    const startDraft = (x, y) => {
      cancelDraft(); closePops();
      const at = anchorAt(x, y);
      const pin = document.createElement("span"); pin.className = "cmt-pin cmt-pin--draft"; pin.style.left = at.x + "px"; pin.style.top = at.y + "px";
      let name = ""; try { name = localStorage.getItem("commentName") || ""; } catch (e) {}
      const box = document.createElement("form"); box.className = "cmt-box cmt-glass"; box.setAttribute("aria-label", "New comment");
      box.innerHTML = `<label class="cmt-sr" for="cmt-name">Your name</label><input id="cmt-name" class="cmt-name" type="text" maxlength="40" placeholder="Your name (optional)" value="${esc(name)}" autocomplete="name">
        <label class="cmt-sr" for="cmt-text">Comment</label><textarea id="cmt-text" class="cmt-text" rows="3" maxlength="500" placeholder="Add a comment"></textarea>
        <div class="cmt-actions"><button type="button" class="cmt-cancel">Cancel</button><button type="submit" class="cmt-post" disabled>Post</button></div>`;
      box.style.left = at.x + "px"; box.style.top = at.y + "px";
      layer.append(pin, box);
      const text = $(".cmt-text", box), post = $(".cmt-post", box);
      text.addEventListener("input", () => (post.disabled = !text.value.trim()));
      text.addEventListener("keydown", (e) => { if (e.key === "Enter" && (e.metaKey || e.ctrlKey) && text.value.trim()) box.requestSubmit(); });
      $(".cmt-cancel", box).addEventListener("click", () => setMode(false));
      box.addEventListener("submit", async (e) => {
        e.preventDefault(); const nm = $(".cmt-name", box).value.trim();
        try { localStorage.setItem("commentName", nm); } catch (er) {}
        post.disabled = true; post.textContent = "Sending…";
        const ok = await store.add({ page, ...at, name: nm, text: text.value.trim() });
        if (ok) { setMode(false); toast("Thanks! Your comment will appear once Rajvi approves it."); }
        else { post.disabled = false; post.textContent = "Post"; toast("Sorry, that didn't send. Please try again."); }
      });
      draft = { pin, box }; text.focus();
    };

    addBtn.addEventListener("click", () => setMode(!mode));
    moveBtn.addEventListener("click", () => setMode(false));
    eyeBtn.addEventListener("click", () => { const on = eyeBtn.getAttribute("aria-pressed") !== "true"; eyeBtn.setAttribute("aria-pressed", String(on)); layer.classList.toggle("cmt-hidden", !on); });
    // in comment mode a click anywhere (except on the comment tools) places a comment instead of following links
    document.addEventListener("click", (e) => {
      if (!mode || e.target.closest(".cmt-bar, .cmt-box, .cmt-pop, .nav")) return;
      e.preventDefault(); e.stopPropagation(); startDraft(e.clientX, e.clientY);
    }, true);
    document.addEventListener("keydown", (e) => {
      const typing = e.target.closest("input, textarea, [contenteditable]");
      if (e.key === "Escape") { if (draft || mode) setMode(false); closePops(); }
      else if (!typing && !e.metaKey && !e.ctrlKey && !e.altKey && (e.key === "c" || e.key === "C")) setMode(!mode);
      else if (!typing && !e.metaKey && !e.ctrlKey && !e.altKey && (e.key === "v" || e.key === "V") && mode) setMode(false);
    });
    render();
    store.load(page).then((l) => { cache = l; render(); });
    addEventListener("resize", render); addEventListener("load", render);
    new ResizeObserver(() => { if (!draft) render(); }).observe(document.body);
  }

  /* ---------- Nav: hide on scroll down, mobile menu ---------- */
  const nav = $(".nav");
  if (nav) {
    let last = scrollY;
    const heroBox = $(".hero");
    const onHero = () => nav.classList.toggle("on-hero", !!heroBox && scrollY < heroBox.offsetHeight - 90);
    onHero();
    addEventListener("scroll", () => {
      const y = scrollY;
      onHero();
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

  /* ---------- Case studies: each section fades up once as it scrolls in, on every page load ---------- */
  const cs = document.querySelector("main.sila");
  if (cs) {
    // these pages use the block reveal below instead of the per-card one
    cs.querySelectorAll("[data-reveal]").forEach((el) => el.removeAttribute("data-reveal"));
    if (!reduce) {
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

  /* ---------- About: as the next stacking card slides over, the one underneath shrinks back a little ---------- */
  const stackCards = $$(".stack-card");
  if (stackCards.length > 1 && !reduce) {
    let ticking = false, vh = innerHeight, stuck = [];
    const measure = () => { vh = innerHeight; stuck = stackCards.map((c) => parseFloat(getComputedStyle(c).top) || 0); };
    const stackUpdate = () => {
      ticking = false;
      stackCards.forEach((card, i) => {
        const next = stackCards[i + 1];
        if (!next) return;
        // 0 while the next card is below the screen, 1 once it has slid all the way up over this one
        const p = Math.min(1, Math.max(0, (vh - next.getBoundingClientRect().top) / (vh - stuck[i + 1])));
        if (card._p !== p) { card._p = p; card.style.setProperty("--p", p.toFixed(3)); }
      });
    };
    addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(stackUpdate); } }, { passive: true });
    addEventListener("resize", () => { measure(); stackUpdate(); });
    measure(); stackUpdate();
  }

  /* ---------- About: photo library, a curved wall of photos drifting sideways ---------- */
  const lib = $(".lib");
  if (lib) {
    const GAP = innerWidth < 640 ? 14 : 22; // space between photos
    const rows = $$(".lib-row", lib).map((row, r) => ({ row, tiles: $$(".lib-ph", row), off: 0, dir: r ? 1 : -1, speed: r ? 20 : 26, paused: false }));
    let W = 0, run = false, last = 0;
    const layout = () => {
      W = lib.clientWidth;
      rows.forEach((R) => { R.tw = R.tiles[0].offsetWidth + GAP; R.total = R.tw * R.tiles.length; });
    };
    const place = (R) => {
      const half = W / 2;
      R.tiles.forEach((t, i) => {
        const x = (((i * R.tw + R.off) % R.total) + R.total) % R.total - R.tw; // wraps around off-screen
        const u = Math.max(-1.3, Math.min(1.3, (x + R.tw / 2 - half) / half)); // -1 left edge, 0 centre, 1 right edge
        t.style.transform = `translate3d(${x.toFixed(1)}px,0,${(u * u * 150).toFixed(1)}px) rotateY(${(-u * 34).toFixed(2)}deg)`;
      });
    };
    const tick = (now) => {
      if (!run) return;
      const dt = Math.min(64, now - (last || now)) / 1000; last = now;
      rows.forEach((R) => { if (!R.paused) { R.off += R.dir * R.speed * dt; place(R); } });
      requestAnimationFrame(tick);
    };
    rows.forEach((R) => {
      R.row.addEventListener("pointerenter", (e) => { if (e.pointerType === "mouse") R.paused = true; });
      R.row.addEventListener("pointerleave", () => { R.paused = false; });
    });
    layout(); rows.forEach(place);
    addEventListener("resize", () => { layout(); rows.forEach(place); });
    // only moves while the wall is on screen
    new IntersectionObserver(([en]) => {
      const was = run; run = en.isIntersecting && !reduce;
      if (run && !was) { last = 0; requestAnimationFrame(tick); }
    }).observe(lib);
  }

  /* ---------- About: stop-motion photos in the polaroid; each frame lands slightly off, like hand-shot stop motion ---------- */
  const meBox = $(".me-motion");
  if (meBox) {
    const frames = $$("img", meBox);
    let fi = 0;
    if (!reduce && frames.length > 1) {
      setInterval(() => {
        if (document.hidden) return;
        frames[fi].classList.remove("is-on");
        fi = (fi + 1) % frames.length;
        const j = (n) => (Math.random() * 2 - 1) * n;
        frames[fi].style.transform = `translate(${j(1.6).toFixed(1)}px, ${j(1.6).toFixed(1)}px) rotate(${j(0.6).toFixed(2)}deg) scale(1.03)`;
        frames[fi].classList.add("is-on");
      }, 320);
    }
    // phones have no hover: a tap switches colour on and off
    if (matchMedia("(hover: none)").matches) (meBox.closest(".polaroid") || meBox.parentElement).addEventListener("click", () => meBox.classList.toggle("is-color"));
  }

  /* ---------- Home hero: letters light up in a new colour each time; a soft glow follows the pointer and uncovers the picnic check ---------- */
  const ht = $(".ht");
  if (ht) {
    const LETTER_COLOURS = ["#f06a9b", "#3fb37f", "#e9b22c", "#4a9be8", "#f08a4b", "#8a6ee8", "#2fb5b0", "#e5534b"];
    let next = 0;
    $$(".ht-l", ht).forEach((l) => {
      let t = 0;
      l.addEventListener("pointerenter", () => {
        clearTimeout(t);
        l.style.color = LETTER_COLOURS[next++ % LETTER_COLOURS.length];
        l.classList.add("is-lit");
      });
      l.addEventListener("pointerleave", () => {
        l.classList.remove("is-lit");
        t = setTimeout(() => { l.style.color = ""; }, 700); // the colour lingers, then fades back
      });
    });
    // the polaroid sticks exactly where it starts, so scrolling never nudges it up first (wide screens only)
    const vid = $(".ht-video", ht);
    const pinVid = () => {
      if (!vid || innerWidth <= 900) { if (vid) vid.style.top = ""; return; }
      vid.style.position = "relative"; vid.style.top = "0px"; // measure its natural spot (no offset)
      const start = vid.getBoundingClientRect().top + scrollY;
      vid.style.position = "";
      vid.style.top = Math.max(100, Math.round(start)) + "px";
    };
    // as the next section's top edge reaches the polaroid, the polaroid fades out from the bottom up (a soft edge, never a hard cut)
    const nextSec = $(".ht-next");
    const FADE = 140;
    let sinkRaf = 0;
    const sink = () => {
      sinkRaf = 0;
      if (!vid || !nextSec) return;
      const v = vid.getBoundingClientRect();
      // once the polaroid stops sticking, it scrolls away together with the section, so it must be fully gone by then:
      // shift the fade up by however much of the polaroid would still peek out at that moment (+ a little margin)
      const lead = Math.max(0, v.height - parseFloat(getComputedStyle(nextSec).marginTop) * -1) + 40;
      const cut = nextSec.getBoundingClientRect().top - v.top - lead; // where the polaroid should end, inside it
      if (cut >= v.height + FADE * 0.25) { vid.style.webkitMaskImage = vid.style.maskImage = ""; vid.style.visibility = ""; return; }
      if (cut <= 0) { vid.style.visibility = "hidden"; return; }
      vid.style.visibility = "";
      const m = `linear-gradient(180deg, #000 ${Math.round(cut - FADE)}px, transparent ${Math.round(cut)}px)`;
      vid.style.webkitMaskImage = m; vid.style.maskImage = m;
    };
    addEventListener("scroll", () => { if (!sinkRaf) sinkRaf = requestAnimationFrame(sink); }, { passive: true });
    const layoutHero = () => { pinVid(); sink(); };
    layoutHero(); addEventListener("resize", layoutHero); addEventListener("load", layoutHero);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(layoutHero); // measure again once the fonts have loaded
    const bg = $(".ht-bg", ht);
    if (bg && matchMedia("(hover: hover)").matches) {
      let raf = 0, px = 0, py = 0;
      ht.addEventListener("pointermove", (e) => {
        const r = ht.getBoundingClientRect(); px = e.clientX - r.left; py = e.clientY - r.top;
        if (!raf) raf = requestAnimationFrame(() => { raf = 0; bg.style.setProperty("--mx", px + "px"); bg.style.setProperty("--my", py + "px"); });
        ht.classList.add("is-hover");
      });
      ht.addEventListener("pointerleave", () => ht.classList.remove("is-hover"));
    }
  }

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

  /* ---------- Hero framing: on narrower screens, line the window's black right frame up with the screen's right edge ---------- */
  const heroBox = $(".hero");
  if (heroBox && $(".hero-room")) {
    const IMG_W = 2000, IMG_H = 1116, FRAME_RIGHT = 0.965; // the window frame ends ~96.5% across the picture
    const fitHero = () => {
      const w = heroBox.offsetWidth, h = heroBox.offsetHeight;
      const shownW = Math.max(w, h * IMG_W / IMG_H), r = w / shownW;   // how much of the picture's width fits on screen
      const x = r >= FRAME_RIGHT ? 0.5 : (FRAME_RIGHT - r) / (1 - r);
      heroBox.style.setProperty("--hpos", `${(x * 100).toFixed(2)}% 50%`);
    };
    fitHero(); addEventListener("resize", fitHero); addEventListener("load", fitHero);
  }

  /* ---------- Hero scroll: video drifts down + fades as the next section slides over it ---------- */
  const hero = $(".hero");
  if (hero && !reduce) {
    let ticking = false;
    const update = () => {
      ticking = false;
      const p = Math.min(Math.max(scrollY / hero.offsetHeight, 0), 1); // 0 at top → 1 when hero has scrolled away
      hero.style.setProperty("--hero-p", p.toFixed(3));
      target = p; if (!easing) { easing = true; requestAnimationFrame(ease); }
    };
    // a softly trailing copy of the scroll progress, so the room layer glides instead of jumping
    let target = 0, hs = 0, easing = false;
    const ease = () => {
      hs += (target - hs) * 0.12;
      if (Math.abs(target - hs) < 0.0005) hs = target;
      hero.style.setProperty("--hs", hs.toFixed(4));
      if (hs !== target) requestAnimationFrame(ease); else easing = false;
    };
    addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  /* ---------- Footer scene: the hero picture builds back up as you reach the end of the page ---------- */
  const ftScene = $(".ft--scene");
  if (ftScene && !reduce) {
    let fTarget = 0, fs = 0, fEasing = false, fTick = false;
    const fEase = () => {
      fs += (fTarget - fs) * 0.12;
      if (Math.abs(fTarget - fs) < 0.0005) fs = fTarget;
      ftScene.style.setProperty("--fs", fs.toFixed(4));
      if (fs !== fTarget) requestAnimationFrame(fEase); else fEasing = false;
    };
    const fUpdate = () => {
      fTick = false;
      const r = ftScene.getBoundingClientRect();
      // 0 when the footer's top reaches the bottom of the screen, 1 at the very end of the page
      const travel = Math.min(r.height, document.documentElement.scrollHeight - innerHeight) || 1;
      fTarget = Math.min(Math.max((innerHeight - r.top) / travel, 0), 1);
      if (!fEasing) { fEasing = true; requestAnimationFrame(fEase); }
    };
    addEventListener("scroll", () => { if (!fTick) { fTick = true; requestAnimationFrame(fUpdate); } }, { passive: true });
    addEventListener("resize", fUpdate);
    fUpdate();
  }

  /* ---------- CD player (Spotify iFrame API) ---------- */
  const stage = $(".cd-stage");
  if (stage) {
    const cd = $(".cd", stage), dock = $(".spotify-dock"), np = $(".now-playing");
    let controller = null, ready = false, playing = false, pendingPlay = false, lastPos = 0;
    const setPlaying = (p) => { playing = p; stage.classList.toggle("is-playing", p); np?.classList.toggle("is-playing", p);
      if (np) np.querySelector("span").textContent = p ? "Now playing" : "Paused, press play on the wheel";
      const st = $(".pod-state", stage); if (st) st.textContent = p ? "▶" : "❚❚"; };
    // music player screen: progress bar and times
    const fmt = (ms) => { const s = Math.max(0, Math.round(ms / 1000)); return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`; };
    const showProgress = (pos, dur) => {
      if (!dur) return;
      const bar = $(".pod-prog i", stage); if (bar) bar.style.width = (pos / dur * 100).toFixed(2) + "%";
      const c = $(".pod-cur", stage), l = $(".pod-left", stage);
      if (c) c.textContent = fmt(pos); if (l) l.textContent = "-" + fmt(dur - pos);
    };
    window.onSpotifyIframeApiReady = (IFrameAPI) => {
      const el = document.createElement("div"); dock.appendChild(el);
      IFrameAPI.createController(el, { uri: `spotify:track:${SITE.spotifyTrack}`, width: "100%", height: 80, theme: "light" }, (ctrl) => {
        controller = ctrl; ready = true;
        ctrl.addListener("playback_update", (e) => { setPlaying(!e.data.isPaused); lastPos = e.data.position; showProgress(e.data.position, e.data.duration); });
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
    // click wheel buttons
    const nowView = $(".pod-now", stage), menuView = $(".pod-menu", stage);
    const showNow = () => { if (nowView && menuView) { nowView.hidden = false; menuView.hidden = true; } };
    $(".pw-play", stage)?.addEventListener("click", () => { showNow(); toggle(); });
    $(".pw-prev", stage)?.addEventListener("click", () => { showNow(); if (ready && controller) controller.seek(0); });
    $(".pw-next", stage)?.addEventListener("click", () => { showNow(); if (ready && controller) controller.seek(Math.round((lastPos + 30000) / 1000)); });
    $(".pw-menu", stage)?.addEventListener("click", () => { if (nowView && menuView) { const m = menuView.hidden; menuView.hidden = !m; nowView.hidden = m; } });
    stage.querySelectorAll(".pw, .pod-center").forEach((btn) => btn.addEventListener("pointerdown", () => {
      const w = $(".pod-wheel", stage); w.classList.remove("tick"); void w.offsetWidth; w.classList.add("tick"); }));
  }

  /* ---------- Visual journey: click a tile to open it in the glass preview ---------- */
  const vj = $(".vj-modal");
  if (vj) {
    const tiles = $$(".shot--img:not([aria-hidden])");
    const img = $(".vj-img", vj), cap = $(".vj-cap", vj);
    let at = 0, opener = null;
    const show = (i) => {
      at = (i + tiles.length) % tiles.length;
      const src = $("img", tiles[at]);
      img.src = src.currentSrc || src.src; img.alt = src.alt; cap.textContent = src.alt;
    };
    $$(".shot--img").forEach((t) => t.addEventListener("click", () => {
      opener = t;
      show(tiles.findIndex((x) => x.dataset.vj === t.dataset.vj));
      vj.showModal(); document.documentElement.classList.add("modal-open");
    }));
    $(".vj-prev", vj).addEventListener("click", () => show(at - 1));
    $(".vj-next", vj).addEventListener("click", () => show(at + 1));
    $(".vj-close", vj).addEventListener("click", () => vj.close());
    vj.addEventListener("click", (e) => { if (e.target === vj) vj.close(); }); // click outside the glass
    vj.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") show(at - 1);
      if (e.key === "ArrowRight") show(at + 1);
    });
    vj.addEventListener("close", () => {
      document.documentElement.classList.remove("modal-open");
      // the looping copy can't take focus, so return focus to the matching real tile
      const back = opener && opener.hasAttribute("aria-hidden") ? tiles.find((x) => x.dataset.vj === opener.dataset.vj) : opener;
      if (back) back.focus({ preventScroll: true });
    });
  }

  /* ---------- Book a call: any "Book a call" button opens the Cal.com calendar in a pop-up ---------- */
  const calModal = $(".cal-modal");
  if (calModal && SITE.calLink) {
    const body = $(".cal-body", calModal);
    const openCal = (e) => {
      e.preventDefault();
      if (!body.firstChild) body.innerHTML = `<iframe src="https://cal.com/${SITE.calLink}?embed=true&theme=light&layout=month_view" title="Book a call with Rajvi"></iframe>`;
      calModal.showModal(); document.documentElement.classList.add("modal-open");
    };
    $$("[data-cal]").forEach((a) => a.addEventListener("click", openCal));
    const closeCal = () => calModal.close();
    $(".cal-close", calModal).addEventListener("click", closeCal);
    calModal.addEventListener("click", (e) => { if (e.target === calModal) closeCal(); }); // click outside the window
    calModal.addEventListener("close", () => document.documentElement.classList.remove("modal-open"));
  } else if (SITE.calLink) {
    // pages without the pop-up: go straight to the booking page
    $$("[data-cal]").forEach((a) => { a.href = `https://cal.com/${SITE.calLink}`; a.target = "_blank"; a.rel = "noopener"; });
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

  /* ---------- Typing effect: the footer's "Let's …" and the About / AI Lab sky lines ---------- */
  if (!reduce) $$("[data-type]").forEach((typeEl) => {
    const words = typeEl.dataset.type.split("|"); let w = 0, i = words[0].length, del = true;
    const tick = () => {
      if (del) { i--; if (i <= 0) { del = false; w = (w + 1) % words.length; } }
      else { i++; if (i >= words[w].length) { del = true; typeEl.textContent = words[w]; return setTimeout(tick, 1800); } }
      typeEl.textContent = words[w].slice(0, Math.max(i, 0));
      setTimeout(tick, del ? 45 : 85);
    };
    setTimeout(tick, 1800);
  });

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
    { title: "My toolkit, AI included.", text: "AI is my thinking partner. I use Claude to pressure-test flows, write UX copy and build faster, getting from idea to prototype sooner. The decisions stay mine.",
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
  /* ---- drag stickers around the table; they drift home 20 seconds after the last move, or when the page scrolls ---- */
  const HOME_AFTER = 20 * 1000;
  let scrollFrom = null;
  addEventListener("scroll", () => {
    if (scrollFrom === null || Math.abs(scrollY - scrollFrom) < 40) return; // a small nudge doesn't count
    scrollFrom = null; clearTimeout(homeTimer); goHome();
  }, { passive: true });
  let homeTimer = 0, topZ = 10, justDragged = false;
  const goHome = () => obs.forEach((o) => {
    if (!o.style.getPropertyValue("--dx")) return;
    o.classList.add("homing"); o.style.removeProperty("--dx"); o.style.removeProperty("--dy");
    setTimeout(() => { o.classList.remove("homing"); o.style.zIndex = ""; }, 1500);
  });
  const startDrag = (o, x0, y0) => {
    const g = gt.getBoundingClientRect(), cqw = g.width / 100;
    const sx = parseFloat(o.style.getPropertyValue("--dx")) || 0, sy = parseFloat(o.style.getPropertyValue("--dy")) || 0;
    const r = o.getBoundingClientRect(), cx = r.left + r.width / 2 - sx * cqw, cy = r.top + r.height / 2 - sy * cqw;
    o.classList.remove("homing"); o.classList.add("dragging"); o.style.zIndex = ++topZ;
    clearTimeout(homeTimer); scrollFrom = null;
    return {
      move(x, y) {
        // keep the sticker's centre on the table
        const nx = Math.min(g.right - 10, Math.max(g.left + 10, cx + sx * cqw + x - x0));
        const ny = Math.min(g.bottom - 10, Math.max(g.top + 10, cy + sy * cqw + y - y0));
        o.style.setProperty("--dx", ((nx - cx) / cqw).toFixed(2)); o.style.setProperty("--dy", ((ny - cy) / cqw).toFixed(2));
      },
      end() { o.classList.remove("dragging"); scrollFrom = scrollY; homeTimer = setTimeout(() => { scrollFrom = null; goHome(); }, HOME_AFTER); },
    };
  };
  obs.forEach((o) => {
    // mouse / pen: drag straight away
    o.addEventListener("pointerdown", (e) => {
      if (e.pointerType === "touch" || e.button !== 0 || e.target.closest(".tool")) return;
      const x0 = e.clientX, y0 = e.clientY; let d = null;
      const mv = (ev) => {
        if (!d && Math.hypot(ev.clientX - x0, ev.clientY - y0) < 5) return;
        if (!d) d = startDrag(o, x0, y0);
        d.move(ev.clientX, ev.clientY);
      };
      const up = () => { removeEventListener("pointermove", mv); removeEventListener("pointerup", up);
        if (d) { d.end(); justDragged = true; setTimeout(() => (justDragged = false), 0); } };
      addEventListener("pointermove", mv); addEventListener("pointerup", up);
      e.preventDefault();
    });
    // touch: press and hold briefly, then drag (a normal swipe still scrolls the page)
    o.addEventListener("touchstart", (e) => {
      if (e.touches.length > 1 || e.target.closest(".tool")) return;
      const t = e.touches[0], x0 = t.clientX, y0 = t.clientY; let d = null, cancelled = false;
      const hold = setTimeout(() => { if (!cancelled) { d = startDrag(o, x0, y0); navigator.vibrate?.(8); } }, 280);
      const mv = (ev) => {
        const p = ev.touches[0];
        if (d) { ev.preventDefault(); d.move(p.clientX, p.clientY); }
        else if (Math.hypot(p.clientX - x0, p.clientY - y0) > 8) { cancelled = true; clearTimeout(hold); }
      };
      const end = (ev) => { clearTimeout(hold); o.removeEventListener("touchmove", mv); o.removeEventListener("touchend", end); o.removeEventListener("touchcancel", end);
        if (d) { d.end(); if (ev.cancelable) ev.preventDefault(); justDragged = true; setTimeout(() => (justDragged = false), 50); } };
      o.addEventListener("touchmove", mv, { passive: false }); o.addEventListener("touchend", end); o.addEventListener("touchcancel", end);
    }, { passive: true });
    o.addEventListener("contextmenu", (e) => e.preventDefault());
    // a drag is not a click
    o.addEventListener("click", (e) => { if (justDragged) { e.stopImmediatePropagation(); e.preventDefault(); } }, true);
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
    const rows = [4, 4], dx = ts * 1.42, dy = ts * 1.22, baseY = -w * .34 - ts * .45; popY = -w * .25;
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
