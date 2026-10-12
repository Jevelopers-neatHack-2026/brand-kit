# Inventory checks

Standard library only; Python 3.9 or newer. Nothing is installed, published or sent anywhere, and no consumer repository is touched. (`tools/build_logos.py` still needs `fonttools` and `uharfbuzz`; the checks do not.)

| Command | What it does | Exit |
|---|---|---|
| `make check-inventory` | Validates [`inventory/brand-inventory.json`](../inventory/brand-inventory.json): required fields, no duplicate id or path, every catalogued path exists, every git-tracked file is catalogued (a tracked file deleted from the work tree still counts, so deleting it and its entry fails; untracked notes are ignored unless `--include-untracked`), source/canonical-authority references resolve, enums, source-of-truth paths exist and are named in the [index](source-of-truth.md), README links the index. | 0 only if all pass; 1 on any problem or a missing inventory |
| `make check-links` | Offline. Resolves relative links in tracked `.md` and `.html` files (inline and reference-style Markdown links and images, `src`, `href`, CSS `url()`), including `#anchor` targets in Markdown. Fails on undefined or empty reference definitions, and when `README.md`, `docs/source-of-truth.md` or any scannable file is missing (an empty root cannot pass). | 0 only if no local link is broken |
| `make test` | Unit tests including negative cases: missing path, duplicate entry, uncatalogued asset, deleted tracked file, untracked-notes default, broken canonical reference, broken local link, broken or undefined reference-style link, missing anchor, empty root. | 0 only if all pass |
| `make check-links-external` | Optional. Sends a request to each external URL. | 1 if any fails |

## Limits

- Both checkers take `--include-untracked` as an authoring aid to also consider untracked-unignored files; the default and `make check` use tracked files only. Outside a git work tree (tests only) a filesystem walk is used.
- Reference-style links: `[text][label]`, `[label][]` and images are checked for a definition; bare shortcut `[label]` uses are not (indistinguishable from plain brackets), though every definition's target is always checked.
- `check-links` is deterministic and offline. External `http(s)` links are printed as `UNCHECKED` and are **not** verified by it. Anchors are only checked for local Markdown targets, not HTML ids or external pages.
- `check-links-external` proves reachability at run time only, depends on the network, and is not part of `make check`. On 2026-10-12 it reported 35 reachable and 2 failed; the failures are the bare `fonts.googleapis.com` and `fonts.gstatic.com` preconnect hosts, which answer 404 at their root and are not real broken links. It does not show that the target content is right; for example, a link that resolves on a branch may not on `main`. As of 2026-10-12 PR #3's getticketstub.com `docs/studio/` targets exist on getticketstub.com `main` (`388005240aa6`); that is link evidence only, not approval or deployment.
- The inventory checker proves coverage and referential integrity, not that descriptions, owners or statuses are true. `approval_status: unknown` is a statement of absent evidence; the checker does not decide approval.
- Drift between `tokens.json`, `tokens.css` and the Tailwind preset, and between `SPEC.md` and the tokens, is not checked.
- Adding a file to the repository fails `check-inventory` until it gets an entry. That is intended.
