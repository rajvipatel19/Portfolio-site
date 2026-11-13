"""Generates the static pages of the portfolio.

Edit text in content.py, then run:  python3 build.py
(Or edit the generated .html files directly — both are fine.)
"""
from pathlib import Path
from html import escape
import content as C

ROOT = Path(__file__).parent

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
<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400;1,700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css">
</head>
<body>
<div class="page-fade" aria-hidden="true"></div>
<div class="ambient" aria-hidden="true"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div></div>
<div class="grain" aria-hidden="true"></div>
"""


def nav(root, active):
    def link(href, label, key, extra=""):
        cls = ' class="is-active" aria-current="page"' if key == active else ""
        return f'<a href="{root}{href}"{cls}>{label}{extra}</a>'
    return f"""<header class="nav">
  <a class="logo" href="{root}index.html" aria-label="Rajvi Patel — home"><img class="logo-avatar" src="{root}assets/img/avatar.svg" alt="" width="42" height="42"><span class="logo-name">Rajvi <span class="logo-last">Patel</span></span></a>
  <nav class="nav-menu glass" aria-label="Main">
    <div class="nav-links">
      {link("about.html", "About", "about")}
      {link("art-lab.html", "Art Lab", "art")}
      {link("index.html#work", "Projects", "work")}
      <a href="{C.LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
      <a class="nav-resume nav-resume--menu" href="{C.RESUME}" target="_blank" rel="noopener">Resume {ARROW_UR}</a>
    </div>
    <span class="nav-divider" aria-hidden="true"></span>
    <a class="nav-resume" href="{C.RESUME}" target="_blank" rel="noopener">Resume {ARROW_UR}</a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false"><span></span></button>
  </nav>
</header>
"""


def footer(root):
    return f"""<footer class="footer" id="contact">
  <div class="wrap">
    <div class="footer-top">
      <h2 data-reveal>Let's make it<br>easy to use <span class="hand">together</span></h2>
      <div class="footer-links" data-reveal style="--d:.1s">
        <a class="btn magnetic" href="{root}index.html#call" data-cal>Book a call {ARROW}</a>
        <a class="btn magnetic" href="{C.LINKEDIN}" target="_blank" rel="noopener">LinkedIn {ARROW_UR}</a>
        <a class="btn magnetic" href="{C.RESUME}" target="_blank" rel="noopener">Resume {ARROW_UR}</a>
      </div>
    </div>
  </div>
  <div class="desk" aria-label="My desk — drag things around">
    <div class="desk-surface"></div>
    <div class="desk-hint">psst… you can move things around on my desk ☕</div>
    {desk_items()}
    <div class="wrap footer-bottom">
      <span>© <span data-year>2026</span> Rajvi Patel · Dubai</span>
      <span class="hand">built with code &amp; lots of coffee</span>
    </div>
  </div>
</footer>
<script src="{root}assets/js/main.js"></script>
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
def home():
    root = ""
    cards = []
    for i, p in enumerate(C.PROJECTS):
        wide = " card--wide" if p.get("wide") else ""
        tags = "".join(f'<span class="chip">{t}</span>' for t in p["tags"])
        cards.append(f"""<a class="card glass tilt{wide}" href="work/{p['slug']}.html" data-video="{p.get('video','')}" data-reveal style="--d:{i*0.08:.2f}s">
  <div class="card-media">{scene(p['scene'])}</div>
  <div class="card-body">
    <div class="card-meta">{p['meta']} <span class="badge{' badge--soft' if p['badge']=='MVP' else ''}">{p['badge']}</span></div>
    <h3>{p['name']} <span class="go">{ARROW_UR}</span></h3>
    <p>{p['summary']}</p>
    <div class="tags">{tags}</div>
  </div>
</a>""")
    shots = "".join(f'<div class="shot glass"><div class="shot-inner"><span class="ph">visual {n:02d}</span></div></div>' for n in range(1, 9))
    shots2 = "".join(f'<div class="shot glass"><div class="shot-inner"><span class="ph">visual {n:02d}</span></div></div>' for n in range(9, 17))
    sparkles = "".join(f'<span class="sparkle" style="left:{l}%;top:{t}%;animation-delay:{d}s;width:{s}px;height:{s}px">{SPARK}</span>'
                       for l, t, d, s in [(12, 22, 0, 10), (78, 18, 1.2, 14), (64, 40, 2.1, 8), (30, 58, .6, 12), (88, 62, 1.8, 10), (48, 14, 2.6, 9)])
    body = f"""{nav(root, 'work')}
<main>
<section class="hero">
  <div class="hero-media" aria-hidden="true">
    <div class="mesh"></div>
    <video autoplay muted loop playsinline preload="auto" poster=""><source src="assets/media/hero.mp4" type="video/mp4"></video>
    {sparkles}
    <span class="video-note">← your hero video plays here</span>
  </div>
  <div class="wrap hero-inner">
    <span class="hand hi" data-reveal>hi! i'm Rajvi ✿</span>
    <h1 class="split">I design products that are <em>easy to understand</em> &amp; use.</h1>
    <div class="hero-side" data-reveal style="--d:.35s">
      <p>{C.INTRO}</p>
      <div class="hero-cta">
        <a class="btn btn--dark magnetic" href="#work">See my work {ARROW}</a>
        <a class="btn magnetic" href="#call" data-cal>Book a call {ARROW}</a>
      </div>
    </div>
  </div>
  <div class="scroll-cue" aria-hidden="true"><span></span>scroll</div>
</section>

<section class="section" id="work">
  <div class="wrap">
    <div class="section-head">
      <div data-reveal><span class="hand">case studies, start to finish</span><h2>Selected work</h2></div>
      <p data-reveal style="--d:.1s">Fintech, travel tech and B2B commerce. Research-led, shipped with small teams, written up in plain words.</p>
    </div>
    <div class="work-grid">
      {''.join(cards)}
    </div>
  </div>
</section>

<section class="ticker-section" aria-label="Visual journey">
  <div class="ticker-head wrap" data-reveal><span class="hand">a sneak peek of my</span><h2>visual journey</h2></div>
  <div class="ticker"><div class="ticker-track">{shots}{shots}</div></div>
  <div class="ticker reverse"><div class="ticker-track">{shots2}{shots2}</div></div>
</section>

<section class="cd-section">
  <div class="wrap cd-wrap">
    <div class="cd-copy" data-reveal>
      <span class="hand">before you scroll on…</span>
      <h2>Here's a song for you while you see what I do</h2>
      <p>Tap the CD to play. It's on my repeat list while I design.</p>
      <div class="now-playing glass"><span class="eq"><i></i><i></i><i></i><i></i></span><span>Tap the CD to play</span></div>
      <div class="spotify-dock"></div>
    </div>
    <div class="cd-stage" data-reveal style="--d:.15s">
      <div class="cd-case glass"><span class="case-label">rajvi's<br>design mix ♫</span></div>
      <div class="cd" role="button" tabindex="0" aria-label="Play song">
        <div class="cd-label"><span>side A</span><small>press play</small></div>
      </div>
      <div class="cd-hint">tap me! ↖</div>
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
          <a class="btn btn--dark magnetic" href="{C.LINKEDIN}" target="_blank" rel="noopener">LinkedIn {ARROW_UR}</a>
          <a class="btn magnetic" href="{C.RESUME}" target="_blank" rel="noopener">Resume {ARROW_UR}</a>
        </div>
        <p class="call-mail">or email me at <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
      </div>
      <div class="cal-frame">
        <div class="cal-placeholder">
          <div class="cal-top"><span class="cal-month">Month</span><span class="chip">30 min · Google Meet</span></div>
          <div class="cal-grid"></div>
          <div class="cal-slots"></div>
          <div class="cal-note">Preview only. Your real calendar (Cal.com) appears here once the link is added.</div>
        </div>
      </div>
    </div>
  </div>
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


# ---------------------------------------------------------------- about / art lab
def about():
    root = ""
    facts = "".join(f'<span class="chip">{f}</span>' for f in C.ABOUT_FACTS)
    paras = "".join(f"<p>{p}</p>" for p in C.ABOUT_BIO)
    body = f"""{nav(root, 'about')}
<main>
<section class="about-hero">
  <div class="wrap about-grid">
    <div class="polaroid-wrap" data-reveal>
      <div class="polaroid"><span class="tape"></span>{img_ph('your photo', '4/5')}<span class="caption">that's me! ✿</span></div>
      <span class="sticker" style="right:-24px;top:18%;width:70px">{desk_sticker('star')}</span>
      <span class="sticker" style="left:-26px;bottom:22%;width:60px;animation-delay:-2s">{desk_sticker('heart')}</span>
    </div>
    <div class="about-copy">
      <span class="eyebrow" data-reveal>About me</span>
      <h1 class="split">From dental chairs to <em>design systems.</em></h1>
      <div data-reveal style="--d:.3s">{paras}</div>
      <div class="about-facts" data-reveal style="--d:.4s">{facts}</div>
      <div class="hero-cta" data-reveal style="--d:.5s">
        <a class="btn btn--dark magnetic" href="{C.RESUME}" target="_blank" rel="noopener">Resume {ARROW_UR}</a>
        <a class="btn magnetic" href="index.html#call" data-cal>Book a call {ARROW}</a>
      </div>
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


def art_lab():
    root = ""
    body = f"""{nav(root, 'art')}
<main>
<section class="soon-page">
  <div class="wrap">
    <div class="soon-card glass" data-reveal style="margin-inline:auto">
      <div class="palette-dots"><i style="background:var(--lav)"></i><i style="background:var(--butter);animation-delay:.2s"></i><i style="background:#ffc7d8;animation-delay:.4s"></i><i style="background:#cfe9de;animation-delay:.6s"></i></div>
      <span class="hand" style="font-size:26px">still mixing the colours…</span>
      <h1>Art Lab</h1>
      <p>A space for visual experiments, AI explorations and things I make for fun. Coming soon.</p>
      <a class="btn magnetic" href="index.html#work">Meanwhile, see my work {ARROW}</a>
    </div>
  </div>
</section>
</main>
{footer(root)}"""
    return head("Art Lab · Rajvi Patel", "Visual experiments by Rajvi Patel — coming soon.", root) + body


if __name__ == "__main__":
    (ROOT / "work").mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(home())
    (ROOT / "about.html").write_text(about())
    (ROOT / "art-lab.html").write_text(art_lab())
    projs = C.PROJECTS
    for i, cs in enumerate(C.CASE_STUDIES):
        nxt = projs[(i + 1) % len(projs)]
        (ROOT / "work" / f"{cs['slug']}.html").write_text(case_study(cs, nxt))
    print("built", 3 + len(C.CASE_STUDIES), "pages")
