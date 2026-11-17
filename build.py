"""Generates the static pages of the portfolio.

Edit text in content.py, then run:  python3 build.py
(Or edit the generated .html files directly — both are fine.)
"""
from pathlib import Path
from html import escape
import content as C

ROOT = Path(__file__).parent
import hashlib
ASSET_V = hashlib.md5((ROOT / "assets/css/style.css").read_bytes() + (ROOT / "assets/css/dark.css").read_bytes() + (ROOT / "assets/js/main.js").read_bytes()).hexdigest()[:8]

ARROW = '<svg class="arr" width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_UR = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M4 10 10 4M5 4h5v5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
IMG_ICON = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="4" stroke="currentColor" stroke-width="1.6"/><circle cx="9" cy="10" r="2" stroke="currentColor" stroke-width="1.6"/><path d="m4 18 5-5 4 4 2-2 5 5" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>'
SPARK = '<svg viewBox="0 0 10 10"><path d="M5 0 6 4 10 5 6 6 5 10 4 6 0 5 4 4Z" fill="currentColor"/></svg>'


def head(title, desc, root):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta name="theme-color" content="#fdfcff">
<link rel="icon" type="image/svg+xml" href="{root}assets/img/avatar.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<!-- fonts load in the background, so the page can draw straight away (system fonts show for a moment) -->
<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400..700;1,400..700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400..700;1,400..700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet"></noscript>
<script>/* home page: start downloading the hero pictures for the current theme straight away, alongside the stylesheet */
try {{ if (/^\/(index(\.html)?)?$/.test(location.pathname)) {{ var d = localStorage.getItem("theme") === "dark", m = "{root}assets/media/";
  [d ? "hero-room.jpg" : "hero-room-day.jpg", d ? "hero-room-mask.png" : "hero-room-day-mask.png", d ? "hero-view.jpg" : "hero-view-day.jpg"].forEach(function (f) {{
    var l = document.createElement("link"); l.rel = "preload"; l.as = "image"; l.href = m + f; l.fetchPriority = "high"; if (/mask/.test(f)) l.crossOrigin = "anonymous"; /* masks are fetched that way */ document.head.appendChild(l); }}); }} }} catch (e) {{}}</script>
<link rel="stylesheet" href="{root}assets/css/style.css?v={ASSET_V}">
<link rel="stylesheet" href="{root}assets/css/dark.css?v={ASSET_V}">
<script>/* dark mode: apply the saved choice before the page draws, so there is no flash */
try {{ if (localStorage.getItem("theme") === "dark") document.documentElement.dataset.theme = "dark"; }} catch (e) {{}}
/* the "just a minute" reveal plays only the first time the home page opens in a visit */
try {{ if (/^\/(index(\.html)?)?$/.test(location.pathname) && !sessionStorage.getItem("revealed")) {{ document.documentElement.classList.add("first-reveal"); sessionStorage.setItem("revealed", "1"); }} }} catch (e) {{}}</script>
</head>
<body>
<div class="page-fade" aria-hidden="true"><div class="pf-skel"><i class="sk-av"></i><i class="sk-nav"></i><div class="sk-hero"><i class="sk-l sk-s"></i><i class="sk-l sk-h"></i><i class="sk-l sk-h sk-h2"></i><i class="sk-l"></i><i class="sk-l"></i><i class="sk-l sk-short"></i><div class="sk-btns"><i></i><i></i></div></div></div><p class="pf-msg"><span class="pf-spark">✦</span> just a minute</p></div>
<div class="ambient" aria-hidden="true"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div></div>
<div class="grain" aria-hidden="true"></div>
"""


def nav(root, active):
    def link(href, label, key, extra=""):
        cls = ""  # no item is highlighted; Projects simply jumps to the work section
        return f'<a href="{root}{href}"{cls}>{label}{extra}</a>'
    return f"""<header class="nav">
  <a class="logo" href="{root}index.html" aria-label="Rajvi Patel — home"><img class="logo-avatar" src="{root}assets/img/avatar.svg" alt="" width="46" height="46"><span class="logo-name">Rajvi <span class="logo-last">Patel</span></span></a>
  <nav class="nav-menu glass" aria-label="Main">
    <div class="nav-links">
      {link("about.html", "About", "about")}
      {link("ai-lab.html", "AI Lab", "ai")}
      {link("index.html#work", "Projects", "work")}
      <a href="{C.LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
      <a class="nav-resume nav-resume--menu" href="{C.RESUME}" target="_blank" rel="noopener">Resume {ARROW_UR}</a>
    </div>
    <span class="nav-divider" aria-hidden="true"></span>
    <div class="theme-switch" role="group" aria-label="Colour theme">
      <span class="ts-thumb" aria-hidden="true"></span>
      <button type="button" class="ts-btn" data-set-theme="light" aria-pressed="true" aria-label="Light theme"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/></svg></button>
      <button type="button" class="ts-btn" data-set-theme="dark" aria-pressed="false" aria-label="Dark theme"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5a8.5 8.5 0 1 0 11 11z"/></svg></button>
    </div>
    <a class="nav-resume" href="{C.RESUME}" target="_blank" rel="noopener">Resume {ARROW_UR}</a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false"><span></span></button>
  </nav>
</header>
"""


def footer(root):
    """Footer scene: the meadow video settles into view as you reach the end of the page, with the typing 'Let's …', Resume + LinkedIn and the copyright line on top."""
    heart = '<svg class="ft-heart" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.6-9.1C.9 8.6 3 5 6.5 5c2 0 3.5 1.1 5.5 3.2C14 6.1 15.5 5 17.5 5 21 5 23.1 8.6 21.6 11.9 19.5 16.4 12 21 12 21Z" fill="currentColor"/></svg>'
    return f"""<footer class="ft ft--scene" id="contact">
  <div class="ft-media" aria-hidden="true">
    <video class="ft-video" src="{root}assets/media/footer-meadow.mp4" muted loop playsinline preload="none" data-autoplay></video>
  </div>
  <div class="ft-in">
    <div class="ft-top">
      <div>
        <p class="ft-title">Let's <span class="ft-type" data-type="connect|collaborate|work together!">connect</span><span class="ft-caret" aria-hidden="true"></span></p>
        <p class="ft-sub">Would love to talk about projects, growth &amp; anything design!</p>
      </div>
      <div class="ft-btns">
        <a class="btn btn--dark magnetic" href="{C.RESUME}" target="_blank" rel="noopener">Resume {ARROW}</a>
        <a class="btn magnetic" href="{C.LINKEDIN}" target="_blank" rel="noopener">LinkedIn {ARROW}</a>
      </div>
    </div>
    <div class="ft-bottom">
      <p>© <span data-year>2026</span> Rajvi Patel</p>
      <p>Built with {heart} &amp; lots of coffee!</p>
    </div>
  </div>
</footer>
<div class="cmt-bar" role="toolbar" aria-label="Comments" aria-orientation="vertical">
  <button type="button" class="cmt-btn cmt-move" aria-pressed="true" aria-label="Browse the page (shortcut V)" data-tip="Browse · V"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M5.5 3.5l13 6.2-5.6 1.7-2.4 5.6z"/></svg></button>
  <button type="button" class="cmt-btn cmt-add" aria-pressed="false" aria-label="Add a comment (shortcut C)" data-tip="Comment · C"><svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M12 3.5a8.5 8.5 0 1 1-4.1 15.95L3.5 20.5l1.05-4.4A8.5 8.5 0 0 1 12 3.5z"/></svg></button>
  <button type="button" class="cmt-btn cmt-eye" aria-pressed="false" aria-label="Show comments on the page" data-tip="Show / hide"><svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="2.8"/><path class="cmt-slash" d="M4 4l16 16"/></svg></button>
</div>
<div class="cmt-layer cmt-hidden"></div>
<script src="{root}assets/js/main.js?v={ASSET_V}"></script>
</body>
</html>
"""


def desk_items():
    mug = """<svg viewBox="0 0 170 180"><g class="steam" fill="none" stroke="#c9bcf5" stroke-width="4" stroke-linecap="round">
<path d="M52 44c-8-10 8-16 0-28"/><path d="M74 40c-8-10 8-16 0-28"/><path d="M96 44c-8-10 8-16 0-28"/></g>
<g class="wiggle"><path d="M128 84c30 0 30 50 0 50" fill="none" stroke="#c4b3ff" stroke-width="13" stroke-linecap="round"/>
<path d="M22 58h112v86c0 14-11 24-24 24H46c-13 0-24-10-24-24Z" fill="url(#mugG)"/>
<ellipse cx="78" cy="58" rx="56" ry="11" fill="#f1ebff"/><ellipse cx="78" cy="59" rx="48" ry="7.5" fill="#9b6a47"/>
<path d="M78 63c-6-6-12-1-8 3l8 6 8-6c4-4-2-9-8-3Z" fill="#f6e3cf"/>
<path d="M64 108c-6-7-15-1-9 6l9 8 9-8c6-7-3-13-9-6Z" fill="#fff" opacity=".85"/>
<text x="78" y="148" text-anchor="middle" font-family="Caveat" font-size="17" fill="#6c58d6">clarity first</text></g>
<defs><linearGradient id="mugG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3d9ff"/><stop offset="1" stop-color="#c8b8ff"/></linearGradient></defs></svg>"""
    bag = """<svg viewBox="0 0 150 210"><g class="wiggle"><path d="M28 30h94l8 168c0 6-4 10-10 10H30c-6 0-10-4-10-10Z" fill="url(#bagG)"/>
<path d="M28 8h94v26H28Z" fill="#ead9b0"/><path d="M28 18h94M28 26h94" stroke="#dcc796" stroke-width="2"/>
<rect x="36" y="76" width="78" height="92" rx="12" fill="#ece5ff"/>
<text x="75" y="106" text-anchor="middle" font-family="Caveat" font-size="22" fill="#4b3fa0" font-weight="600">raji roast</text>
<text x="75" y="124" text-anchor="middle" font-family="DM Sans" font-size="8.5" letter-spacing="1.6" fill="#7a74a0">CLARITY BLEND</text>
<g transform="translate(75 146) rotate(-25)"><ellipse rx="11" ry="7.5" fill="#8a5a3c"/><path d="M-9 0c5-3 13 3 18 0" stroke="#5e3a24" stroke-width="1.6" fill="none"/></g>
<circle cx="118" cy="54" r="12" fill="#f3d16f"/><text x="118" y="58" text-anchor="middle" font-family="Caveat" font-size="12" fill="#7a5a10">new!</text></g>
<defs><linearGradient id="bagG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbefd2"/><stop offset="1" stop-color="#f1dca6"/></linearGradient></defs></svg>"""
    journal = """<svg viewBox="0 0 200 240"><g class="wiggle"><rect x="26" y="10" width="164" height="222" rx="10" fill="#fff" />
<rect x="18" y="6" width="166" height="224" rx="12" fill="url(#jG)"/><rect x="18" y="6" width="20" height="224" rx="10" fill="#a996f4"/>
<rect x="150" y="6" width="9" height="224" fill="#6c58d6" opacity=".85"/>
<circle cx="96" cy="88" r="38" fill="#fff3cc"/><text x="96" y="84" text-anchor="middle" font-family="Caveat" font-size="19" fill="#7a5a10">ship it</text>
<text x="96" y="104" text-anchor="middle" font-family="Caveat" font-size="19" fill="#7a5a10">softly ♡</text>
<path d="M78 162l6 13 14 2-10 10 3 14-13-7-13 7 3-14-10-10 14-2Z" fill="#fff" opacity=".9"/>
<rect x="100" y="168" width="40" height="18" rx="9" fill="#ffe3ec"/><text x="120" y="181" text-anchor="middle" font-family="DM Sans" font-size="9" font-weight="600" fill="#b0567a">UX ♡</text></g>
<defs><linearGradient id="jG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d9ceff"/><stop offset="1" stop-color="#bfaefc"/></linearGradient></defs></svg>"""
    note = """<svg viewBox="0 0 120 120"><g class="wiggle"><path d="M8 8h104v92l-14 12H8Z" fill="#ffe9a6"/><path d="M98 112v-12h14Z" fill="#f3d16f"/>
<text x="16" y="36" font-family="Caveat" font-size="18" fill="#6a5418">todo:</text>
<text x="16" y="60" font-family="Caveat" font-size="17" fill="#6a5418">✓ make it easy</text>
<text x="16" y="82" font-family="Caveat" font-size="17" fill="#6a5418">✓ more coffee</text></g></svg>"""
    pencil = """<svg viewBox="0 0 200 30"><g class="wiggle"><rect x="20" y="6" width="150" height="18" rx="4" fill="#cfc2ff"/><rect x="20" y="6" width="150" height="6" rx="3" fill="#e4dcff"/>
<path d="M170 6l24 9-24 9Z" fill="#f6e3cf"/><path d="M188 13l6 2-6 2Z" fill="#231e35"/><rect x="4" y="6" width="18" height="18" rx="5" fill="#ffc7d8"/><rect x="18" y="6" width="6" height="18" fill="#c9c3d9"/></g></svg>"""
    star = """<svg viewBox="0 0 80 80"><g class="wiggle"><path d="M40 6l9 20 22 3-16 15 4 22-19-10-19 10 4-22L9 29l22-3Z" fill="#f3d16f" stroke="#fff" stroke-width="5" stroke-linejoin="round"/></g></svg>"""
    heart = """<svg viewBox="0 0 80 72"><g class="wiggle"><path d="M40 66 10 38C-2 26 6 6 22 6c8 0 14 5 18 11 4-6 10-11 18-11 16 0 24 20 12 32Z" fill="#ffc7d8" stroke="#fff" stroke-width="5"/></g></svg>"""
    smiley = """<svg viewBox="0 0 80 80"><g class="wiggle"><circle cx="40" cy="40" r="34" fill="#cfc2ff" stroke="#fff" stroke-width="5"/><circle cx="29" cy="34" r="4" fill="#231e35"/><circle cx="51" cy="34" r="4" fill="#231e35"/><path d="M27 48c7 9 19 9 26 0" stroke="#231e35" stroke-width="4" fill="none" stroke-linecap="round"/></g></svg>"""
    bean = """<svg viewBox="0 0 30 22"><ellipse cx="15" cy="11" rx="13" ry="9" fill="#8a5a3c"/><path d="M4 11c6-4 16 4 22 0" stroke="#5e3a24" stroke-width="2" fill="none"/></svg>"""
    items = [
        (mug, 150, "6%", 64, -4), (journal, 170, "22%", 34, -9), (pencil, 170, "36%", 22, -12),
        (bag, 128, "50%", 48, 6), (note, 110, "66%", 120, 8), (star, 64, "80%", 66, 12),
        (heart, 58, "18%", 214, -14), (smiley, 60, "62%", 28, -6), (star, 44, "90%", 190, -18),
        (bean, 26, "46%", 30, 30), (bean, 22, "48%", 18, -20), (bean, 24, "76%", 30, 60),
    ]
    out = []
    for svg, w, left, bottom, rot in items:
        out.append(f'<div class="desk-item" style="--w:{w};left:{left};bottom:{bottom + 56}px" data-rot="{rot}">{svg}</div>')
    return "\n    ".join(out)


def img_ph(label="Image coming soon", ratio="16/9", extra_cls=""):
    return f'<div class="img-ph {extra_cls}" style="aspect-ratio:{ratio}"><div class="ph-in">{IMG_ICON}<b>{escape(label)}</b><span>drop your image here</span></div></div>'


# ---------------------------------------------------------------- scenes
CARD_ART = {"sila": ("scene--lav", "sila.png", "SILA app: verify-identity home screen and the send-money screen"),
            "kiosk": ("scene--butter", "citylockers.png", "CityLockers kiosk welcome screen"),
            "sku": ("scene--mix", "sku.png", "SKU Platform product catalogue on a tablet")}


def card_art(kind):
    """Home page card picture (same images as the Framer site), on the card's soft coloured panel."""
    bg, img, alt = CARD_ART[kind]
    return f'<div class="scene {bg}"><img class="card-img" src="assets/media/cards/{img}" alt="{alt}" loading="lazy" decoding="async"></div>'


def scene(kind):
    if kind == "sila":
        return f"""<div class="scene scene--lav">
  <div class="phone"><div class="phone-screen">
    <span class="ui-small">YOU SEND</span><span class="ui-big">1,000 AED</span>
    <div class="ui-line w80"></div>
    <span class="ui-small">THEY RECEIVE</span><span class="ui-big" style="color:var(--lav-deep)">₹<span data-count="25809">25,809</span></span>
    <div class="track"><i></i><i></i><i></i></div><div class="ui-line w60"></div><div class="ui-line w40"></div>
    <div class="ui-btn"></div>
  </div></div>
  <div class="toast" style="right:9%;top:22%"><span class="tick">✓</span>Delivered in 14 min</div>
  <div class="float-tag" style="left:8%;top:18%">No hidden fees</div>
  <span class="s-label">▶ add flow video</span></div>"""
    if kind == "kiosk":
        cells = "".join(f'<i class="{c}"></i>' for c in ["", "t", "", "", "t", "", "sel", "t", "", "", "t", "", "t", "", "", ""])
        return f"""<div class="scene scene--butter">
  <div class="kiosk"><span class="ui-small">SELECT YOUR LOCKER</span><div class="ui-line w60"></div>
    <div class="lockers">{cells}</div><div class="ui-btn"></div></div>
  <div class="toast" style="right:8%;top:24%"><span class="tick">✓</span>Locker B2 is open</div>
  <div class="float-tag" style="left:7%;top:20%;animation-delay:-2s">&lt; 4 min booking</div>
  <span class="s-label">▶ add kiosk video</span></div>"""
    prods = "".join('<div class="prod"><div class="ui-line w60"></div></div>' for _ in range(8))
    return f"""<div class="scene scene--mix">
  <div class="browser"><div class="browser-bar"><i></i><i></i><i></i></div>
    <div class="browser-body"><div class="browser-side"><div class="ui-line"></div><div class="ui-line w60"></div><div class="ui-line w80"></div><div class="ui-line w40"></div><div class="ui-line w60"></div></div>
    <div class="browser-main"><div class="bars"><i style="height:40%"></i><i style="height:65%"></i><i style="height:50%"></i><i style="height:80%"></i><i style="height:60%"></i><i style="height:95%"></i><i style="height:70%"></i></div>
    <div class="prod-grid">{prods}</div></div></div></div>
  <div class="toast" style="right:6%;top:16%"><span class="tick">✓</span>Added to your Shopify store</div>
  <span class="s-label">▶ add platform video</span></div>"""


# ---------------------------------------------------------------- home
# ---------------------------------------------------------------- what I bring to the table
AI_ICONS = {
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/>',
    "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path class="ai-ln" d="M9 13h6"/><path class="ai-ln ai-ln2" d="M9 17h4"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>',
    "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle class="ai-sun" cx="9" cy="10" r="1.8"/><path d="m21 16-5-5-9 9"/>',
    "loop": '<path d="M20 11a8 8 0 0 0-14.3-4.9L4 8"/><path d="M4 3v5h5"/><path d="M4 13a8 8 0 0 0 14.3 4.9L20 16"/><path d="M20 21v-5h-5"/>',
    "rocket": '<path d="M5 15c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.9A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22.4 22.4 0 0 1-4 2z"/><path d="M9 12H4s.6-3 2-4c1.6-1.1 5 0 5 0M12 15v5s3-.6 4-2c1.1-1.6 0-5 0-5"/>',
}


def ai_flow():
    """Home: an interactive flowchart of how I use AI, from research to delivery. Click a step to see its tools."""
    def icon(k):
        return f'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><g class="ai-i ai-{k}">{AI_ICONS[k]}</g></svg>'
    tabs, panels = [], []
    for i, f in enumerate(C.AI_FLOW):
        on = i == 0
        tabs.append(f'''<button type="button" class="af-step" role="tab" id="af-tab-{i}" aria-controls="af-panel-{i}" aria-selected="{str(on).lower()}" tabindex="{0 if on else -1}" style="--i:{i}">
      <span class="af-dot">{icon(f["icon"])}</span><span class="af-num">0{i + 1}</span><span class="af-name">{escape(f["step"])}</span>
    </button>''')
        tools = "".join(f'<li>{escape(x)}</li>' for x in f["tools"])
        panels.append(f'''<div class="af-panel" role="tabpanel" id="af-panel-{i}" aria-labelledby="af-tab-{i}" tabindex="0"{"" if on else " hidden"}>
      <div class="af-copy"><span class="hand">step 0{i + 1} · {escape(f["step"].lower())}</span><h3>{escape(f["title"])}</h3><p>{escape(f["text"])}</p></div>
      <div class="af-side"><p class="af-label">Tools</p><ul class="af-tools">{tools}</ul>
        <p class="af-label">What comes out</p><p class="af-out">{escape(f["out"])}</p></div>
    </div>''')
    return f'''<section class="af" aria-labelledby="af-title">
  <div class="wrap">
    <div class="bring-head af-head" data-reveal><span class="hand">{escape(C.AI_FLOW_NOTE)}</span><h2 id="af-title">{escape(C.AI_FLOW_TITLE)}</h2></div>
    <div class="af-chart" data-reveal>
      <div class="af-track" role="tablist" aria-label="AI workflow steps">
        <span class="af-line" aria-hidden="true"><i></i></span>
        {"".join(tabs)}
      </div>
      <p class="af-hint" aria-hidden="true">tap a step ✦</p>
      <div class="af-card glass">{"".join(panels)}</div>
    </div>
    <p class="af-end" data-reveal>{escape(C.AI_FLOW_END)}</p>
  </div>
</section>'''


def bring():
    P = ROOT / "partials"
    diary = (P / "diary.html").read_text()
    sticky = (P / "sticky.svg").read_text()
    dental = (P / "dental.svg").read_text()
    def ob(k, cls, x, y, w, r, dl, title, art):
        return f"""<div class="ob {cls}" data-k="{k}" tabindex="0" role="button" aria-label="{escape(title)}" style="--x:{x}%;--y:{y}%;--w:{w}%;--r:{r}deg;--dl:{dl}s">
  <span class="cloud">{escape(title)}<small>click to read more</small></span>
  <span class="ob-float"><span class="ob-art">{art}</span></span>
</div>"""
    box_art = """<span class="box-nudge" style="position:absolute;inset:0">
      <svg class="layer interior" viewBox="0 0 880 728" aria-hidden="true">
        <defs><linearGradient id="inG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bdb2a3"/><stop offset="1" stop-color="#e6ddcf"/></linearGradient>
        <radialGradient id="litG" cx=".5" cy=".55" r=".6"><stop offset="0" stop-color="#fffaf0"/><stop offset=".5" stop-color="#fbe8b8"/><stop offset="1" stop-color="#e9d6a8" stop-opacity=".2"/></radialGradient></defs>
        <polygon points="70,322 441,194 806,318 435,446" fill="url(#inG)"/>
        <polygon points="70,322 441,194 806,318 790,330 441,214 88,332" fill="#a99d8d" opacity=".55"/>
        <polygon class="lit" points="70,322 441,194 806,318 435,446" fill="url(#litG)"/>
        <polyline points="70,322 435,446 806,318" fill="none" stroke="#fff" stroke-width="10" stroke-linejoin="round"/>
      </svg>
      <img class="layer base" src="assets/media/box-base.png" loading="lazy" decoding="async" alt="">
      <img class="layer lid" src="assets/media/box-lid.png" loading="lazy" decoding="async" alt="">
      <span class="beam" aria-hidden="true"></span>
      <span class="sparks" aria-hidden="true"></span>
      <span class="tools"></span>
    </span>"""
    objs = [
        ob(0, "o-diary", 21, 30, 29, -3, 0, "I ask why before how",
           f'<img src="assets/media/diary-sticker.png" loading="lazy" decoding="async" alt="Open diary: questions before designing a SaaS dashboard, and a pencil wireframe"><span class="photo">{diary}</span>'),
        ob(5, "o-dental", 80, 73, 19, 3, -2.5, "I design with a clinician's care",
           f'<img src="assets/media/dental-sticker.png" loading="lazy" decoding="async" alt="Lab coat with dental tools, a tooth model and an x-ray"><span class="photo">{dental}</span>'),
        ob(1, "o-sticky", 80, 29, 26, 4, -1.2, "I think in systems",
           f'<img src="assets/media/sticky-sticker.png" loading="lazy" decoding="async" alt="Sticky notes mapping a product flow"><span class="photo">{sticky}</span>'),
        ob(2, "o-mac", 20, 74, 21, 6, -3.6, "I like getting my hands dirty",
           '<img src="assets/media/macbook-sticker.png" loading="lazy" decoding="async" alt="Closed MacBook">'),
        ob(4, "o-box", 50, 31, 18, 0, -1.8, "My toolkit, AI included", box_art),
        ob(3, "o-cups", 50.5, 73, 21, -5, -4.4, "I value honest collaboration",
           '<img src="assets/media/cups-sticker.png" loading="lazy" decoding="async" alt="Three coffees and a matcha latte, like a team meeting">'),
    ]
    return f"""<section class="bring" id="bring">
  <div class="bring-head wrap" data-reveal>
    <span class="hand">like literally</span>
    <h2>What I bring to the table</h2>
    <p>Hover to peek, click to read more.</p>
  </div>
  <div class="gt-wrap" data-reveal style="--d:.1s">
    <div class="gt-glow" aria-hidden="true"><i></i><i></i><i></i></div>
    <div class="gt">
      <div class="fx fx-checks" aria-hidden="true"></div><div class="fx fx-glow" aria-hidden="true"></div>
      {''.join(objs)}
      <span class="gt-hint">psst… click on the stickers to know the meaning ✿</span>
    </div>
    <aside class="panel" aria-live="polite">
      <button class="panel-close" aria-label="Close">×</button>
      <div class="swap"><span class="p-num"></span><h3></h3><p class="p-text"></p><div class="p-tools"></div></div>
      <div class="p-proof"><b>From my work</b><span></span></div>
      <div class="p-nav"><button class="p-prev">← prev</button><button class="p-next">next →</button></div>
    </aside>
  </div>
</section>"""

def fireflies(n=15):
    """Warm glowing dots drifting slowly outside the window (between the view and the room layers)."""
    import random
    rnd = random.Random(7)  # same layout on every build
    dots = []
    for _ in range(n):
        x, y = rnd.uniform(6, 94), rnd.uniform(48, 90)
        dots.append(f'<i class="ff" style="--x:{x:.1f}%;--y:{y:.1f}%;--s:{rnd.uniform(4.5, 8):.1f}px;'
                    f'--dx:{rnd.uniform(-70, 70):.0f}px;--dy:{rnd.uniform(18, 60):.0f}px;'
                    f'--dur:{rnd.uniform(9, 17):.1f}s;--glow:{rnd.uniform(2.2, 4.5):.1f}s;--dl:{-rnd.uniform(0, 17):.1f}s"></i>')
    return f'<div class="fireflies" aria-hidden="true">{"".join(dots)}</div>'


def home():
    root = ""
    cards = []
    for i, p in enumerate(C.PROJECTS):
        wide = " card--wide" if p.get("wide") else ""
        tags = "".join(f'<span class="chip">{t}</span>' for t in p["tags"])
        cards.append(f"""<a class="card glass tilt{wide}" href="work/{p['slug']}.html" data-video="{p.get('video','')}" data-reveal style="--d:{i*0.08:.2f}s">
  <div class="card-media">{card_art(p['scene'])}</div>
  <div class="card-body">
    <div class="card-meta">{p['meta']} <span class="badge{' badge--soft' if p['badge']=='MVP' else ''}">{p['badge']}</span></div>
    <h3>{p['name']} <span class="go">{ARROW_UR}</span></h3>
    <p>{p['summary']}</p>
    <div class="tags">{tags}</div>
  </div>
</a>""")
    # visual journey: (file, width, height, alt). Each tile keeps its image's own shape.
    V = {1: ("v1-rose.jpg", 2000, 1442, "SILA transfer tracking screens"), 2: ("v2-rose.jpg", 1964, 2000, "SILA home and send screens"),
         3: ("v3-rose.jpg", 2000, 1442, "SILA onboarding screens"), 4: ("v4-rose.jpg", 1964, 2000, "Arabic chat app with money transfer"),
         5: ("v5.webp", 2000, 1622, "wildfern landing page hero"), 6: ("v6.webp", 2000, 1532, "wildfern programme features"),
         7: ("v7.webp", 2000, 1532, "Novaflux robotics news homepage")}
    def shot(n, copy=False):
        f, w, h, alt = V[n]
        # each tile is a button that opens the glass preview; the second (looping) copy is hidden from screen readers
        extra = ' tabindex="-1" aria-hidden="true"' if copy else f' aria-label="Preview: {alt}"'
        return (f'<button type="button" class="shot shot--img" data-vj="{f}"{extra} style="aspect-ratio:{w}/{h}">'
                f'<img src="assets/media/visuals/{f}" alt="{"" if copy else alt}" loading="lazy" decoding="async"></button>')
    order = [1, 5, 2, 6, 3, 7, 4]  # one row
    shots = "".join(shot(n) for n in order)
    shots_copy = "".join(shot(n, True) for n in order)
    sparkles = "".join(f'<span class="sparkle" style="left:{l}%;top:{t}%;animation-delay:{d}s;width:{s}px;height:{s}px">{SPARK}</span>'
                       for l, t, d, s in [(12, 22, 0, 10), (78, 18, 1.2, 14), (64, 40, 2.1, 8), (30, 58, .6, 12), (88, 62, 1.8, 10), (48, 14, 2.6, 9)])
    body = f"""{nav(root, 'work')}
<main class="home sl-bg">
<section class="hero">
  <div class="hero-media" aria-hidden="true">
    <img class="hero-img hero-view hero-view--day" data-src="assets/media/hero-view-day.jpg" alt="" decoding="async">
    <img class="hero-img hero-view hero-view--night" data-src="assets/media/hero-view.jpg" alt="" decoding="async">
    <script>/* load only the view for the current theme first; the other one loads later (main.js) */
    (function () {{ var i = document.querySelector(document.documentElement.dataset.theme === "dark" ? ".hero-view--night" : ".hero-view--day"); i.fetchPriority = "high"; i.src = i.dataset.src; }})();</script>
    {fireflies()}
    <div class="hero-room"></div>
    {sparkles}
  </div>
  <nav class="ff-links" aria-label="Case studies">
    <a class="ff-link" href="work/sila.html" aria-label="Open the SILA case study" style="--x:57%;--y:63%;--mx:10%;--my:81%;--dur:11s;--dl:-2s"><i></i><span>click on me</span></a>
    <a class="ff-link" href="work/citylockers-kiosk.html" aria-label="Open the CityLockers Kiosk case study" style="--x:68%;--y:46%;--mx:29%;--my:84%;--dur:13s;--dl:-6s"><i></i><span>click on me</span></a>
    <a class="ff-link" href="work/sku-platform.html" aria-label="Open the SKU Platform case study" style="--x:77%;--y:34%;--mx:47%;--my:81%;--dur:12s;--dl:-9s"><i></i><span>click on me</span></a>
  </nav>
  <div class="wrap hero-inner">
    <p class="hero-hi" data-reveal><span>Hi! I’m Rajvi</span><span class="wave" aria-hidden="true">👋</span></p>
    <h1 class="split">{C.HERO_TITLE}</h1>
    <div class="hero-side" data-reveal style="--d:.35s">
      <p>{C.INTRO}</p>
      <div class="hero-cta">
        <a class="btn btn--dark magnetic" href="#work">See my work {ARROW}</a>
        <a class="btn magnetic" href="#call" data-cal>Book a call {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="work">
  <div class="wrap">
    <div class="section-head">
      <div data-reveal><h2>Selected work</h2></div>
      <p data-reveal style="--d:.1s">Fintech, travel tech and B2B commerce. Research-led, shipped with small teams, written up in plain words.</p>
    </div>
    <div class="work-grid">
      {''.join(cards)}
    </div>
  </div>
</section>

{bring()}

{ai_flow()}

<section class="ticker-section" aria-label="Visual journey">
  <div class="ticker-head wrap" data-reveal><span class="hand">a sneak peek of my</span><h2>Visual journey</h2></div>
  <div class="ticker"><div class="ticker-track">{shots}{shots_copy}</div></div>
  <dialog class="vj-modal" aria-label="Image preview">
    <button type="button" class="vj-close" aria-label="Close preview"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    <button type="button" class="vj-nav vj-prev" aria-label="Previous image">&larr;</button>
    <figure class="vj-frame"><img class="vj-img" src="" alt=""><figcaption class="vj-cap"></figcaption></figure>
    <button type="button" class="vj-nav vj-next" aria-label="Next image">&rarr;</button>
  </dialog>
</section>

<section class="cd-section">
  <div class="wrap cd-wrap">
    <div class="cd-copy" data-reveal>
      <span class="hand">before you scroll on…</span>
      <h2>Here's a song for you while you see what I do</h2>
      <p>Press play on the wheel. It's on my repeat list while I design.</p>
      <div class="spotify-dock"></div>
    </div>
    <div class="cd-stage pod-stage" data-reveal style="--d:.15s">
      <div class="pod-rig">
      <svg class="pod-wire" viewBox="-170 100 470 500" aria-hidden="true">
        <defs>
          <path id="pwc1" d="M70 536 C 72 580, 0 592, -50 566 C -112 534, -152 420, -140 296" />
          <ellipse id="pwl1" cx="-78" cy="252" rx="64" ry="50" transform="rotate(-12 -78 252)" />
          <ellipse id="pwl2" cx="-70" cy="246" rx="57" ry="54" transform="rotate(14 -70 246)" />
          <ellipse id="pwl3" cx="-86" cy="258" rx="60" ry="45" transform="rotate(-32 -86 258)" />
          <path id="pwc2" d="M-40 206 C -62 190, -88 186, -104 180" />
          <path id="pwc3" d="M-40 206 C -30 192, -20 178, -12 166" />
        </defs>
        <g class="pw-cords-o"><use href="#pwl3"/><use href="#pwl2"/><use href="#pwl1"/><use href="#pwc1"/><use href="#pwc2"/><use href="#pwc3"/></g>
        <g class="pw-cords"><use href="#pwl3"/><use href="#pwl2"/><use href="#pwl1"/><use href="#pwc1"/><use href="#pwc2"/><use href="#pwc3"/></g>
        <rect class="pw-part" x="-5" y="-8" width="10" height="16" rx="4.5" transform="translate(-40 206) rotate(-30)" />
        <rect class="pw-part" x="-12" y="-4.5" width="24" height="9" rx="4.5" transform="translate(-133 330) rotate(-80)" />
        <g class="pw-pod" transform="translate(-104 180) rotate(-72)"><rect class="pw-stem" x="-5" y="-42" width="10" height="42" rx="5"/><ellipse class="pw-head" cx="7" cy="-52" rx="17" ry="13.5" transform="rotate(-18 7 -52)"/><ellipse class="pw-mesh" cx="12" cy="-55" rx="7.5" ry="4.6" transform="rotate(-18 12 -55)"/><circle class="pw-dot" cx="-3" cy="-48" r="1.6"/><rect class="pw-tip" x="-5" y="-4" width="10" height="4" rx="1.5"/></g>
        <g class="pw-pod" transform="translate(-12 166) rotate(24)"><rect class="pw-stem" x="-5" y="-42" width="10" height="42" rx="5"/><ellipse class="pw-head" cx="7" cy="-52" rx="17" ry="13.5" transform="rotate(-18 7 -52)"/><ellipse class="pw-mesh" cx="12" cy="-55" rx="7.5" ry="4.6" transform="rotate(-18 12 -55)"/><circle class="pw-dot" cx="-3" cy="-48" r="1.6"/><rect class="pw-tip" x="-5" y="-4" width="10" height="4" rx="1.5"/></g>
        <rect class="pw-part" x="66" y="516" width="8" height="22" rx="4" />
        <rect class="pw-plug" x="62" y="492" width="16" height="27" rx="3" />
        <rect class="pw-ring" x="62" y="506" width="16" height="2" />
      </svg>
      <div class="pod">
        <div class="pod-screen">
          <div class="pod-view pod-now">
            <div class="pod-bar"><span class="pod-state">❚❚</span><span>Now Playing</span><i class="pod-batt"></i></div>
            <div class="pod-np">
              <img class="pod-art" src="https://image-cdn-ak.spotifycdn.com/image/ab67616d00001e02dffe8e5a1e7c4eed82fbbfd5" alt="" loading="lazy">
              <div class="pod-meta"><b>Los Angeles</b><span>The Midnight</span><small>Days of Thunder</small></div>
            </div>
            <div class="pod-prog"><i></i></div>
            <div class="pod-time"><span class="pod-cur">0:00</span><span class="pod-left">-6:29</span></div>
          </div>
          <div class="pod-view pod-menu" hidden>
            <div class="pod-bar"><span></span><span>rajvi's pod</span><i class="pod-batt"></i></div>
            <ul><li class="on">Now Playing</li><li>Design Mix</li><li>Focus Songs</li><li>Shuffle Songs</li><li>Settings</li></ul>
          </div>
        </div>
        <div class="pod-wheel" role="group" aria-label="Music controls">
          <button type="button" class="pw pw-menu" aria-label="Menu">MENU</button>
          <button type="button" class="pw pw-prev" aria-label="Back to the start"><svg viewBox="0 0 24 24"><path d="M6 6h2v12H6zM20 6v12l-9-6z"/></svg></button>
          <button type="button" class="pw pw-next" aria-label="Skip ahead 30 seconds"><svg viewBox="0 0 24 24"><path d="M16 6h2v12h-2zM4 6v12l9-6z"/></svg></button>
          <button type="button" class="pw pw-play" aria-label="Play or pause"><svg viewBox="0 0 24 24"><path d="M3 6v12l8-6zM14 6h2.5v12H14zM18.5 6H21v12h-2.5z"/></svg></button>
          <button type="button" class="pod-center cd" aria-label="Play or pause the song"></button>
        </div>
      </div>
      </div>
      <div class="pod-note">
        <svg class="pod-arrow" viewBox="0 0 120 90" aria-hidden="true">
          <path d="M112 78 C 92 80, 62 70, 50 52 C 40 37, 40 22, 30 12" />
          <path d="M20 22 L 30 11 L 40 20" />
        </svg>
        <span>feeling nostalgic eh? ♫</span>
      </div>
    </div>
  </div>
</section>

<section class="section" id="call">
  <div class="wrap">
    <div class="call glass" data-reveal>
      <div>
        <span class="hand">got a project or a role?</span>
        <h2>Let's talk about it</h2>
        <p>Would love to talk about projects, growth &amp; anything design. Pick a time that works for you, it's a relaxed 30-minute chat.</p>
        <div class="call-actions">
          <a class="btn btn--dark magnetic" href="#call" data-cal>Book a call {ARROW}</a>
          <a class="btn magnetic" href="{C.LINKEDIN}" target="_blank" rel="noopener">LinkedIn {ARROW_UR}</a>
        </div>
        <p class="call-mail">or email me at <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
      </div>
    </div>
  </div>
  <dialog class="cal-modal" aria-label="Book a call with Rajvi">
    <button type="button" class="cal-close" aria-label="Close">&times;</button>
    <div class="cal-body"></div>
  </dialog>
</section>
</main>
{footer(root)}"""
    return head("Rajvi Patel · Senior Product Designer", C.META_DESC, root) + body


# ---------------------------------------------------------------- case study
def render_block(b):
    t = b[0]
    if t == "p":
        return f"<p>{b[1]}</p>"
    if t == "h3":
        return f"<h3>{b[1]}</h3>"
    if t == "cards":
        items, cols = b[1], (b[2] if len(b) > 2 else 2)
        numbered = b[3] if len(b) > 3 else True
        cs = "".join(
            f'<div class="c glass" data-reveal style="--d:{(i % cols) * 0.06:.2f}s">'
            + (f'<span class="n">{i+1:02d}</span>' if numbered else "")
            + f'<h4>{h}</h4>' + (f'<p>{d}</p>' if d else "") + "</div>"
            for i, (h, d) in enumerate(items))
        return f'<div class="block g-cards" style="--cols:{cols}">{cs}</div>'
    if t == "stats":
        ss = "".join(
            f'<div class="stat glass" data-reveal style="--d:{i*0.06:.2f}s"><b>{n}</b><span>{l}</span>' + (f"<small>{s}</small>" if s else "") + "</div>"
            for i, (n, l, s) in enumerate(b[1]))
        return f'<div class="block stats">{ss}</div>'
    if t == "img":
        ratio = b[2] if len(b) > 2 else "16/9"
        cap = f'<p class="cap">{b[3]}</p>' if len(b) > 3 else ""
        return f'<div class="block" data-reveal>{img_ph(b[1], ratio)}{cap}</div>'
    if t == "imgs":
        inner = "".join(img_ph(lbl, b[2] if len(b) > 2 else "4/3") for lbl in b[1])
        return f'<div class="block g-cards" style="--cols:{len(b[1]) if len(b[1]) < 4 else 2}" data-reveal>{inner}</div>'
    if t == "two":
        cols = "".join(f'<div class="col glass" data-reveal><h4>{h}</h4><ul>' + "".join(f"<li>{li}</li>" for li in lis) + "</ul></div>" for h, lis in b[1])
        return f'<div class="block two-col">{cols}</div>'
    if t == "list":
        return '<ul class="list block">' + "".join(f"<li>{li}</li>" for li in b[1]) + "</ul>"
    if t == "quote":
        cite = f"<cite>{b[2]}</cite>" if len(b) > 2 else ""
        return f'<blockquote class="quote glass" data-reveal>{b[1]}{cite}</blockquote>'
    if t == "persona":
        p = b[1]
        qs = "".join(f"<span>“{q}”</span>" for q in p.get("quotes", []))
        lis = "".join(f"<li>{x}</li>" for x in p.get("points", []))
        return f"""<div class="block persona glass" data-reveal>{img_ph('persona', '1/1')}
<div><h4>{p['name']}</h4><p class="role">{p['role']}</p><ul class="list">{lis}</ul><div class="qs">{qs}</div></div></div>"""
    raise ValueError(t)


def case_study(cs, nxt):
    root = "../"
    meta = "".join(f'<div class="glass"><small>{k}</small><span>{v}</span></div>' for k, v in cs["meta"])
    stations = "".join(
        f'<li><a href="#{s["id"]}"><span class="node"></span>{s["nav"]}<span class="num">{i+1:02d}</span></a></li>'
        for i, s in enumerate(cs["sections"]))
    secs = []
    for s in cs["sections"]:
        blocks = "".join(render_block(b) for b in s["blocks"])
        secs.append(f"""<section class="cs-sec" id="{s['id']}">
  <span class="eyebrow">{s['eyebrow']}</span>
  <h2 data-reveal>{s['title']}</h2>
  {blocks}
</section>""")
    body = f"""{nav(root, 'work')}
<main>
<section class="cs-hero">
  <div class="wrap">
    <div><a class="back glass" href="../index.html#work"><span class="arr">←</span> All work</a></div>
    <span class="eyebrow" data-reveal>{cs['kicker']}</span>
    <h1 class="split">{cs['title']}</h1>
    <p class="lede" data-reveal style="--d:.3s">{cs['lede']}</p>
    <div class="cs-meta" data-reveal style="--d:.4s">{meta}</div>
    <div class="cs-cover" data-reveal style="--d:.5s">{img_ph('Cover image / video', '16/8')}</div>
  </div>
</section>
<div class="wrap cs-layout">
  <aside class="roadmap glass" aria-label="Case study sections">
    <h4>the roadmap ✿</h4>
    <ol><span class="progress"></span>{stations}</ol>
    <div class="flag">🏁 the finish line</div>
  </aside>
  <div class="cs-content">
    {''.join(secs)}
    <a class="next-cs glass" href="{nxt['slug']}.html">
      <div><small>Next case study</small><h3>{nxt['name']}</h3></div>
      <span class="go">{ARROW_UR}</span>
    </a>
  </div>
</div>
</main>
{footer(root)}"""
    return head(f"{cs['name']} · Rajvi Patel", cs["lede"], root) + body


# ---------------------------------------------------------------- about / AI lab
# Both pages open with a "sky" scene in the footer's lavender-peach palette: drifting clouds,
# fireflies, a typing line and soft pill buttons. The sky melts into the page at the bottom.
def sky_clouds():
    return '<div class="sky-clouds" aria-hidden="true">' + "".join(f'<i class="c{i}"></i>' for i in range(1, 6)) + "</div>"


def sky_btns(primary, secondary):
    return f'<div class="sky-btns">{primary}{secondary}</div>'


def about():
    root = ""
    facts = "".join(f'<span class="sky-chip">{f}</span>' for f in C.ABOUT_FACTS)
    paras = "".join(f"<p>{p}</p>" for p in C.ABOUT_BIO)
    words = "|".join(C.ABOUT_TYPING)
    body = f"""{nav(root, 'about')}
<main>
<section class="sky sky--about">
  {sky_clouds()}
  {fireflies(12)}
  <div class="wrap about-grid">
    <div class="polaroid-wrap" data-reveal>
      <div class="polaroid"><span class="tape"></span>{img_ph('your photo', '4/5')}<span class="caption">that's me! ✿</span></div>
      <span class="sticker" style="right:-24px;top:18%;width:70px">{desk_sticker('star')}</span>
      <span class="sticker" style="left:-26px;bottom:22%;width:60px;animation-delay:-2s">{desk_sticker('heart')}</span>
    </div>
    <div class="about-copy">
      <p class="sky-hi hand" data-reveal>hi, I'm Rajvi, <span class="sky-type" data-type="{words}">{C.ABOUT_TYPING[0]}</span><span class="sky-caret" aria-hidden="true"></span></p>
      <h1 class="split">From dental chairs to <em>design systems.</em></h1>
      <div data-reveal style="--d:.3s">{paras}</div>
      <div class="about-facts" data-reveal style="--d:.4s">{facts}</div>
      <div data-reveal style="--d:.5s">{sky_btns(
          f'<a class="sky-btn sky-btn--dark" href="{C.RESUME}" target="_blank" rel="noopener">Resume {ARROW_UR}</a>',
          f'<a class="sky-btn" href="index.html#call" data-cal>Book a call {ARROW}</a>')}</div>
    </div>
  </div>
</section>
</main>
{footer(root)}"""
    return head("About · Rajvi Patel", "About Rajvi Patel, Senior Product Designer in Dubai.", root) + body


def desk_sticker(kind):
    if kind == "star":
        return '<svg viewBox="0 0 80 80"><path d="M40 6l9 20 22 3-16 15 4 22-19-10-19 10 4-22L9 29l22-3Z" fill="#f3d16f" stroke="#fff" stroke-width="5" stroke-linejoin="round"/></svg>'
    return '<svg viewBox="0 0 80 72"><path d="M40 66 10 38C-2 26 6 6 22 6c8 0 14 5 18 11 4-6 10-11 18-11 16 0 24 20 12 32Z" fill="#ffc7d8" stroke="#fff" stroke-width="5"/></svg>'


# A little "neural network" drawn as a constellation of fireflies. Points are in a 100 x 90 box.
NET_NODES = [(10, 30), (30, 12), (52, 22), (78, 10), (92, 36), (66, 42), (40, 46), (16, 62), (46, 72), (74, 66), (90, 82), (26, 86)]
NET_EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (4, 5), (5, 6), (0, 6), (1, 6), (6, 7), (6, 8), (7, 8), (8, 9), (5, 9), (9, 10), (8, 11), (7, 11), (4, 9)]
NET_TAGS = {1: ("above", "prompt experiments"), 4: ("above", "tiny AI tools"), 7: ("below", "prototypes built with Claude"), 9: ("below", "notes on designing for AI")}


def ai_net():
    lines, pulses = [], []
    for k, (a, b) in enumerate(NET_EDGES):
        (x1, y1), (x2, y2) = NET_NODES[a], NET_NODES[b]
        xy = f'x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"'
        lines.append(f'<line class="ln" {xy} style="--i:{k}"/>')
        pulses.append(f'<line class="pulse" {xy} pathLength="100" style="--dl:{-(k * 0.83) % 6:.2f}s"/>')
    nodes = []
    for k, (x, y) in enumerate(NET_NODES):
        pos = f"--x:{x}%;--y:{y / 90 * 100:.2f}%"
        big = k in NET_TAGS
        nodes.append(f'<i class="nd{" nd--big" if big else ""}" style="{pos};--dl:{-(k * 0.7):.1f}s"></i>')
        if big:
            side, label = NET_TAGS[k]
            edge = " nd-tag--l" if x < 25 else " nd-tag--r" if x > 75 else ""  # near an edge: grow inwards so it never runs off
            nodes.append(f'<span class="nd-tag nd-tag--{side}{edge}" style="{pos};--dl:{-(k * 0.9):.1f}s">{label}</span>')
    return f"""<div class="net" data-reveal style="--d:.3s" aria-hidden="true">
      <svg viewBox="0 0 100 90">{"".join(lines)}{"".join(pulses)}</svg>
      {"".join(nodes)}
    </div>"""


def lab_experiments():
    out = []
    for e in C.LAB_EXPERIMENTS:
        steps = "".join(f"<li>{x}</li>" for x in e["steps"])
        tags = "".join(f'<span class="sky-chip">{x}</span>' for x in e["tags"])
        href, label = e["link"]
        out.append(f"""<article class="lab-exp">
    <div class="lab-copy" data-reveal>
      <span class="lab-num hand">experiment {e['num']}</span>
      <h2>{e['title']}</h2>
      <p>{e['text']}</p>
      <p class="lab-try">Try it</p>
      <ol class="lab-steps">{steps}</ol>
      <div class="lab-tags">{tags}</div>
      <a class="sky-btn" href="{href}">{label} {ARROW}</a>
    </div>
    <div class="lab-stage" data-reveal style="--d:.15s">
      <iframe src="{e['src']}" title="{e['title']}: interactive prototype" loading="lazy" scrolling="no" allow="accelerometer; gyroscope"></iframe>
    </div>
  </article>""")
    return f"""<section class="lab" id="experiments">
  <div class="wrap">
    <div class="lab-head" data-reveal><h2>Experiments</h2></div>
    {"".join(out)}
  </div>
</section>"""


def ai_lab():
    root = ""
    body = f"""{nav(root, 'ai')}
<main>
<section class="sky sky--lab">
  {sky_clouds()}
  {fireflies(12)}
  <div class="wrap sky-grid">
    <div class="sky-copy">
      <p class="sky-hi hand" data-reveal>everything I make for fun ✿</p>
      <h1 class="sky-title" data-reveal style="--d:.1s">AI Lab is<br><span class="sky-type" data-type="brewing|prototyping|learning|almost here">brewing</span><span class="sky-caret" aria-hidden="true"></span></h1>
      <p class="sky-lede" data-reveal style="--d:.2s">{C.AI_LAB_TEXT}</p>
      <div data-reveal style="--d:.4s">{sky_btns(
          f'<a class="sky-btn sky-btn--dark" href="index.html#work">Meanwhile, see my work {ARROW}</a>',
          f'<a class="sky-btn" href="index.html#call" data-cal>Book a call</a>')}</div>
    </div>
    {ai_net()}
  </div>
</section>
{lab_experiments()}
</main>
{footer(root)}"""
    return head("AI Lab · Rajvi Patel", "AI experiments by Rajvi Patel: prompt play, tiny tools and prototypes. Coming soon.", root) + body


# ---------------------------------------------------------------- SILA (matches the Framer case study)
SL_ICON = '<svg class="sl-ic" viewBox="0 0 28 28" aria-hidden="true"><path d="M14 5.3 17.6 8.9 14 12.5 10.4 8.9ZM19.1 10.4 22.7 14 19.1 17.6 15.5 14ZM8.9 10.4 12.5 14 8.9 17.6 5.3 14ZM14 15.5 17.6 19.1 14 22.7 10.4 19.1Z" fill="currentColor"/></svg>'
SL_UP = '<svg viewBox="0 0 28 28" aria-hidden="true"><path d="M14 23V5M6 13l8-8 8 8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SL_DOWN = '<svg viewBox="0 0 28 28" aria-hidden="true"><path d="M14 5v18M6 15l8 8 8-8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
M = "../assets/media/sila/"


def sl_points(items, dark=False):
    """Purple icon + title + description rows (used in flows, tier 2, edge case, learnings)."""
    return '<ul class="sl-points">' + "".join(
        f'<li>{SL_ICON}<div><h4>{t}</h4><p>{d}</p></div></li>' for t, d in items) + "</ul>"


# Each recording has white square corners around the phone; clip it to the phone's own rounded outline.
# (top, side, bottom inset %, corner radius % of width / % of height) — measured from each video.
SL_CLIPS = {
    "flow-onboarding.mp4": (0.40, 1.20, 0.40, 18.1, 8.8),
    "flow-kyc.mp4":        (0.40, 1.35, 0.40, 18.6, 9.0),
    "flow-send.mp4":       (0.40, 1.40, 0.50, 18.4, 8.9),
    "tier2.mp4":           (0.50, 1.60, 0.30, 17.9, 8.7),
    "rejected.mp4":        (0.50, 1.60, 0.60, 19.0, 9.2),
}


def sl_video(src, label, round_=False):
    t, sd, b, rx, ry = SL_CLIPS.get(src, (0.5, 1.5, 0.5, 18, 9))
    clip = f"clip-path: inset({t}% {sd}% {b}% {sd}% round {rx}% / {ry}%)"
    return f'<video class="sl-phone" style="{clip}" src="{M}{src}" muted loop playsinline preload="none" data-autoplay aria-label="{label}"></video>'


def sl_numcards(items, cls="sl-card"):
    return "".join(f'<div class="{cls}" data-reveal><span class="sl-num">{i+1}.</span><h4>{t}</h4><p>{d}</p></div>'
                   for i, (t, d) in enumerate(items))


def sila_page():
    root = "../"
    secs = [("context", "The context"), ("problem", "The problem"), ("research", "Research"),
            ("discovery", "Discovery"), ("persona", "User persona"), ("constraints", "Constraints & KYC"),
            ("decisions", "Key decisions"), ("flow", "User flow"), ("tier2", "Tier 2"),
            ("edge", "Edge case"), ("impact", "Projected impact"), ("retention", "Retention"),
            ("learnings", "Learnings")]
    stations = "".join(f'<li><a href="#{i}"><span class="node"></span>{n}</a></li>' for i, n in secs)

    users = [("Surprise fees", '"zero fees" apps hide the margin in the rate; less lands than expected'),
             ("A wall before value", "ID and income asked in onboarding before even user experience the app"),
             ("Unexplained holds", "No reason, no document named, no timeline clarified"),
             ("Silence after sending", 'Money enters a black box; "did it arrive?"')]
    biz = [("Drop-off at the door", "Front-loaded KYC is the funnel's biggest leak"),
           ("Increased support tickets", '"Where is my money" is the top support cost'),
           ("Rejections lose users", 'Vague "verification failed" means retry blind, then uninstall'),
           ("Bad UX is compliance risk", "confusing forms produce wrong answers and flagged accounts")]
    notes = ["KYC acted as a wall, everything asked upfront, causing drop-off",
             'Rates change mid-transaction &amp; "Free" hides fees, cost shows up after sending',
             "Transfers held for days, without clarifying reason, no timeline",
             "Support goes silent when money is stuck",
             "Verification feels endless, rules change every time"]
    peach = [("Identity must be verified", "No anonymous accounts. ID, date of birth and address are legally required."),
             ("Every user is screened", "Sanctions and PEP checks run before onboarding completes."),
             ("Consent is explicit", "The selfie is biometric data, it needs its own agreement, not a buried checkbox.")]
    yellow = [("Purpose must be recorded", "A required question on every transfer, not optional data."),
              ("Declared plans set the baseline", 'Monthly sending plans are what the system measures "unusual" against.'),
              ("Thresholds trigger proofs", "Above set limits, source-of-funds evidence is mandatory. No design can skip it.")]
    decisions = [('"They receive ₹25,809" is the biggest number on screen',
                  "Users think in what lands at home, not exchange rates. It even rides on the CTA."),
                 ("Signup asks for 3 things<br>Email, Phone &amp; MPIN", "KYC when Arjun is motivated, not at the door"),
                 ("MPIN, OTP, UPI name-check patterns Arjun already knows",
                  "His money habits come from GPay and PhonePe. No new behavior to learn")]
    flows = [
        ("flow-onboarding.mp4", "Flow 1 - Onboarding", "An account in under a minute", [
            ("Contact and a PIN", "Email, phone, and an MPIN. Signup gets you an account; it doesn't verify you."),
            ("A step counter shows how far you are", "Four-step signup feels like four steps  not an open-ended form."),
            ("Auto save progress", "User can quit in between and come back anytime, start from where he left"),
            ("Rates visible with zero verification", "Tier 0 means a newcomer comparing three apps can judge SILA on price and speed")]),
        ("flow-kyc.mp4", "Flow 2 - KYC", "KYC at the moment of intent", [
            ("Triggered by the first send, not signup", "Verification lands when motivation is highest"),
            ("The ID scan does the typing", "Name, DOB, address and nationality auto-fill from one Emirates ID scan."),
            ("Verified instantly, or an honest 24h wait", 'Most users see "You\'re verified" instantly. The rest see "Almost there" with a 24-hour promise')]),
        ("flow-send.mp4", "Flow 3 - Add recipient + Send", "Send money to India", [
            ("Follows UPI pattern", "Recipients can be added by UPI ID or bank account + IFSC"),
            ("Rate, fee and total  upfront", "All amounts clear on one screen"),
            ("Dual input", '"Send 1,000 AED" or "they receive exactly 25,000 INR." Senders think in what the family needs.'),
            ('"They receive ₹25,000" leads everywhere', "The biggest number on the calculator, the review, and the CTA itself."),
            ('Expected by 9:55" becomes "in 14 minutes', "The success screen is a state machine, the app makes a claim, then shows its receipt. Trust compounds per transfer.")]),
    ]
    flow_rows = "".join(f"""<div class="sl-row" data-reveal>
      <div class="sl-row-media">{sl_video(v, title)}</div>
      <div class="sl-row-text"><p class="sl-flow">{lab}</p><h3>{title}</h3>{sl_points(pts)}</div>
    </div>""" for v, lab, title, pts in flows)
    impact = [(SL_UP, "Signup completion", "Three inputs instead of a KYC wall"),
              (SL_UP, "First-transfer conversion", "Rate and fees visible before any sensitive ask"),
              (SL_DOWN, '"Where is my money" tickets', "Every hold answers what / how long / where")]

    body = f"""{nav(root, 'work')}
<main class="sila sl-bg">
<aside class="roadmap sl-rail" aria-label="Case study sections">
  <a class="sl-rail-back" href="../index.html#work"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M16 10H4m5-5-5 5 5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Back to work</a>
  <ol><span class="progress"></span>{stations}</ol>
</aside>
<div class="sl-main">
<section class="sl-hero">
  <div class="in">
    <a class="sl-back" href="../index.html#work"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M16 10H4m5-5-5 5 5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>Go Back</a>
    <p class="sl-kicker">SILA - UAE TO INDIA REMITTANCE</p>
    <h1>Helping UAE expats send money to India in under 15 minutes with a 3-tier KYC that asks only what each transfer needs</h1>
  </div>
  <div class="sl-hero-band"><img src="{M}hero.png" alt="Three SILA app screens: tracking, home with first transfer, and the send amount screen" width="2048" height="1418"></div>
</section>

<aside class="roadmap glass sl-side" aria-label="Case study sections">
  <h4>the roadmap ✿</h4>
  <ol><span class="progress"></span>{stations}</ol>
</aside>

<section class="sl-sec" id="context"><div class="in">
  <p class="sl-eyebrow">THE CONTEXT</p>
  <h2><em>SILA</em> is a UAE → India remittance app with transparent fees, clarity at every step, and step-by-step KYC.</h2>
  <p class="sl-lead">The UAE to India corridor moves billions in remittances every year, largely from workers supporting families back home. I joined a founder as the freelance designer on his MVP which is a money transfer app built to feel fast and trustworthy rather than cluttered. I owned the design end to end, discovery through high-fidelity UI.</p>
  <div class="sl-chips"><span>End-to-end UX</span><span>UX writing</span><span>Compliance research</span></div>
</div></section>

<section class="sl-sec" id="problem"><div class="in">
  <p class="sl-eyebrow">THE PROBLEM</p>
  <h2>What users and businesses face in money transfer apps</h2>
  <h3 class="sl-sub">Users problems</h3>
  <div class="sl-grid4">{sl_numcards(users)}</div>
  <h3 class="sl-sub">Business problems</h3>
  <div class="sl-grid4">{sl_numcards(biz)}</div>
  <p class="sl-trust" data-reveal>Trust is the “product” in fintech</p>
  <div class="sl-stats">
    <div class="sl-stat" data-reveal><p>Onboarding drop-off</p><b>63–68%</b><p>of users abandon fintech onboarding - Signicat, Battle to Onboard</p><a href="https://www.signicat.com/the-battle-to-onboard-2022" target="_blank" rel="noopener">Read here</a></div>
    <div class="sl-stat" data-reveal><p>The KYC leak</p><b>~70%</b><p>abandon identity checks that take over 3 minutes -  Zyphe, Perspective AI</p><a href="https://www.zyphe.com/resources/blog/reduce-kyc-onboarding-drop-off" target="_blank" rel="noopener">Read here</a></div>
  </div>
  <div class="sl-articles" data-reveal>
    <p>Articles I referred for more KYC and Compliance related research</p>
    <div>
      <a href="https://wsa.design/news/top-10-fintech-ux-design-best-practices-for-2026" target="_blank" rel="noopener">Article 1 {ARROW}</a>
      <a href="https://www.forbes.com/councils/forbestechcouncil/2026/03/04/fintech-friction-common-ux-pain-points-and-how-to-fix-them/" target="_blank" rel="noopener">Article 2 {ARROW}</a>
      <a href="https://goodface.agency/insight/fintech-mobile-app-onboarding-checklist/" target="_blank" rel="noopener">Article 3 {ARROW}</a>
    </div>
  </div>
</div></section>

<section class="sl-sec sl-band-gray" id="research"><div class="in">
  <p class="sl-eyebrow">THE RESEARCH</p>
  <h2>The pain points, in users' own words</h2>
  <p class="sl-lead">Before designing, I read through App Store and Play Store reviews of the biggest transfer apps in the UAE</p>
  <div class="sl-reviews">
    <div><h4>Hidden costs</h4><img src="{M}research-1.png" alt="App store reviews about hidden costs" loading="lazy"></div>
    <div><h4>Unexplained holds</h4><img class="r" src="{M}research-2.png" alt="App store review about a failed transfer" loading="lazy"><img class="r" src="{M}research-3.png" alt="App store review about funds being held" loading="lazy"></div>
    <div><h4>Verification pain</h4><img src="{M}research-4.png" alt="App store reviews about verification delays" loading="lazy"></div>
    <div><h4>Support</h4><img src="{M}research-5.png" alt="App store reviews about poor support" loading="lazy"></div>
  </div>
</div></section>

<section class="sl-sec" id="discovery"><div class="in">
  <p class="sl-eyebrow">DISCOVERY</p>
  <h2>UX Problems identified</h2>
  <div class="sl-notes">{''.join(f'<div class="sl-note" data-reveal>{n}</div>' for n in notes)}</div>
</div></section>

<section class="sl-sec" id="persona"><div class="in">
  <p class="sl-eyebrow">USER PERSONA</p>
  <h2>Meet Arjun, 27.<br>Moved to Dubai before 3 months . Sends money home every month.</h2>
  <img class="sl-persona-img" src="{M}persona.jpg" alt="Illustration of Arjun on his sofa, frowning at his phone: why do they need my KYC and salary proof before I can even see the rates and fees?" loading="lazy" data-reveal>
  <div class="sl-persona">
    <div class="sl-card" data-reveal><h4>His situation</h4>
      <p>Relocated from India 3 months ago. Sends money to family once or twice a month.</p>
      <p>Tech comfortable, low patience for friction. Currently finding the best apps to send money.</p>
      <p>Price-sensitive as sending often means small rate differences compound over a year.</p></div>
    <div class="sl-card sl-quotes" data-reveal>
      <p>“Will my money reach home quickly &amp; will I know when it does?”</p>
      <p>"Am I getting a fair rate, or losing money to hidden charges?"</p>
      <p>"Why do they need my KYC and salary proof before I can even see the rates and fees?"</p></div>
  </div>
</div></section>

<section class="sl-sec" id="constraints"><div class="in">
  <p class="sl-eyebrow">CONSTRAINTS &amp; KYC</p>
  <h2>Designing inside the rules</h2>
  <p class="sl-lead sl-lead--s">Knowing which frictions are legally mandatory and which are lazy defaults is the whole game.</p>
  <h3 class="sl-sub sl-sub--l">Constraints</h3>
  <div class="sl-rules">
    <div>{''.join(f'<div class="sl-rule sl-rule--peach" data-reveal><h4>{t}</h4><p>{d}</p></div>' for t, d in peach)}</div>
    <div>{''.join(f'<div class="sl-rule sl-rule--yellow" data-reveal><h4>{t}</h4><p>{d}</p></div>' for t, d in yellow)}</div>
  </div>
  <h3 class="sl-sub sl-sub--l">Progressive KYC</h3>
  <p class="sl-lead sl-lead--s">Instead of demanding full verification upfront, I designed a three-tier model that asks only for what's needed to get started, then layers verification as the user's activity requires it. This lowers the initial wall while staying compliant.</p>
  <img class="sl-wide" src="{M}kyc-tiers.png" alt="Progressive KYC table. Tier 0 Browse: sign up, no money moving, email + phone + MPIN, frictionless. Tier 1 First transfer: Emirates ID scan + selfie, purpose, income range, sending plans, quick. Tier 2 Higher amount: above monthly limits, source of funds, explained." loading="lazy" data-reveal>
</div></section>

<section class="sl-sec" id="decisions"><div class="in">
  <p class="sl-eyebrow">KEY DECISIONS</p>
  <h2>Decisions that shaped the product</h2>
  <div class="sl-grid3">{sl_numcards(decisions, "sl-card sl-card--line")}</div>
</div></section>

<section class="sl-sec" id="flow"><div class="in">
  <p class="sl-eyebrow">THE USER-FLOW</p>
  <h2>See it in motion</h2>
  <p class="sl-lead">The complete experience across onboarding, sending money, and the states</p>
  {flow_rows}
</div></section>

<section class="sl-sec sl-band-dark" id="tier2"><div class="in">
  <p class="sl-eyebrow">TIER 2 VERIFICATION</p>
  <h2>Sending more than the monthly limit</h2>
  <p class="sl-lead">Bigger transfers need proof of income, a requirement under UAE regulation. The design job was to make it clear, early, and one-time.</p>
  <div class="sl-row" data-reveal>
    <div class="sl-row-media">{sl_video("tier2.mp4", "Tier 2 verification flow", round_=True)}</div>
    <div class="sl-row-text">{sl_points([("Shown before he pays, not after", "An amber note and a meter as he types the amount."), ("Never blocked", '"Send AED 6,000 instead"  his remaining limit, calculated for him.'), ("One document, one time", "Salary certificate or 3-month bank statement. Named upfront, so he knows what to look for.")])}</div>
  </div>
</div></section>

<section class="sl-sec" id="edge"><div class="in">
  <p class="sl-eyebrow">EDGE CASE</p>
  <h2>When the document is <span class="sl-red">rejected</span></h2>
  <p class="sl-lead">In cases like this, SILA shows the reason and the fix rather than generic "verification failed" and leave the user guessing.</p>
  <div class="sl-row" data-reveal>
    <div class="sl-row-media">{sl_video("rejected.mp4", "Document rejected flow")}</div>
    <div class="sl-row-text">{sl_points([("The reason is specific", '"The photo was too blurry to read"  never "invalid document".'), ("One fix, in plain words", "Rest the document on a flat surface and hold your phone steady.")])}</div>
  </div>
</div></section>
<section class="sl-band-grad"><div class="in">
  <h3 class="sl-center">Rejection reasons, with its fixes</h3>
  <img class="sl-wide" src="{M}rejection-reasons.png" alt="Error in document reading screen, surrounded by rejection reasons and fixes: wrong document type, too old, cut off corners, name mismatch, glare or shadow." loading="lazy" data-reveal>
</div></section>

<section class="sl-sec" id="impact"><div class="in">
  <p class="sl-eyebrow">PROJECTED IMPACT</p>
  <h2>What should improve</h2>
  <div class="sl-impact">{''.join(f'<div class="sl-card" data-reveal><span class="sl-arrow">{ic}</span><h4>{t}</h4><p>{d}</p></div>' for ic, t, d in impact)}</div>
</div></section>

<section class="sl-sec" id="retention"><div class="in">
  <div class="sl-row sl-row--retention" data-reveal>
    <div class="sl-row-media"><img src="{M}retention.png" alt="Delivered screen with a 'Send again next month?' prompt" loading="lazy"></div>
    <div class="sl-row-text"><p class="sl-eyebrow">RETENTION</p><h3>Return loops designed in</h3>{sl_points([('"Send this again next month?"', "Appears only at delivered. One tap from a scheduled monthly transfer.")])}</div>
  </div>
</div></section>

<section class="sl-sec" id="learnings"><div class="in">
  <p class="sl-eyebrow">LEARNINGS &amp; NEXT STEPS</p>
  <h2>Designing for trust is a different problem!!</h2>
  <h3 class="sl-sub sl-sub--m">Learnings</h3>
  {sl_points([("The worst screen sets the tone.", "Along with good success messages,  users remember is what the app said when their money stopped."), ("Regulation made the design easier, not harder.", 'Once I knew which rules were real, every field had a reason I could point to. "This exists because of a threshold" ends debates'), ("Clarity is a feature, not a finish.", "Step counters, named documents, live status, none of these are visual polish. They're the product doing its main job - telling the user the truth about where they stand.")])}
  <h3 class="sl-sub sl-sub--m">What I would do next if still working on the product</h3>
  <ul class="sl-points sl-points--inline">{''.join(f'<li>{SL_ICON}<p><b>{t}</b> {d}</p></li>' for t, d in [("KYC step-completion rate", "per step, to find the exact drop-off point"), ("Time-to-verification", "against the ~3-minute abandonment threshold"), ("Re-upload rate", "the document step is the highest-leverage lever"), ("Transfer completion vs. cancellation", "split by where users drop")])}</ul>
  <p class="sl-quote" data-reveal>“A remittance app has to manufacture the trust a bank inherits”</p>
</div></section>
</div>
</main>
{footer(root)}"""
    return head("SILA · Rajvi Patel", "Helping UAE expats send money to India in under 15 minutes with a 3-tier KYC that asks only what each transfer needs.", root) + body


# ---------------------------------------------------------------- CityLockers (matches the Framer case study)
CM = "../assets/media/citylockers/"


def cs_rail(secs):
    """Static left column (wide screens) + sliding section bar (phone/tablet), shared by the Framer-style case studies."""
    stations = "".join(f'<li><a href="#{i}"><span class="node"></span>{n}</a></li>' for i, n in secs)
    rail = f"""<aside class="roadmap sl-rail" aria-label="Case study sections">
  <a class="sl-rail-back" href="../index.html#work"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M16 10H4m5-5-5 5 5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Back to work</a>
  <ol><span class="progress"></span>{stations}</ol>
</aside>"""
    bar = f"""<aside class="roadmap glass sl-side" aria-label="Case study sections">
  <h4>the roadmap ✿</h4>
  <ol><span class="progress"></span>{stations}</ol>
</aside>"""
    return rail, bar


def cl_bullets(items, cls="cl-bul"):
    return f'<ul class="{cls}">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def citylockers_page():
    root = "../"
    rail, bar = cs_rail([("context", "The context"), ("impact", "The impact"), ("problem", "The problem"),
                         ("previous", "Previous design"), ("research", "Research"), ("decision1", "Decision 1"),
                         ("decision2", "Decision 2"), ("decision3", "Decision 3"), ("walkthrough", "Walkthrough"),
                         ("beforeafter", "Before / After"), ("learnings", "Learnings")])
    prev = [("No locker door IDs", ["No A1, B2 labels so users had no way to confirm which locker they selected."]),
            ("Horizontal scroll on the locker grid", ["Some lockers weren't visible without scrolling.", "On a touch kiosk, most users never find them."]),
            ("Action buttons share same visual weight", ["Continue and Back looked identical so no clear primary action."]),
            ("No colour coding on the locker grid", ["Every door looked the same. Available, taken, selected which was impossible to tell apart."]),
            ("No visual hierarchy or clear entry point", ["Every element competed equally. A first-time user had no obvious next step."]),
            ("Missing information", ["Selected duration is missing from the booking summary.", "Cant find which duration option is selected too."])]
    prev_html = "".join(f'<div class="cl-card cl-card--pink" data-reveal><span class="cl-num">{i+1:02d}</span><h4>{t}</h4>{cl_bullets(b)}</div>'
                        for i, (t, b) in enumerate(prev))
    comp = [("DIGITAL COMPETITOR", "Bounce &amp; LuggageHero", ["Used both end-to-end to understand existing booking flows.", "They work through <b>third-party shops, different trust model, different safety level.</b> Same core problem, different solution."]),
            ("IN PERSON OBSERVATION - BUDAPEST &amp; PRAGUE", "Train station lockers, used in person", ["Used lockers at Budapest Keleti and Prague main station to study what works.", "No size guide were available on the doors."]),
            ("HARDWARE REFERENCE", "Noon Lockers, Dubai", ["Studied for hardware interaction patterns how users approach a physical locker unit and how the screen relates to the doors."]),
            ("USER CONVERSATIONS", "Frequent travellers in my network", ["Talked to friends who travel often.", "They brought up locker experiences in Paris and Spain confirming the checkout gap is a real recurring frustration, not a niche edge case."])]
    comp_html = "".join(f'<div class="cl-comp" data-reveal><div class="cl-comp-head"><span class="cl-tag">{tag}</span><h4>{t}</h4></div>{cl_bullets(b)}</div>'
                        for tag, t, b in comp)
    changed = [("Label every door", ["Added Medium / Large size labels on every door in kiosk grid so no instructions needed."]),
               ("Let users pick their locker", ["No competitor does this. Auto-assignment ignores that travellers with large bags need large lockers, or may want adjacent doors for multiple bags."]),
               ("Keep it simple above all", ["The best lockers I used in Europe were obvious. That became the bar.", "If a first-time user can't figure it out in under 30 seconds, it's not done."])]
    changed_html = "".join(f'<div class="cl-changed" data-reveal><span class="cl-num">{i+1:02d}</span><h4>{t}</h4><div class="cl-sticky">{cl_bullets(b)}</div></div>'
                           for i, (t, b) in enumerate(changed))

    def numbered(items, tone):
        return '<ol class="cl-badges cl-badges--' + tone + '">' + "".join(f"<li><span>{i+1}</span><p>{x}</p></li>" for i, x in enumerate(items)) + "</ol>"

    persona = lambda letter, img, name, role, text, chips: f"""<div class="cl-persona" data-reveal>
      <div class="cl-persona-top">User {letter}</div>
      <div class="cl-persona-body">
        <div class="cl-persona-id"><img src="{CM}{img}" alt="" width="64" height="64" loading="lazy"><div><h4>{name}</h4><p>{role}</p></div></div>
        <p class="cl-persona-text">{text}</p>
        <div class="cl-chips">{''.join(f'<span>{c}</span>' for c in chips)}</div>
      </div>
    </div>"""

    body = f"""{nav(root, 'work')}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Indie+Flower&display=swap">
<main class="sila cl sl-bg">
{rail}
<div class="sl-main">
<section class="sl-hero">
  <div class="in">
    <a class="sl-back" href="../index.html#work"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M16 10H4m5-5-5 5 5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>Go Back</a>
    <p class="sl-kicker">CITYLOCKERS KIOSK EXPERIENCE</p>
    <h1>Helping travellers go hands-free in under 4 minutes, 2,000+ bookings completed across Dubai.</h1>
  </div>
  <div class="cl-hero-band"><img src="{CM}hero.png" alt="CityLockers kiosk home screen: Book Locker, Open My Locker, Delivery, and Book a free locker for 30 minutes" width="2048" height="1258"></div>
</section>
{bar}

<section class="sl-sec cl-gray" id="context"><div class="in">
  <p class="sl-eyebrow">THE CONTEXT</p>
  <h2>CityLockers gives travellers a safe place to drop their bags and help them keep moving!</h2>
  <p class="sl-lead">CityLockers is an <b>early-stage Dubai startup building smart locker infrastructure across malls, hotels, beaches, and residential buildings</b>. I was brought in to redesign the kiosk experience, rethinking the flows, rebuilding the interface, and designing every edge case from the ground up.</p>
  <div class="cl-facts">
    <div><p class="sl-eyebrow">TEAM</p><p>Product designer (Me)<br>4 Frontend &amp; backend developers<br>Founder &amp; Investor</p></div>
    <div><p class="sl-eyebrow">LOCATION</p><p>UAE</p></div>
    <div><p class="sl-eyebrow">PLATFORM</p><p>Touch Kiosk</p></div>
  </div>
  <p class="sl-eyebrow cl-impact-label" id="impact">THE IMPACT</p>
  <div class="cl-impact" data-reveal>
    <div><p>Used by</p><b>2000+</b></div>
    <div><p>Real users tested: prototype and post-deployment</p><b>10</b></div>
    <div><p>Average booking time</p><b>&lt; 4 Mins</b></div>
  </div>
</div></section>

<section class="sl-sec" id="problem"><div class="in">
  <p class="sl-eyebrow">THE PROBLEM</p>
  <h2>Luggage holds<br>travellers back.</h2>
  <p class="sl-lead">UAE welcomes <b>over 20 million tourists annually</b>. The gap between hotel checkout and departure sometimes 6 to 8 hours forces <b>travellers to drag luggage through malls, beaches, and tourist spots. No direct competitor solves this in Dubai</b> with a dedicated locker network.</p>
  <div class="cl-problem">
    <div class="cl-problem-cards">
      <div class="cl-card" data-reveal><h4>The checkout gap</h4><p>Hotels check you out at 12pm. Your flight is at 10pm. That's 10 hours with nowhere to leave your bags.</p></div>
      <div class="cl-card" data-reveal><h4>Luggage kills the experience</h4><p>Travellers skip attractions or pay for hotel storage just to move freely for a few hours.</p></div>
      <div class="cl-card" data-reveal><h4>No dedicated solution in Dubai</h4><p>Bounce and LuggageHero use grocery stores. CityLockers offers proper dedicated lockers, a different level of trust.</p></div>
    </div>
    <svg class="cl-links" aria-hidden="true"><defs><marker id="clArr" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" fill="#17171a"/></marker></defs>
      <line x1="54%" y1="16.5%" x2="84%" y2="16.5%"/><line x1="84%" y1="16.5%" x2="84%" y2="22%" marker-end="url(#clArr)"/>
      <line x1="54%" y1="50%" x2="68%" y2="50%" marker-end="url(#clArr)"/>
      <line x1="54%" y1="83.5%" x2="84%" y2="83.5%"/><line x1="84%" y1="83.5%" x2="84%" y2="78%" marker-end="url(#clArr)"/>
    </svg>
    <div class="cl-dark" data-reveal><b>20M+</b><p>Tourists visit UAE annually,</p><p>most experiencing the checkout-to-departure luggage problem firsthand.</p></div>
  </div>
</div></section>

<section class="sl-sec cl-gray" id="previous"><div class="in">
  <p class="sl-eyebrow">WHAT THEY HAD WHEN I JOINED</p>
  <h2>The previous design</h2>
  <p class="sl-lead">Before I could design anything new, I had to understand exactly <b>what was broken</b> and why <b>rebuilding from scratch</b> was the right call.</p>
  <img class="cl-prev-img" src="{CM}previous-design.png" alt="The previous CityLockers Book a Locker screen" loading="lazy" data-reveal>
  <div class="cl-grid3">{prev_html}</div>
</div></section>

<section class="sl-sec" id="research"><div class="in">
  <p class="sl-eyebrow">THE RESEARCH</p>
  <h2>I studied what already works &amp;<br>what breaks.</h2>
  <p class="sl-lead">I used real lockers, studied competitors end-to-end, and talked to frequent travellers in my network.</p>
  <h3 class="cl-sub">Who I was designing for</h3>
  <div class="cl-grid2">
    {persona("A", "persona-emma.png", "Emma Richardson", "Marketing Manager · Visiting from London", "<b>First-time tourist in Dubai</b> on a 5-day solo trip. She has a gap between hotel checkout and check-in with luggage to manage. She wants to <b>explore freely without carrying bags in the hand.</b>", ["Store luggage between hotel changes", "Easy to understand", "Affordable for a few hours"])}
    {persona("B", "persona-ahmed.png", "Ahmed Hassan", "Software Developer · JBR, Dubai", "<b>Egyptian expat in a high-security residential tower</b> where delivery personnel aren't permitted beyond the lobby. Works from home but <b>misses 60% of deliveries because security won't allow couriers upstairs.</b>", ["Receive orders without missing deliveries", "Reliable solution", "24/7 access"])}
  </div>
  <h3 class="cl-sub">Competitive &amp; observational analysis</h3>
  <div class="cl-grid2">{comp_html}</div>
  <h3 class="cl-sub">What the research changed?</h3>
  <div class="cl-changed-row">{changed_html}</div>
  <p class="cl-boring">Boring part is over! 😮‍💨</p>
</div></section>

<section class="sl-sec cl-gray" id="decision1"><div class="in">
  <p class="sl-eyebrow">KEY DECISIONS</p>
  <h2>With the research done, I rebuilt all screens.<br>Three decisions defined the experience.</h2>
  <p class="sl-eyebrow cl-dec">DECISION 1</p>
  <h3 class="cl-sub cl-sub--tight">Consolidate the home screen options</h3>
  <div class="cl-box" data-reveal>
    <div class="cl-box-row">{numbered(["4 options in a 2×2 grid → cognitive load, unclear priority", '"Manage My Booking" and "Extend Booking" are the same user journey split into two options unnecessarily.', "No low-friction entry point for first-time users"], "red")}<img src="{CM}home-before.png" alt="Previous home screen with four options in a 2×2 grid" loading="lazy"></div>
    <p class="cl-divider"><span>What changed and why</span></p>
    <div class="cl-box-row">{numbered(["3 options in a row → clear hierarchy, one decision", '"Extend Booking" consolidated under "Open My Locker" → one entry point', '"Open my locker" → clear, specific copy', '"Book a free locker for 30 minutes" → a business decision which drives conversion'], "green")}<img src="{CM}home-after.png" alt="New home screen with three options in a row and a free 30 minute locker button" loading="lazy"></div>
  </div>
</div></section>

<section class="sl-sec cl-gray cl-tight-top" id="decision2"><div class="in">
  <p class="sl-eyebrow cl-dec">DECISION 2</p>
  <h3 class="cl-sub cl-sub--tight">The manage booking screen had three options.<br>I reduced it to two - clearer actions, fewer steps.</h3>
  <div class="cl-ba-card" data-reveal><img src="{CM}manage-before.png" alt="Previous manage bookings screen with three choices" loading="lazy"><div><p class="cl-ba-label">Before</p>{cl_bullets(['Opened to three choices -"Access &amp; End Booking", "Access &amp; Continue Booking", "Extend Booking"', "First two meant the same thing, users had to read carefully to spot the difference"])}</div></div>
  <div class="cl-ba-card" data-reveal><img src="{CM}manage-after.png" alt="New booked lockers screen with Open Locker and Extend Current Booking" loading="lazy"><div><p class="cl-ba-label">After</p>{cl_bullets(["Opens directly to two clear actions, Open Locker or Extend Booking", "Confirmation dialogue inside the flow handles the end booking vs continue decision", "Extend Booking opens the same locker selection screen so no new patterns to learn."])}</div></div>
</div></section>

<section class="sl-sec" id="decision3"><div class="in">
  <p class="sl-eyebrow cl-dec">DECISION 3</p>
  <h3 class="cl-sub cl-sub--tight">Let users pick their own locker.</h3>
  <div class="cl-grid-evo" data-reveal>
    <p class="cl-evo-title"><span>Grid Evolution</span></p>
    <div class="cl-evo-row">
      <div><span class="cl-tag">Previous</span><img src="{CM}grid-previous.png" alt="Previous locker grid, all doors look the same" loading="lazy"></div>
      <div><span class="cl-tag">V1</span><img src="{CM}grid-v1.png" alt="First version of the colour-coded grid" loading="lazy"></div>
      <div><span class="cl-tag">Final</span><img src="{CM}grid-final.png" alt="Final locker grid with door IDs, sizes and availability colours" loading="lazy"></div>
    </div>
    <div class="cl-evo-arrow"></div>
    {cl_bullets(["No competitor lets users pick their own locker, everyone auto-assigns based on size selection. I gave users a visual grid, colour-coded by availability, so they tap exactly the door they want.", "Auto-assignment can't account for a traveller with a large suitcase, or someone who needs two adjacent doors. The grid handles all of it without a single line of instruction copy."])}
  </div>
</div></section>

<section class="sl-sec cl-tight-bottom" id="walkthrough"><div class="in">
  <p class="sl-eyebrow">WALKTHROUGH</p>
  <h2>Here's how kiosk works</h2>
  <p class="sl-lead">A complete kiosk experience from first touch to locker open.</p>
</div></section>
<section class="cl-video-band"><div class="in"><h3>Booking locker flow</h3><div class="cl-vframe cl-vframe--booking"><div class="cl-vclip"><video src="{CM}flow-booking.mp4" muted loop playsinline preload="none" data-autoplay aria-label="Booking locker flow on the kiosk"></video></div></div></div></section>
<section class="cl-video-band"><div class="in"><h3>Manage booking flow</h3><div class="cl-vframe cl-vframe--manage"><div class="cl-vclip"><video src="{CM}flow-manage.mp4" muted loop playsinline preload="none" data-autoplay aria-label="Manage booking flow on the kiosk"></video></div></div></div></section>

<section class="sl-sec" id="beforeafter"><div class="in">
  <p class="sl-eyebrow">Before / After</p>
  <h3 class="cl-sub cl-sub--tight">Slide to see changes</h3>
  <div class="cl-slider" data-ba style="--pos:50%" data-reveal>
    <img src="{CM}slider-a.png" alt="New Book a Locker screen" loading="lazy">
    <div class="cl-slider-before"><img src="{CM}slider-b.png" alt="Old Book a Locker screen" loading="lazy"></div>
    <span class="cl-slider-handle" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="m9 7-5 5 5 5M15 7l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    <input type="range" min="0" max="100" value="50" aria-label="Slide to compare the old and new screen">
  </div>
  <div class="cl-proto" data-reveal>
    <div><h3>Want to try Prototype?</h3><p>Click here to check Figma Prototype!</p></div>
    <a href="https://www.figma.com/proto/cV1RM3IOsOe1lO1wSM8GV3/CityLockers-Kiosk?node-id=691-11992&amp;viewport=678%2C334%2C0.11&amp;t=ShPyNHbvu6HOM7Ha-1&amp;scaling=min-zoom&amp;content-scaling=fixed&amp;starting-point-node-id=691%3A11992&amp;show-proto-sidebar=1&amp;page-id=628%3A8739" target="_blank" rel="noopener">View Prototype {ARROW}</a>
  </div>
</div></section>

<section class="sl-sec" id="learnings"><div class="in">
  <p class="sl-eyebrow">MY LEARNINGS</p>
  <h2>What CityLockers Kiosk Project<br>Taught Me</h2>
  <div class="cl-learn">
    <div class="cl-card cl-learn-card" data-reveal><h4>Designing for a small screen kiosk is different</h4>{cl_bullets(["This wasn't an app someone opens on their sofa. <b>It's a kiosk in a metro station or mall while luggage in hand, somewhere to be.</b>", "That context changed how I thought about every screen, how much text to add, <b>how big the buttons should be, how many steps.</b>", "<b>Testing in the real environment taught me more than any prototype session.</b>", "<b>The colour-coded locker grid came as a savior.</b> Nobody needs to read anything. That one decision made the screen work for everyone, regardless of language"])}</div>
    <figure class="cl-me" data-reveal><figcaption>That’s me!</figcaption><img src="{CM}me.jpg" alt="Rajvi testing the CityLockers kiosk in person" loading="lazy"></figure>
  </div>
  <div class="cl-card cl-learn-card" data-reveal><h4>What I'd do next with more time and data</h4>{cl_bullets(["Run usability sessions at the physical kiosk testing 5 users, <b>observing the manage booking flow specifically</b>", "Add a <b>remote end-booking option</b> in the app as post-deployment testing showed users didn't always know they had to end at the kiosk", "<b>Booking drop-off tracking</b> to identify exactly where users abandon the flow", "Test Arabic RTL layout as it is functional but not fully optimised for RTL reading patterns"])}</div>
</div></section>
</div>
</main>
{footer(root)}"""
    return head("CityLockers Kiosk · Rajvi Patel", "Helping travellers go hands-free in under 4 minutes, 2,000+ bookings completed across Dubai.", root) + body


# ---------------------------------------------------------------- SKU Platform (matches the Framer case study)
KM = "../assets/media/sku/"
SK_CMD = '<svg class="sk-cmd" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6a3 3 0 1 0-3 3h3V6Zm0 0v12m0-12h6m-6 12a3 3 0 1 1-3-3h3v3Zm0 0h6m0 0a3 3 0 1 0 3-3h-3v3Zm0 0V6m0 0a3 3 0 1 1 3 3h-3V6Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
SK_EXT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SK_ICONS = {
    "sitemap": '<svg viewBox="0 0 32 32"><rect x="12" y="3" width="8" height="6" rx="1.5"/><rect x="3" y="23" width="8" height="6" rx="1.5"/><rect x="12" y="23" width="8" height="6" rx="1.5"/><rect x="21" y="23" width="8" height="6" rx="1.5"/><path d="M16 9v7M7 23v-7h18v7M16 16v7" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    "flow": '<svg viewBox="0 0 32 32"><rect x="3" y="4" width="9" height="7" rx="1.5"/><rect x="20" y="12.5" width="9" height="7" rx="1.5"/><rect x="3" y="21" width="9" height="7" rx="1.5"/><path d="M12 7.5h4v17h-4M16 16h4" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    "wire": '<svg viewBox="0 0 32 32"><rect x="3" y="4" width="26" height="24" rx="2.5" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M3 10h26" stroke="currentColor" stroke-width="2.4"/><rect x="7" y="14" width="8" height="10" rx="1"/><path d="M18 15h7M18 19h7M18 23h5" stroke="currentColor" stroke-width="2"/></svg>',
    "pen": '<svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="14" fill="#efe9f8"/><path d="M9 23l2-6 9-9 4 4-9 9-6 2Z"/><path d="M18 10l4 4" stroke="#efe9f8" stroke-width="1.5"/></svg>',
}


def sk_head(icon, title, text, cls=""):
    ic = f'<span class="sk-ic">{SK_ICONS[icon]}</span>' if icon in SK_ICONS else (f'<img class="sk-ic" src="{KM}{icon}" alt="" width="56" height="56">' if icon else "")
    return f'<div class="sk-head {cls}"><div>{ic}<h3>{title}</h3></div><p>{text}</p></div>'


def sk_split(pill, text):
    return f'<div class="sk-head sk-head--pill"><div><span class="sk-pill">{pill}</span></div><p>{text}</p></div>'


def sk_intro(small, big):
    return f'<div class="sk-intro" data-reveal><p>{small}</p><h2>{big}</h2></div>'


def sku_page():
    root = "../"
    rail, bar = cs_rail([("context", "Context"), ("summary", "Project summary"), ("problem", "The problem"), ("goals", "The goals"),
                         ("discover", "Discover"), ("define", "Define"), ("design", "Design"), ("deliver", "Deliver"),
                         ("results", "Results"), ("takeaways", "Key takeaways"), ("conclusion", "Conclusion")])
    PROTO = "https://www.figma.com/proto/ZCjXwYFBb5MsBgypUKW4CD/Prototype?page-id=0%3A1&amp;node-id=1-5646&amp;p=f&amp;viewport=3367%2C-476%2C0.32&amp;t=4joBuUKoRZuxixNm-1&amp;scaling=min-zoom&amp;content-scaling=fixed&amp;starting-point-node-id=4%3A3296"
    problems = ["Inventory management creates financial risk and logistical challenges", "Product sourcing requires navigating multiple platforms and suppliers",
                "Store integration often involves complex technical knowledge", "Order fulfillment adds another layer of operational complexity"]
    prios = ["<b>Simplicity of integration</b> with their existing platforms", "Less technical <b>user experience</b>", "<b>Ready to sell</b> high quality products",
             "<b>Ability to customize product details</b> according to their brand needs", "<b>Speed</b> of adding products to their store"]
    takeaways_l = ["User finds difficult to handle orders across different e-commerce platforms simultaneously", "Users want a platform that helps them to customize and build their own brand experience",
                   "A platform which Addresses underserved markets while maintaining global capabilities", "Limited options of products to select from"]
    takeaways_r = ["78% of sellers felt overwhelmed by the technical complexity of managing multiple platforms,", "100% of participants struggled with pricing decisions due to unclear product cost, shipping fees and profit margins",
                   "Users experience Manual Product Import Fatigue", "90% Users feel Inventory Anxiety &amp; Storage Limitations"]
    tk = lambda items: "".join(f'<div class="sk-note" data-reveal>{SK_CMD}<p>{t}</p></div>' for t in items)
    wires = [("Dashboard", "wire-dashboard.png"), ("Orders", "wire-orders.png"), ("Products", "wire-products.png"),
             ("My Stores", "wire-stores.png"), ("My Products", "wire-myproducts.png"), ("Import List", "wire-importlist.png")]
    features = ["The central hub providing users with an overview of their dropshipping business", "Centralized order management across all connected stores",
                "Product discovery and sourcing interface", "Staging area for product customization before adding to stores",
                "Management of products successfully added to connected stores", "Store connection &amp; statistics", "User profile and platform configuration"]
    steps = [("Click on add store", "store-1.png"), ("Add new store modal opens", "store-2.png"),
             ("Select store &amp; add store URL", "store-3.png"), ("With just one step of “confirm permissions”, Its done!", "store-4.png")]
    results = [("User Growth", "500+ seller onboarding within 6 months with 75% retention rate through simplified one-click integration reducing setup time from hours to minutes."),
               ("User Experience", "Integration time reduced by 93% (from 30+ minutes to under 2 minutes) &amp; Product discovery and addition accelerated by 87% (from 15 minutes per product to under 2 minutes)"),
               ("Platform Performance", "Handle 10,000+ daily product imports with 50% improved order processing efficiency and real-time synchronization across integrated platforms.")]
    keys = ["I learned how to think beyond screens, to design systems that scale and simplify complex business models. As the sole designer in early stages, I wore many hats and learned to balance speed with precision.",
            "Realized that successful B2B platforms must clearly demonstrate ROI to users. Every design decision needed to translate into measurable time savings or revenue opportunities for sellers.",
            "Discovered that revealing information gradually from store connection to product browsing to detailed editing prevents cognitive overload and helps users feel confident navigating complex business tools.",
            "Learned to design for growth from day one considering how the interface would handle thousands of products and multiple store connections without losing usability or performance."]

    body = f"""{nav(root, 'work')}
<main class="sila sk sl-bg">
{rail}
<div class="sl-main">
<section class="sl-hero sk-hero">
  <div class="in">
    <a class="sl-back" href="../index.html#work"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M16 10H4m5-5-5 5 5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>Go Back</a>
    <h1>SKU Platform</h1>
    <div class="sk-meta">
      <div><p>Role</p><b>Product designer</b><b>User Journey</b><b>User Research</b></div>
      <div><p>Duration</p><b>4 Months</b></div>
      <div><p>Team</p><b>Designer 🙋🏻‍♀️</b><b>2 Backend Developers</b><b>1 Frontend Developer</b><b>CEO</b></div>
      <div class="sk-links"><a href="https://skuplatform.com/" target="_blank" rel="noopener">Live website link {SK_EXT}</a><a href="{PROTO}" target="_blank" rel="noopener">Prototype link {SK_EXT}</a></div>
    </div>
    <div class="sk-context" id="context"><h2 class="sk-ghost">Context</h2><p>SKU Platform helps e-commerce sellers grow by connecting their already exisitng stores (Shopify, Salla, WooCommerce ) and importing ready-to-sell products no inventory or logistics needed.</p></div>
  </div>
  <div class="sk-hero-img"><img src="{KM}hero.png" alt="SKU Platform product discovery screen on a laptop" width="2048" height="1152"></div>
</section>
{bar}

<section class="sl-sec" id="summary"><div class="in">
  <div class="sk-summary">
    <div><p class="sk-kick">An unconventional journey of designer!</p><h2>Project summary</h2>
      <p class="sk-summary-text">As the <b>founding product designer</b> behind SKU Platform - a <b>global drop-shipping solution,</b> I worked closely with the founder &amp; engineers, shaped the product direction, and helped turn a raw concept into a full, scalable platform. I <b>led</b> the design, turning <b>a raw idea</b> into a <b>fully functional platform</b> &amp; created efficient user experience that would make dropshipping accessible to sellers with <b>minimal technical knowledge.</b></p></div>
    <div class="sk-promo" data-reveal><img class="sk-promo-woman" src="{KM}summary-phone.png" alt="A seller smiling at her laptop" loading="lazy"><div class="sk-promo-side"><div class="sk-promo-logo"><img src="{KM}summary-logo.png" alt="SKU Platform" loading="lazy"></div><p>SKU makes dropshipping easy connect your store, import products, and sell without inventory.</p></div></div>
  </div>
</div></section>

<section class="sl-sec" id="problem"><div class="in">
  <div class="sk-split"><div><p class="sk-kick">But first!</p><h2>The Problem</h2></div>
    <p class="sk-lead">Sellers want to scale their product listings without <b>the hassle of inventory</b> or <b>manual uploads</b> , but most tools make it <b>complicated to find suitable products, difficult to integrate with stores</b>, or <b>time-consuming.</b></p></div>
  <div class="sk-problems">{''.join(f'<div class="sk-problem" data-reveal>{p}</div>' for p in problems)}</div>
</div></section>

<section class="sl-sec sk-tight-top" id="goals"><div class="in">
  {sk_intro("Not to forget", "The Goals")}
  <div class="sk-goals">
    <div class="sk-goal sk-goal--wide" data-reveal><h3>User</h3><p>Making it <b>easy for sellers to scale their stores</b> - by giving them ready-to-sell products, smooth integrations, and zero inventory stress.</p></div>
    <div class="sk-goal" data-reveal><h3>Business</h3><p>Creating a <b>drop-shipping website</b> with smooth user experience</p></div>
    <div class="sk-goal" data-reveal><h3>Design</h3><p>Transform technical complexity into intuitive, <b>scalable solutions</b></p></div>
  </div>
</div></section>
<div class="sk-band"><img src="{KM}goals-band.png" alt="Design process: Discover, Define, Design, Deliver" loading="lazy"></div>

<section class="sl-sec" id="discover"><div class="in">
  {sk_intro("Let’s", "Discover")}
  <div class="sk-head"><div><div class="sk-faces">{''.join(f'<img src="{KM}user-{i}.jpg" alt="" width="48" height="48" loading="lazy">' for i in range(1, 6))}</div><h3>User Research</h3></div>
    <p>To understand the real challenges facing e-commerce sellers, I conducted interviews with <b>5 e-commerce store owners</b> across different platforms.</p></div>
  <div class="sk-prio"><h2 class="sk-ghost">Their Priorities</h2><div class="sk-prio-cards">{''.join(f'<div class="sk-prio-card" data-reveal><span>{i+1}.</span><p>{p}</p></div>' for i, p in enumerate(prios))}</div></div>
</div></section>
<section class="sl-sec sk-gray"><div class="in">
  <h2 class="sk-ghost">Competitive Research</h2>
  <img class="sk-wide" src="{KM}competitive.svg" alt="Competitive research table comparing Spocket, Salehoo, Modalyst and SKU Platform on integrations, order management, target user, supplier region, branded packaging, product import and user experience" loading="lazy" data-reveal>
</div></section>
<section class="sl-sec sk-lav"><div class="in">
  {sk_intro("Everything i found during all kind of research", "Major takeaways from research")}
  <div class="sk-notes"><div>{tk(takeaways_l)}</div><div class="sk-notes-r">{tk(takeaways_r)}</div></div>
</div></section>

<section class="sl-sec" id="define"><div class="in">
  {sk_intro("Let’s", "Define")}
  {sk_head("persona-avatar.png", "User Persona", "The fictional represesntation of the key user of this app.")}
  <div class="sk-persona">
    <p class="sk-quote">“I spend hours every day juggling between different supplier websites, manually adding products, and tracking inventory across multiple platforms. It is exhausting."</p>
    <div class="sk-persona-row">
      <div class="sk-persona-id"><h4>Rohan Sharma</h4><p>Age - 32 Years</p><p>Occupation -E-commerce Entrepreneur &amp; Clothing Store Owner</p><p>Income - 12,000 AED/month</p><p>Platform: Shopify store with growing customer base</p><p>Experience: 3 years in e-commerce, self-taught digital marketing skills</p></div>
      <div class="sk-persona-story"><h4>Background Story</h4><p>Rohan started his Clothing E-commerce website from his apartment in 2021, initially selling a collection of locally-sourced items. As his Instagram following grew and customer demand increased, he quickly realized that his small inventory couldn't keep pace with market opportunities.  Rohan faces a common challenge: <b>Finding unique products to sell without the hassle of inventory management.</b> He's tech-savvy enough to manage his Shopify store and social media marketing, but gets overwhelmed by the technical aspects of supplier integration and inventory management.</p></div>
    </div>
    <div class="sk-quads">
      <div><span class="sk-pill">Goals</span><img src="{KM}persona-goals.svg" alt="Goals: expand product catalog without increasing storage costs or inventory risk; manage orders from one platform; find unique, trending home decor items that align with his brand aesthetic" loading="lazy"></div>
      <div class="sk-quad-r"><span class="sk-pill">Motivations</span><img src="{KM}persona-motivations.svg" alt="Motivations: build a sustainable business model; scale his current product catalogue; find more time for marketing and brand building" loading="lazy"></div>
      <div><span class="sk-pill">Pain points &amp; frustrations</span><img src="{KM}persona-pains.svg" alt="Pain points: high upfront costs for stocking new product lines; difficulty predicting which products will sell; overwhelmed by complex dropshipping platform interfaces; spends too much time on operational tasks; struggles with integrating multiple tools; time-consuming supplier research" loading="lazy"></div>
      <div class="sk-quad-r"><span class="sk-pill">Needs &amp; Expectations</span><img src="{KM}persona-needs.svg" alt="Needs: simple one-click integration with his existing Shopify store; access to unique products that fit his niche; automated inventory and order management; reliable suppliers with quality products and reasonable shipping times; simple and less technical user experience" loading="lazy"></div>
    </div>
  </div>
</div></section>
<section class="sl-sec sk-pattern"><div class="in">
  {sk_head("sitemap", "Site map", "Created a comprehensive site map to visualize the platform's information architecture and ensure logical navigation flows between core features")}
  <img class="sk-wide sk-wide--md" src="{KM}sitemap.png" alt="SKU Platform site map: sign up, home page, then dashboard, orders, products, my stores and settings with their sub-pages" loading="lazy" data-reveal>
</div></section>
<section class="sl-sec sk-gray"><div class="in">
  {sk_head("flow", "Primary user flow", "This flow represents the core SKU experience - taking a new user from initial login through successfully importing their first customized product to their e-commerce store.")}
  <img class="sk-wide" src="{KM}userflow.png" alt="Primary user flow from login through store connection, product exploration and customization to importing the product to the store" loading="lazy" data-reveal>
</div></section>
<section class="sl-sec sk-dots"><div class="in">
  {sk_head("wire", "Wireframes", "Initial wireframes showing the dashboard, orders list, explore products interface, and product category navigation")}
  <div class="sk-wires">{''.join(f'<div class="sk-wire" data-reveal><span class="sk-pill">{n}</span><img src="{KM}{f}" alt="{n} wireframe" loading="lazy"></div>' for n, f in wires)}</div>
</div></section>

<section class="sl-sec" id="design"><div class="in">
  {sk_intro("It’s time to", "Design")}
  {sk_head("pen", "Final Design", "SKU removes that friction by offering an all-in-one product sourcing and syncing experience. This flow was central to making SKU actually useful.")}
</div></section>
<section class="sl-sec sk-pattern"><div class="in">
  {sk_split("Dashboard", "The dashboard provides a clean, minimalist overview with key metrics and navigation")}
  <img class="sk-shot sk-shot--md" src="{KM}dashboard.png" alt="SKU dashboard with account overview, orders graph and order summary" loading="lazy" data-reveal>
</div></section>
<section class="sl-sec sk-gray"><div class="in">
  <div class="sk-center"><span class="sk-pill sk-pill--lg">Main Features</span></div>
  <div class="sk-features"><ul>{''.join(f'<li>{x}</li>' for x in features)}</ul><img src="{KM}features-nav.png" alt="SKU sidebar navigation: Home, Order list, Products, All products, Import list, My products, My stores, Account settings" loading="lazy" data-reveal></div>
</div></section>
<section class="sl-sec sk-pattern"><div class="in">
  {sk_split("Store integration &amp; My Stores", "My Store has one click store integration process, individual store cards &amp; their analytics in most simple form")}
  <div class="sk-steps">{''.join(f'<div class="sk-step" data-reveal><h4>{t}</h4><img src="{KM}{f}" alt="{t}" loading="lazy"></div>' for t, f in steps)}</div>
</div></section>
<section class="sk-gif"><div class="in"><img src="{KM}store-flow.gif" alt="Animation of connecting a new store in My Stores" loading="lazy"></div></section>
<section class="sl-sec sk-gray"><div class="in">
  {sk_split("Product Discovery", "This feature has thousands of products but with all useful filters! User can also see SKU suggested “Selling price” for maximum profits!")}
  <div class="sk-two"><div data-reveal><h4>All products has categories &amp; sub categories to make it easier</h4><img class="sk-framed" src="{KM}discovery-1.png" alt="Product discovery grid with categories" loading="lazy"></div>
    <div data-reveal><h4>Bulk “add to import list” is an easy &amp; quick option to add products in “import list”</h4><img class="sk-framed" src="{KM}discovery-2.png" alt="Product discovery grid with bulk add to import list" loading="lazy"></div></div>
  <h4 class="sk-center sk-cap">Product details shows all important features and details about product</h4>
  <img class="sk-shot sk-shot--sm sk-framed" src="{KM}product-details.png" alt="Product details page with images, pricing, key features and similar products" loading="lazy" data-reveal>
</div></section>
<section class="sl-sec sk-pattern"><div class="in">
  {sk_split("Import list", "It is a space where users could personalize products before adding them to their stores.")}
  <div class="sk-import">
    <div class="sk-import-note"><p>I conceptualized the "Import List" (Playground) as a staging area where users could</p><p>Customize product titles and descriptions</p><p>Adjust pricing and profit margins</p><img src="{KM}importlist-note.png" alt="Import list product card with pricing tab" loading="lazy"></div>
    <img class="sk-import-main sk-framed" src="{KM}importlist.png" alt="Import list screen with products ready to customize" loading="lazy" data-reveal>
    <div class="sk-import-side"><p>Add to store button adds selected product to user’s store in one click!</p><img src="{KM}importlist-toast.png" alt="Product card with the Add to store button" loading="lazy"><p class="sk-added"><span>✓</span>Product added to store</p></div>
  </div>
</div></section>
<section class="sl-sec sk-gray"><div class="in">
  {sk_split("My Products", "It shows all the products user has added with all important measures like total profit, total sellings, store name &amp; status of product")}
  <img class="sk-shot sk-shot--md sk-framed" src="{KM}myproducts.png" alt="My Products table with profit, sales, store and status" loading="lazy" data-reveal>
</div></section>
<section class="sl-sec sk-pattern"><div class="in">
  {sk_split("Orders", "The Orders List provides a consolidated view of orders across all connected stores")}
  <div class="sk-two"><img class="sk-framed" src="{KM}orders-1.png" alt="Orders list" loading="lazy" data-reveal><img class="sk-framed" src="{KM}orders-2.png" alt="Order details" loading="lazy" data-reveal></div>
</div></section>
<section class="sk-story"><div class="in"><img src="{KM}deliver.png" alt="Storyboard: Rohan has a Shopify store, wants to expand without inventory, signs up with SKU, integrates his store, adds products to the import list and imports them to Shopify in one click, and is now a happy dropshipper" loading="lazy" data-reveal></div></section>

<section class="sl-sec" id="deliver"><div class="in">
  {sk_intro("Is it ready already?", "Deliver")}
  <p class="sk-center"><a class="sk-proto" href="{PROTO}" target="_blank" rel="noopener">Let’s Check Prototype {SK_EXT}</a></p>
</div></section>
<section class="sl-sec sk-gray" id="results"><div class="in">
  <h2 class="sk-h">Results</h2><p class="sk-sub">Although the project is at the prototype stage, the following outcomes are anticipated upon the app's launch:</p>
  <div class="sk-results">{''.join(f'<div class="sk-result" data-reveal><h3>{t}</h3><p>{d}</p></div>' for t, d in results)}</div>
</div></section>
<section class="sl-sec sk-gray sk-tight-top" id="takeaways"><div class="in">
  <h2 class="sk-h sk-center">Key takeaways</h2>
  <div class="sk-keys">{''.join(f'<div class="sk-note sk-note--lg" data-reveal>{SK_CMD}<p>{k}</p></div>' for k in keys)}</div>
</div></section>
<section class="sl-sec"><div class="in">
  <div class="sk-forward"><h2 class="sk-ghost">Looking Forward</h2><div><p>If continuing development on SKU, I would focus on enhancing the platform with</p><ul><li>AI-powered product recommendations based on store performance</li><li>Advanced analytics to identify trending products</li><li>Additional e-commerce platform integrations</li></ul></div></div>
</div></section>
<section class="sl-sec sk-concl-band" id="conclusion"><div class="in">
  <div class="sk-concl" data-reveal><h2>Conclusion</h2><p>This project demonstrates my approach to solving complex UX challenges through thorough research, iterative design,  creating intuitive solutions that feel natural to users.. The SKU platform showcases my ability to simplify technical complexity while creating powerful, flexible solutions for real business problems.</p></div>
</div></section>
</div>
</main>
{footer(root)}"""
    return head("SKU Platform · Rajvi Patel", "SKU Platform helps e-commerce sellers grow by connecting their stores and importing ready-to-sell products, no inventory needed.", root) + body


def offline():
    """Shown by the service worker (sw.js) when a page can't load because there's no internet.
    Everything is inside this one file, so it works with no connection at all."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#2c2a46">
<title>You're offline · Rajvi Patel</title>
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; height: 100%; }
  body { overflow: hidden; color: #f6f3fb; font-family: "Plus Jakarta Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
    background: linear-gradient(180deg, #2b2a4c 0%, #3b3352 45%, #4a405e 75%, #5a4a5c 100%); -webkit-tap-highlight-color: transparent; }
  canvas { position: fixed; inset: 0; width: 100%; height: 100%; display: block; cursor: crosshair; touch-action: manipulation; }
  .hills { position: fixed; left: 0; right: 0; bottom: 0; height: 26vh; pointer-events: none;
    background: radial-gradient(120% 100% at 20% 100%, #26233d 60%, transparent 61%), radial-gradient(110% 90% at 85% 100%, #2c2945 58%, transparent 59%); }
  .card { position: fixed; top: 7vh; left: 50%; transform: translateX(-50%); width: min(560px, calc(100% - 32px)); text-align: center; pointer-events: none; }
  h1 { margin: 0 0 10px; font-family: "Libre Baskerville", Georgia, serif; font-weight: 600; font-size: clamp(26px, 5vw, 40px); line-height: 1.15; }
  p { margin: 0; color: #d2cde0; font-size: clamp(15px, 2.4vw, 17px); line-height: 1.55; }
  .hand { display: block; margin-bottom: 10px; font-family: Georgia, serif; font-style: italic; color: #d6cbff; font-size: 17px; }
  .hud { position: fixed; left: 50%; bottom: 5vh; transform: translateX(-50%); display: flex; gap: 10px; align-items: center; }
  .pill { padding: 10px 18px; border-radius: 999px; font-size: 14px; font-weight: 600; white-space: nowrap;
    background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.22); -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px); }
  button.pill { cursor: pointer; color: #1c1730; font: inherit; font-weight: 600; background: linear-gradient(180deg, #f1ecff, #d9cffb); border-color: rgba(255,255,255,.6); }
  button.pill:focus-visible { outline: 3px solid #d6cbff; outline-offset: 3px; }
  .back { display: none; }
  body.online .back { display: inline-block; }
  body.online .retry { display: none; }
  @media (prefers-reduced-motion: reduce) { canvas { cursor: pointer; } }
</style>
</head>
<body>
<canvas id="sky" aria-hidden="true"></canvas>
<div class="hills" aria-hidden="true"></div>
<div class="card">
  <span class="hand">psst… you're offline</span>
  <h1>The internet wandered off</h1>
  <p>Catch the fireflies while it finds its way back. Tap or click them.</p>
</div>
<div class="hud">
  <span class="pill" id="score" role="status" aria-live="polite">0 caught</span>
  <button class="pill retry" type="button" id="retry">Try again</button>
  <button class="pill back" type="button" id="back">You're back online, open the page</button>
</div>
<script>
(() => {
  const c = document.getElementById("sky"), x = c.getContext("2d");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let W, H, dpr; const flies = [], pops = []; let caught = 0, best = 0;
  try { best = +localStorage.getItem("ffBest") || 0; } catch (e) {}
  const scoreEl = document.getElementById("score");
  const show = () => { scoreEl.textContent = caught + " caught" + (best ? " · best " + best : ""); };
  const size = () => { dpr = Math.min(devicePixelRatio || 1, 2); W = innerWidth; H = innerHeight; c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0); };
  const spawn = () => ({ x: Math.random() * W, y: H * (.3 + Math.random() * .55), r: 3 + Math.random() * 3,
    a: Math.random() * 6.28, s: (reduce ? .25 : .6) + Math.random() * (reduce ? .3 : .9), t: Math.random() * 6.28, life: 0 });
  // (re)place fireflies whenever the window size is known or changes, so they always fill the screen
  const fit = () => { size(); for (let i = 0; i < 14; i++) { if (!flies[i] || flies[i].x > W + 30 || flies[i].y > H || flies[i].y < H * .2) flies[i] = spawn(); } };
  fit(); addEventListener("resize", fit); addEventListener("load", fit);
  const catchAt = (px, py) => {
    let hit = -1, d = 1e9;
    flies.forEach((f, i) => { const dd = Math.hypot(f.x - px, f.y - py); if (dd < d) { d = dd; hit = i; } });
    if (hit < 0 || d > 34) return;
    const f = flies[hit]; pops.push({ x: f.x, y: f.y, k: 0 });
    flies[hit] = spawn(); flies[hit].life = 0;
    caught++; if (caught > best) { best = caught; try { localStorage.setItem("ffBest", best); } catch (e) {} }
    show();
  };
  c.addEventListener("pointerdown", (e) => catchAt(e.clientX, e.clientY));
  const tick = () => {
    x.clearRect(0, 0, W, H);
    flies.forEach((f) => {
      f.a += (Math.random() - .5) * .3; f.x += Math.cos(f.a) * f.s; f.y += Math.sin(f.a) * f.s * .7; f.t += .05; f.life = Math.min(1, f.life + .02);
      if (f.x < -20) f.x = W + 20; if (f.x > W + 20) f.x = -20; if (f.y < H * .25) f.a = Math.PI / 2; if (f.y > H * .9) f.a = -Math.PI / 2;
      const glow = (.55 + .45 * Math.sin(f.t)) * f.life;
      const g = x.createRadialGradient(f.x, f.y, 0, f.x, f.y, f.r * 6);
      g.addColorStop(0, "rgba(255,236,170," + (.9 * glow) + ")"); g.addColorStop(.25, "rgba(255,214,120," + (.35 * glow) + ")"); g.addColorStop(1, "rgba(255,214,120,0)");
      x.fillStyle = g; x.beginPath(); x.arc(f.x, f.y, f.r * 6, 0, 6.29); x.fill();
      x.fillStyle = "rgba(255,248,220," + glow + ")"; x.beginPath(); x.arc(f.x, f.y, f.r * .7, 0, 6.29); x.fill();
    });
    for (let i = pops.length - 1; i >= 0; i--) {
      const p = pops[i]; p.k += .04; if (p.k >= 1) { pops.splice(i, 1); continue; }
      x.strokeStyle = "rgba(214,203,255," + (1 - p.k) + ")"; x.lineWidth = 2; x.beginPath(); x.arc(p.x, p.y, 8 + p.k * 30, 0, 6.29); x.stroke();
      x.fillStyle = "rgba(255,248,220," + (1 - p.k) + ")"; x.font = "600 15px system-ui"; x.textAlign = "center"; x.fillText("+1", p.x, p.y - 14 - p.k * 24);
    }
    requestAnimationFrame(tick);
  };
  show(); tick();
  document.getElementById("retry").addEventListener("click", () => location.reload());
  document.getElementById("back").addEventListener("click", () => location.reload());
  const online = () => document.body.classList.toggle("online", navigator.onLine);
  addEventListener("online", online); addEventListener("offline", online);
})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    (ROOT / "work").mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(home())
    (ROOT / "about.html").write_text(about())
    (ROOT / "ai-lab.html").write_text(ai_lab())
    (ROOT / "offline.html").write_text(offline())
    projs = C.PROJECTS
    for i, cs in enumerate(C.CASE_STUDIES):
        nxt = projs[(i + 1) % len(projs)]
        page = {"sila": sila_page, "citylockers-kiosk": citylockers_page, "sku-platform": sku_page}.get(cs["slug"], lambda: case_study(cs, nxt))()
        (ROOT / "work" / f"{cs['slug']}.html").write_text(page)
    print("built", 4 + len(C.CASE_STUDIES), "pages")
