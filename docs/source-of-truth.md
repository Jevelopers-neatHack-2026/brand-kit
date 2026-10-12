# Source-of-truth index

Where each part of the TicketStub brand is authoritative **today**. The full per-file record (type, source/output relation, canonical authority, owner role, approval and provenance status) is [`inventory/brand-inventory.json`](../inventory/brand-inventory.json); `make check-inventory` fails if it drifts from the tracked files. Baseline: `main` at `74bc86f`, 2026-10-12.

**Approval and provenance are unknown unless stated.** No file here is recorded as approved for release. README says the identity is not ratified; nothing in this index changes that. Rights, tool and prompt provenance for the images, and redistribution policy, are left `unknown` for [BK-06](https://github.com/Jevelopers-neatHack-2026/brand-kit/issues/7).

## Source-of-truth map

| Topic | Authoritative path | Derived or generated | Notes |
|---|---|---|---|
| Logos and marks | [`tools/build_logos.py`](../tools/build_logos.py) | [`logo/`](../logo/) (14 SVGs) | Edit the script and regenerate; never hand-edit `logo/*.svg`. The script reads `fonts/Fraunces[SOFT,WONK,opsz,wght].ttf`. |
| Iconography | none | none | No icon system exists. See [Iconography](#iconography). |
| Colour tokens | [`tokens/tokens.json`](../tokens/tokens.json) | [`tokens/tokens.css`](../tokens/tokens.css), [`tokens/tailwind.preset.js`](../tokens/tailwind.preset.js) | The derivation is stated in the file headers, but no generator is tracked, so drift is not machine-checked. |
| Type tokens and fonts | [`tokens/tokens.json`](../tokens/tokens.json), `fonts/Fraunces[SOFT,WONK,opsz,wght].ttf`, `fonts/InterTight[wght].ttf` | same outputs as above | Licences: [Fraunces](../fonts/Fraunces-OFL.txt), [Inter Tight](../fonts/InterTight-OFL.txt). Upstream version and checksum are not recorded. |
| Spacing and layout | [`tokens/tokens.json`](../tokens/tokens.json) | same outputs as above | No separate layout spec exists. |
| Usage guidance | [`SPEC.md`](../SPEC.md), [`docs/logo.md`](logo.md), [`docs/voice.md`](voice.md), [`docs/imagery.md`](imagery.md), [`docs/motion-sound-haptics.md`](motion-sound-haptics.md), [`docs/material-foil.md`](material-foil.md) | board: [`index.html`](../index.html) | `SPEC.md` holds the prose values, `tokens.json` the machine values; they are not cross-checked. |
| Provenance | [`fonts/Fraunces-OFL.txt`](../fonts/Fraunces-OFL.txt), [`fonts/InterTight-OFL.txt`](../fonts/InterTight-OFL.txt), [`inventory/brand-inventory.json`](../inventory/brand-inventory.json) | none | Only the font licence texts exist. Everything else is `unknown`. |
| Releases | none | none | No versions, packages or release notes. Pending [BK-03B](https://github.com/Jevelopers-neatHack-2026/brand-kit/issues/14). |

## Classifications

| Class | Meaning | Examples |
|---|---|---|
| `canonical-source` | Edit here | `tools/build_logos.py`, `tokens/tokens.json`, font files |
| `generated` | Produced from a source; do not hand-edit | `logo/*.svg`, `tokens/tokens.css`, `tokens/tailwind.preset.js` |
| `guideline` | Human guidance and the brand board | `SPEC.md`, `docs/*.md`, `index.html` |
| `reference-only` | Inspiration or licence text; not an export candidate | `references/*.webp` (rights unknown), font OFL texts |
| `release_class` | `candidate-unapproved`, `reference-only` or `internal`. None is approved. | |

## Actual versus proposed paths

[`OWNERSHIP.md`](architecture/OWNERSHIP.md) proposes a future layout and states that it does not relocate existing assets. **Decision: current paths stay canonical; no file moves in BK-01.**

| Proposed | Actual today | Decision and rationale | If moved later |
|---|---|---|---|
| `identity/` | `logo/`, `tools/build_logos.py` | Keep. The script's output path, `index.html`, docs links and consumer copies in getticketstub.com `public/brand` all use `logo/`. | Keep `logo/` as an alias for one release; update `OUT` in the script and board paths. |
| `tokens/` | `tokens/` | Matches. | n/a |
| `guidelines/` | `SPEC.md`, `docs/*.md` | Keep. README, SPEC and the board link these. | Leave redirect stubs. |
| `components/` | none | Nothing to move. Board patterns need a named application owner first. | n/a |
| `licenses-and-provenance/` | font OFL texts in `fonts/`, the inventory | Keep OFL texts beside the fonts. BK-06 may add a ledger. | n/a |
| `releases/` | none | Nothing exists yet. | n/a |

Imports affected by any future move: the README `@import "brand-kit/tokens/tokens.css"`, the Tailwind `require("@ticketstub/brand-kit/tokens/tailwind.preset.js")`, `index.html` relative `src`/`url()` paths, and consumer copies. These are listed in `path_map` in the inventory.

## Iconography

**Scope: unknown.** The repository has no icon library or icon guidance. `logo/favicon.svg` and `logo/app-icon.svg` are logo variants, and the demo icons in `index.html` are board illustrations. [`OWNERSHIP.md`](architecture/OWNERSHIP.md) lists "icon treatment" as a responsibility without a source. Three outcomes are open: owned guidance here, a future asset family, or consumer-owned (getticketstub.com). None is chosen here; the question is handed to BK-02 and the consumer owners.

## Repository status and open handoffs

- **Visibility (stale text, not edited here).** `OWNERSHIP.md` line 3 says the repository is *private* as verified 2026-10-10. `gh repo view` on 2026-10-12 reports `PUBLIC`. `OWNERSHIP.md` is a governance document owned by BK-07, so BK-01 records the correction here and leaves the edit to that owner. No repository setting was changed.
- **PR #3 (open, not merged).** It repoints the `ticket-studio` links in `README.md`, `SPEC.md`, `tokens/tokens.json` and `docs/material-foil.md`, and proposes "always on paper". Its targets exist only on getticketstub.com branches (#4, #20) and returned 404 on that repository's `main` on 2026-10-10. `main` still points at the nonexistent `ticket-studio`. The direction change needs a BK-02 decision record. BK-01 does not merge or reimplement it.
- **PR #2 (merged).** Its edition-ownership handoff (owner confirmation for the `ticket-studio` link) is preserved unchanged.
- **Consumer copies.** README's claim that getticketstub.com carries byte-identical logo copies was not verified.

## Checks

See [inventory checks](inventory-checks.md): `make check-inventory`, `make check-links`, `make test`.
