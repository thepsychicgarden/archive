# The Psychic Garden — Flyer Archive

A static image gallery of every flyer in `Psychic Garden/Sorted`, ready for GitHub Pages.

- `index.html` — the whole site (search, year filters, lightbox with ←/→/Esc and swipe, shareable `#links` to individual flyers)
- `images/` — web-sized copies (max 2000px, WebP)
- `thumbs/` — grid thumbnails (640px wide, WebP)
- `_build/` — scripts that regenerate the site when you add flyers (harmless if published)

## Publish on GitHub Pages

1. Create a new public repo on GitHub (e.g. `psychic-garden-flyers`).
2. In Terminal:
   ```sh
   cd ~/Pictures/"Psychic Garden"/Sorted/gallery-site
   git init -b main
   git add .
   git commit -m "Flyer gallery"
   git remote add origin https://github.com/YOUR-USERNAME/psychic-garden-flyers.git
   git push -u origin main
   ```
3. On GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, branch `main`, folder `/ (root)`. Save.
4. After a minute it's live at `https://YOUR-USERNAME.github.io/psychic-garden-flyers/`.

## Adding new flyers

Drop new images into `Sorted/` using the `YYYY-MM-DD Lineup, Names.ext` naming, then:
```sh
cd ~/Pictures/"Psychic Garden"/Sorted/gallery-site/_build
python3 build.py 0 100000 && python3 gen.py
```
(Requires Python 3 with Pillow: `pip3 install pillow`.) Then commit and push again.
