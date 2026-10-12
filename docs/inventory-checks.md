# Inventory checks

Standard library only; Python 3.9 or newer. Nothing is installed, published or sent anywhere, and no consumer repository is touched. (`tools/build_logos.py` still needs `fonttools` and `uharfbuzz`; the checks do not.)

| Command | What it does | Exit |
|---|---|---|
| `make check-inventory` | Validates [`inventory/brand-inventory.json`](../inventory/brand-inventory.json): required fields, no duplicate id or path, every catalogued path exists, every tracked or untracked-unignored file is catalogued, source/canonical-authority references resolve, enums, source-of-truth paths exist and are named in the [index](source-of-truth.md), README links the index. | 0 only if all pass; 1 on any problem or a missing inventory |
| `make check-links` | Offline. Resolves relative links in tracked `.md` and `.html` files (Markdown links, `src`, `href`, CSS `url()`), including `#anchor` targets in Markdown. | 0 only if no local link is broken |
| `make test` | Unit tests including negative cases: missing path, duplicate entry, uncatalogued asset, broken canonical reference, broken local link, missing anchor. | 0 only if all pass |
| `make check-links-external` | Optional. Sends a request to each external URL. | 1 if any fails |

## Limits

- `check-links` is deterministic and offline. External `http(s)` links are printed as `UNCHECKED` and are **not** verified by it. Anchors are only checked for local Markdown targets, not HTML ids or external pages.
- `check-links-external` proves reachability at run time only, depends on the network, and is not part of `make check`. On 2026-10-12 it reported 35 reachable and 2 failed; the failures are the bare `fonts.googleapis.com` and `fonts.gstatic.com` preconnect hosts, which answer 404 at their root and are not real broken links. It does not show that the target content is right; for example, PR #3's getticketstub.com targets may resolve on a branch but not on `main`.
- The inventory checker proves coverage and referential integrity, not that descriptions, owners or statuses are true. `approval_status: unknown` is a statement of absent evidence; the checker does not decide approval.
- Drift between `tokens.json`, `tokens.css` and the Tailwind preset, and between `SPEC.md` and the tokens, is not checked.
- Adding a file to the repository fails `check-inventory` until it gets an entry. That is intended.
