// MyVideoPlayer behaviour: clicking a thumbnail plays that video in the hero.

const hero = document.getElementById('hero-video');
const nowPlaying = document.getElementById('now-playing');
const thumbs = [...document.querySelectorAll('.thumb')];
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

// Mark the playing thumbnail. aria-current also draws its highlight (see style.css).
function setActive(thumb) {
  for (const t of thumbs) {
    if (t === thumb) {
      t.setAttribute('aria-current', 'true');
    } else {
      t.removeAttribute('aria-current');
    }
  }
}

function select(thumb) {
  if (hero.getAttribute('src') === thumb.dataset.video) {
    // Already loaded: restart it rather than reloading the file.
    hero.currentTime = 0;
  } else {
    hero.poster = thumb.dataset.poster;
    hero.src = thumb.dataset.video;
  }
  setActive(thumb);
  nowPlaying.textContent = `Now playing: ${thumb.querySelector('img').alt}`;
}

// play() rejects when a newer click interrupts loading, or autoplay is refused.
// Neither needs handling: the poster stays up and the next click plays.
function play() {
  hero.play().catch(() => {});
}

for (const thumb of thumbs) {
  thumb.addEventListener('click', () => {
    select(thumb);
    // Call play() synchronously inside the click: Safari only allows playback started by the user.
    play();
  });
}

// First video: highlighted, and started muted unless reduced motion is requested.
setActive(thumbs[0]);
if (!reduceMotion.matches) {
  play();
}

// Fetch the other starting frames once the page is up, so switching never shows a blank player.
window.addEventListener('load', () => {
  for (const t of thumbs) {
    new Image().src = t.dataset.poster;
  }
});
