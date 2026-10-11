# Motion, sound and haptics

Every interaction should feel like handling paper. Tokens are in `tokens/tokens.json` under `motion`.

## Motion

| Token | Value | Use |
|---|---|---|
| `track` | 80 ms linear | Stub follows the finger, mouse or gyro |
| `quick` | 160 ms standard | Floating toolbar and chips appear |
| `base` | 240 ms standard | Sheets, toasts, style swap crossfade |
| `settle` | 380 ms `flip` (.45,0,.55,1) | Tilt returns to rest; card flip. The curve is symmetric so the face swap lands edge-on. |
| `reveal` | 600 ms `enter` | Stub lands after printing; stub pins to the wall |
| `shutter` | 320 ms | Print-complete flash: RGB split fades out with (1-p)^2.6 |
| `print-sweep` | 2600 ms loop | Foil sweep across the stub while it prints and researches |

- **Spring for drag-spin and swipe:** stiffness 0.055, damping 0.9, stepped at a fixed 60 Hz, maximum velocity 34. A fixed step means the stub settles in the same time on a 60 Hz phone and a 120 Hz laptop.
- **Tilt:** at most ±11° with 1400 px perspective.
- **Foil and tilt never step.** Pointer and gyro inputs are eased every frame (tilt τ 110 ms, glow in 400 ms and out 600 ms) instead of being set directly. See "Rules: foil must never pop" in `material-foil.md`.
- **Signature move: the tear.** Drag along the perforation. The stub follows with slight resistance; past 60% it rips free, flies to the wall, rotates to a random angle between -4° and 4°, and pins.
- **Reduced motion:** no tilt, spin or glitch. Foil holds a still sheen (`glow` 0.45), and transitions become instant cross-fades.

## Sound

Sound is **on by default**, with a mute toggle always visible in the top bar. Synthesize every sound live with the Web Audio API, built the way **[cuelume.dev](https://cuelume.dev/)** builds its sounds (rules below). Keep each one under 600 ms (the printer loop is the exception), mixed quietly at -18 LUFS or below.

| Event | Character |
|---|---|
| Ticket dropped | Soft paper slide, short |
| Printing (while the stub feeds) | Thermal head stepping the paper: soft ticks in short runs, timed with the feed, over a faint paper whisper. No hum or steady drone (it reads as a microwave); very quiet |
| Print complete | Single crisp paper snap together with the shutter flash |
| Style shuffle | Card flick |
| Remix | Short shuffle and riffle |
| Tap to edit | Very soft tick |
| Flip to back | Paper turn |
| Perforation drag | Granular tearing that follows drag speed |
| Tear complete | Clean rip, then a pin "thunk" on landing |
| Add to cart | Rubber stamp |

- **Browser rule:** audio can only start after the first user gesture. The drop or tap that starts a stub unlocks it.

### Rules: sounds must never be harsh or interchangeable

The first build got both wrong. Every cue was a 1–2 ms burst of high-passed noise with an exponential attack, so they all sounded like the same sharp click. These rules come from how cuelume builds its sounds (MIT, [source](https://github.com/danielwh2/cuelume)):

1. **Swell in, don't click.** Every layer rises along a straight line (1–6 ms for strikes, 50+ ms for air), then dies away exponentially. An exponential attack stays silent and then jumps in, which is heard as a late second hit.
2. **No unfiltered noise, and nothing centred above 5 kHz.** Noise is always band- or low-passed at the material's hardness: felt about 1 kHz, card about 2.4 kHz, a hard mallet about 3 kHz.
3. **Struck objects, not test tones.** Tones are sines at the modes of a real object (free bar 1 / 2.76 / 5.40, marimba bar 1 / 3.99). Higher modes die out faster (decay ∝ 1/ratio). A knock is a sine struck 1.6× sharp that drops to its pitch in 18 ms.
4. **One shared room.** Every cue sends about -22 dB into one short stereo room (8 ms to the first reflection, 250 ms tail, walls low-passed at 3.5 kHz), then goes through one limiter. Results (success) send twice as much.
5. **One job, one shape.** Pick by the job (tap, select, toggle, open, close, drop, success, stamp, flick, flip, tear, pin, print). Each has its own layers. Never make a cue by changing the volume or EQ of another.
6. **Alive, not random.** Frequent cues vary each strike by about 1–3% in pitch and 10% in level, and each layer's ring varies by up to 10%. Outcomes play the same every time. A cue that repeats within 70–220 ms gets lighter (up to -22% level, -25% length). Each cue plays one voice at a time, so a new play fades the last one out over 80 ms instead of stacking on it.
7. **Emphasis by arrangement.** "Subtle" (frequent actions) drops the ornament layers, and "strong" (rare, important) adds one low layer of its own.

The reference implementation is `getticketstub.com/src/customer/studio/feedback.ts`, with an audition board at `/parts`.

## Haptics

Use `navigator.vibrate` on Android. iOS Safari doesn't support web vibration, so on iOS the sound carries the feedback, and a native wrapper can map these to `UIImpactFeedbackGenerator` later.

| Event | Pattern (ms) |
|---|---|
| Drop accepted | `[12]` |
| Print complete | `[18, 40, 28]` |
| Style shuffle | `[8]` |
| Perforation tick (per hole crossed) | `[4]` |
| Tear complete | `[30, 30, 60]` |
| Pin to wall | `[20]` |
| Low-confidence chip appears | none (visual only) |

## Gyro

On mobile, phone tilt drives the foil light and parallax. iOS needs `DeviceOrientationEvent.requestPermission()` from a user gesture, so ask on the first tap on the stub, not on load. Smooth with a short low-pass filter (α ≈ 0.15) and clamp to the same ±11°.
