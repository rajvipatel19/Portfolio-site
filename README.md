# Rajvi Patel — Portfolio

Static site (HTML/CSS/JS). No build step needed to deploy.

## Deploy to Vercel (free)
1. Go to vercel.com → sign up with Google/GitHub.
2. Dashboard → "Add New…" → "Project" → drag this whole folder onto the upload area
   (or install the CLI and run `npx vercel` inside this folder).
3. Framework preset: "Other". Leave build settings empty. Click Deploy.
4. You get a free URL like rajvi-portfolio.vercel.app.

## Where to edit
- Text: `content.py` → then run `python3 build.py` (or edit the .html files directly)
- Colours / fonts: top of `assets/css/style.css`
- Calendar + Spotify song: top of `assets/js/main.js` (SITE settings)

## Adding media (put files in assets/media/)
- Hero video: `assets/media/hero.mp4` (plays automatically, muted, looping)
- Case study card videos: add `"video": "assets/media/sila.mp4"` to a project in content.py
- Images: replace any `<div class="img-ph">…</div>` with `<div class="img-ph"><img src="../assets/media/your-image.png" alt="…"></div>`
