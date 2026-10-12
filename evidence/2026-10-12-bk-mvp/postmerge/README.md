# PR23 postmerge verification — 2026-10-12

PR [#23](https://github.com/Jevelopers-neatHack-2026/brand-kit/pull/23) merged normally at **`6222a745195e9f15a14069e79210ad45daa16c94`**. Its tree `9b4e5bffc559494731cfdcc23c5df7582792736c` is identical to the independently reviewed candidate `d25cf8a023a7b1d110c105a1c2a36cb5577df7f3`. [GitHub state](github-state.json) and [carry-forward review](reviews/carryforward.json) record this identity; the checks below were freshly executed on the merge itself.

## Result

**14 engineering commands pass; three real prerequisite commands fail; the release aggregate remains blocked with all 29 blockers retained.** All 17 commands ran. `make check-brand-release` exits 2 and `release_approved` is false. See [exact report](gate/report.json), [command/environment](gate/invocation.json) and every preserved command stream beside them. No failed or missing case is represented as a pass.

The full Python suite reports **283 tests passed**. Its 22 asset, 12 contrast and 24 guideline tests are overlapping subsets, not additional unique tests. Actual Tailwind 3.4.19 compiles all 40 mapped utilities. Inventory covers 117 tracked paths; 353 supported local links resolve with zero broken, while 160 other external URLs remain explicitly unchecked. Two complete deterministic asset builds preserve the 14 tracked SVG bytes; the [asset manifest](assets/manifest.json) records 184 payload files plus its manifest, 80 QA cases and 16/24/32/1024px PNG outputs.

The [general browser run](accessibility-browser/report.json) checks four theme/override cases; the [five regression outcomes](browser-regressions/report.json) cover the baseline plus invisible-focus, ancestor-clipping, clipped-focus-ring and source-drift rejection. Missing-runtime failure is retained prior evidence in the candidate packet, not an additional fresh merged-source test. The [consumer browser report](consumer-browser/report.json) passes all 16 actual local fixture cases. These use synthetic local fixtures and platform fallback fonts. CSS 200% layout zoom remains a proxy; approved external-font available/unavailable behavior, real browser zoom and required human/assistive-technology acceptance remain pending. No provider request or external publication occurred.

The [supplemental checks](supplemental/report.json) pass provenance-register structure, local consumer mechanics, diff/clean-tree checks, exact candidate equality and the manually dispositioned legacy/proposed-path search. The [history scan](provenance/history-scan.json) scans 160 reachable text blobs, records nine binary blobs as not text-scanned and retains its limitations; this is not named sanitization approval.

## BK-01 scoped completion

The [independent postmerge recommendation](issue6/closure-recommendation.json) verifies all six current #6 criteria: inventory, index, current/proposed path map, honest classifications/visibility, preserved PR2/PR3/PR22 handoffs, and executable command contracts. It opened and hashed 95 canonical/source/reference targets, preserved all 40 original paths, passed 38 focused tests, and ran the actual CLI against valid and malformed synthetic fixtures. Missing-path and duplicate-ID fixtures both correctly return 1; their diagnostics and exact commands are retained.

Issue #6 expressly excludes rights decisions from inventory closure. Root will record the supervised inventory disposition after publishing this packet; no @lmvdz acknowledgment or creative/rights approval is inferred. The review's authorship exclusions are explicit. The gate run predates this closure disposition: its missing BK-01 release-artifact receipt slot remains recorded, because the actual release artifact/version is still unselected.

## Coverage and open decisions

The [criterion map](criterion-map.json) contains **74 leaf/gate rows: 55 leaf criteria plus 19 gate rows**. The [epic map](epic-dependency-pointers.json) separately covers **all 11 epic dependency pointers**. Those pointers are not 11 additional independent acceptance criteria. This clarifies the earlier candidate README/PR shorthand “all 74 issue checkboxes”; the original packet remains unchanged. Previously closed issues #8/#10 do not supply absent role, identity or release receipts.

Issues #7/#9/#11–#15, gate #5 and epic #4 remain open for actual rights/identity, visual/accessibility/content decisions, a selected versioned distribution/font contract, three named early consumer reviews and accountable gate acceptance. The candidate [decision packet](https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/6222a745195e9f15a14069e79210ad45daa16c94/docs/identity-decision-packet.md), [distribution proposal](https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/6222a745195e9f15a14069e79210ad45daa16c94/distribution/proposal.json) and [acceptance ledger](https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/6222a745195e9f15a14069e79210ad45daa16c94/distribution/acceptance.json) remain explicitly unapproved. The production allowlist remains empty.

PR #3 remains open at `289b22659f0699649abd65ba7a3b7e710839f4d3`: its navigation fixes are integrated, while its unique A-only/foil/sound proposals require accountable decisions. It is not fully superseded. PR #24 was discovered during this postmerge refresh and is being reconciled in a separate owner-compatible lane; this packet does not claim that proposal's outcome.

## Review archive identity and history

Actual M review archive SHA-256: **`aa3445b88bee77dbc96f97392cdaae7d8f81699bdafae2c85bca0d8d1e98bc75`**. File-set digest: **`bc7cd5a7c7fffe42e8d48059bdebd31b6dc83a24a3ad6d1bf1fc838bc1095dc6`**. `brand_version` is null. This is an unapproved local review candidate; no ZIP is published. Its full archive hash differs from the d25 archive because the exact source SHA is embedded, although the payload file-set digest and source tree are unchanged.

[Candidate and retained prior evidence](https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/b6a2cd5b786443abaf4f4023833753c777be910d/evidence/2026-10-12-bk-mvp/candidate/README.md) remains immutable at `b6a2cd5b786443abaf4f4023833753c777be910d`. It retains the original failed/false-pass results, subsequent fixes, exact candidate runs and scoped reviews. Do not relabel those earlier runs as postmerge execution. This supplement includes fresh M outcomes.

Only sanitized/curated text evidence is committed. Asset binaries, fonts, ZIPs, screenshots, reference images and full issue/comment transcripts are excluded. Original report hashes remain intact; references to local unuploaded images are not claims that those images are public. [Evidence files](evidence-files.json) and [packet integrity](packet-integrity.json) provide SHA-256 and byte counts. [Dependency snapshot](dependencies/source-refresh.json) retains dated consumer observations; app composition, shared contracts and canonical/global acceptance remain with their actual owners.
