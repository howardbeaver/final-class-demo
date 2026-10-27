# MyVideoPlayer

A one-page portfolio of my video work. A large hero player sits above a strip of
thumbnails, and clicking a thumbnail plays that video in the hero.

Plain HTML, CSS and JavaScript, with no framework and no build step.

Live at https://final-class-demo.vercel.app. Every push to `main` redeploys on Vercel.

## Files

```
index.html      the page
css/style.css   styles
js/main.js      player behaviour
dev-server.py   local server with Range support (development only)
images/         background.jpg
video/          sue-vid1.mp4, sue-vid2.mp4, sue-vid3.mp4
posters/        sue-vid*-thumb.png (thumbnails), sue-vid*-frame.jpg (starting frames)
```

## Run locally

```bash
python3 dev-server.py
```

Then open http://localhost:8000. Use this server rather than
`python3 -m http.server`: Safari only plays video from a server that answers
Range requests, and this one does. It also tells the browser to recheck files
on every reload, so edits show up straight away.

## Videos

Keep new videos as H.264 MP4 with the index at the start ("fast start"), so
playback can begin before the whole file downloads:

```bash
ffmpeg -i input.mp4 -c copy -movflags +faststart output.mp4
```

## Milestones

- **M1 Setup:** folder structure, page skeleton, git repository
- **M2 Layout:** header, hero, thumbnail strip, footer and background, matched to the mockup
- **M3 Player:** thumbnail click plays it in the hero, active highlight, keyboard access, muted autoplay
- **M4 Responsive:** tablet and phone layouts
- **M5 Local testing:** local server with video streaming, cross-browser checks
- **M6 Deploy:** GitHub and Vercel
