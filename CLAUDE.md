# MyVideoPlayer

A one-page portfolio of the user's video work, built from the mockup `cursor-demo.jpg`. A large hero `<video>` sits above a strip of three thumbnails, and clicking a thumbnail plays that video in the hero. It's plain HTML, CSS and JavaScript, with no framework, no build step and no npm. It's developed locally and will be hosted on Vercel from the user's git repo.

This is a fresh project. Don't reuse code, assets or decisions from the user's older video-player projects. Use only the assets the user points to.

## Files

```
index.html      header (logo, nav, hamburger), hero video, thumbnail strip, footer
css/style.css   all styles; colour and size tokens on :root
js/main.js      thumbnail → hero playback, highlight, autoplay, phone menu
dev-server.py   local server with HTTP Range support (development only)
images/         background.jpg
video/          sue-vid1.mp4, sue-vid2.mp4, sue-vid3.mp4
posters/        sue-vid*-thumb.png (143x105 thumbnails), sue-vid*-frame.jpg (1200x880 starting frames)
README.md       overview, how to run, video prep, milestones
```

`.gitignore` keeps these local only, as the user chose: `cursor-demo.jpg` (the mockup), `video/sample-*` and `posters/sample-*` (unused), `.DS_Store` and `.claude/`. Don't commit them.

## Run locally

```bash
python3 dev-server.py
```

This serves http://localhost:8000. Some things to know:

- **Don't use `python3 -m http.server`.** It ignores Range requests, and Safari won't play `<video>` without them. `dev-server.py` answers them with 206 (and 416 past the end) and sends `Cache-Control: no-cache`, so edits show on a plain reload.
- **Start the server in a Terminal-panel tab, not with `preview_start`.** macOS privacy blocks the app's preview runner from reading `~/Desktop`. `.claude/launch.json` only attaches the preview to the server already running on port 8000.
- **Editing `index.html` makes the app open a `file://` preview tab.** Relative assets don't load there. Close it and use the `localhost:8000` tab.

## Design (from the 1200x800 mockup)

Keep desktop faithful to the mockup. The measured sizes are:

- **Header and footer:** 68px bars of `--glass` (`rgba(255,255,255,0.62)`) over `images/background.jpg`.
- **Logo:** "MyVideoPlayer" in Courier New, bold, 30px, `--logo`, 46px from the left.
- **Nav:** About, Events and Contact in Helvetica 18px, `--ink`. They're right-aligned so Contact ends 132px from the right, where Sign in ended in the mockup.
- **Hero:** 656px wide with an 8px `--navy` (`#131c55`) border and a slight drop shadow, starting at y=88. The video is 640px wide at 15:11, which is the shape of the 1472x1080 videos.
- **Thumbnail strip:** `--navy-strip` (`#143055`), the same width as the hero (656px). It has 7px/16px padding, 22px below the hero. The three 143x105 thumbnails are **centred** with 14px gaps.
- **Footer text:** "My Contact Information – My Social Media Links", Helvetica 14px, centred. (The mockup's "Informatrion" typo was fixed.)
- **Centring:** the hero and strip are centred on the page. The mockup's slight right offset was treated as accidental.
- **Colours:** use the tokens in `:root` (`--navy`, `--navy-strip`, `--logo`, `--ink`, `--sky`, `--glass`) rather than adding new hex values.
- **Background:** it sits on a fixed `body::before` layer, because iOS Safari ignores `background-attachment: fixed`.

**Responsive (M4):**
- The hero and strip shrink together inside 16px `--gutter`s, and the thumbnails scale down at 143:105 (94x69 at 375px).
- Header padding scales from 46px/132px with `clamp()`.
- **Breakpoint at 600px.** At that width and below, the nav collapses behind a 44x44 hamburger into a frosted dropdown under the header. It's driven only by `aria-expanded` on `.menu-toggle`, and closes on a link click, an outside click, Escape (focus returns to the button) or widening past 600px.

**Deliberately left out:** there's no **Sign in** link, and it isn't in the plan. About, Events, Contact and the footer links are placeholders (`href="#"`).

## Player behaviour (js/main.js)

- Each `.thumb` button carries `data-video` and `data-poster`. Clicking one sets the hero's `poster` and `src`, then plays it.
- **Call `hero.play()` synchronously inside the click handler.** Safari only allows playback started directly by a user action.
- Clicking the thumbnail that's already playing restarts it (`currentTime = 0`) instead of reloading it.
- The playing thumbnail gets `aria-current="true"`, which also draws its `--sky` ring. Focus is a white outline (offset 4px) so it shows on the navy strip. The visually hidden `#now-playing` live region announces "Now playing: Video N".
- The hero is `muted playsinline`, with no controls (as in the mockup). `sue-vid1` autoplays muted on load, unless `prefers-reduced-motion: reduce` is set. The videos have no audio track and don't loop.
- The starting frames preload after `load`, so switching never shows a blank player.
- The thumbnail alt text is "Video 1/2/3" until the user supplies real titles.

## Videos

The current files are H.264 High, yuv420p, 24fps, no audio, and fast start (`moov` before `mdat`). Any new video should match. To fix a file that isn't fast start:

```bash
ffmpeg -i input.mp4 -c copy -movflags +faststart output.mp4
```

Each video needs a 143x105 `-thumb.png` and a 15:11 `-frame.jpg` in `posters/`, plus a `<li><button class="thumb">` in `index.html`.

## Milestones

Each milestone ends with a commit whose message starts with its ID.

- [x] **M1 Setup:** folder structure, page skeleton, `.gitignore`, README, `git init`
- [x] **M2 Layout:** desktop layout measured from the mockup
- [x] **M3 Player:** thumbnail click plays in the hero, highlight, keyboard, live region, muted autoplay
- [x] **M4 Responsive:** tablet and phone layouts, hamburger menu; strip set to hero width with centred thumbnails
- [x] **M5 Local testing:** `dev-server.py` with Range support; checked in Chromium (play, switch, seek) and Safari (range requests seen in the server log)
- [ ] **M6 Deploy:**
  - The user creates the GitHub repo. Add the remote and push `main`.
  - Connect Vercel as a static site (Framework Preset: Other, no build command).
  - Keep dev-only files off the live site with a `.vercelignore`: `dev-server.py`, `CLAUDE.md`, `README.md`.
  - Check the live URL.

**Still to verify:**
- A visual check of playback in Safari.
- A real phone.
- Firefox, which isn't installed on this Mac.
- The reduced-motion path, which the preview can't emulate.

## Working agreements

- Ask clarifying questions **one at a time**.
- Verify changes in the browser preview at 1200x800 (desktop) and 375px (phone) before committing. Check 768px for tablet when the layout changes.
- Asset paths stay relative and must match the filenames' case exactly, because Vercel's filesystem is case-sensitive and macOS isn't.
