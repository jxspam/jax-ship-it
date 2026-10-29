# Don't Just Prompt It. Ship It.

The AdaL workshop deck, live at [jax-ship-it.vercel.app](https://jax-ship-it.vercel.app).

## Use it

- `site/index.html` is the finished deck: one self-contained file, open it in a browser.
- Keys: arrows or space to move, `f` fullscreen, `t` start or pause the timer, `r` reset it.
- Every slide shows a QR code (top right) that opens that exact slide on the attendee's phone.

## Make your own

- `base.css`, `extra.css`, `theme.css`: the design style (colours, type, layout).
- `deck.js`: navigation, timer, per slide QR codes.
- `build.py`: assembles the slides into `site/index.html` (`python3 build.py`). It reuses slides from an earlier deck through `perth_slides.py`, so for your own deck swap those slides for yours.
- `b2b.json`: the Part 3 example slides.
- `site/api/`: optional live Q&A backend (Vercel functions plus Upstash Redis, `ADMIN_KEY` env var for presenter actions).

## Deploy

```
cd site && vercel deploy --prod
```
