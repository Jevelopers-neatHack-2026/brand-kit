# Brand documentation and final main evidence — 2026-10-12

**Main `e254df5444f0bfedd5526b0e148b0cdf36cbd31f` is verified. The scoped implementation and documentation work is integrated; the brand release remains blocked by actual owner and consumer prerequisites.** This packet preserves source reviews, actual commands, earlier failures and skips, and the exact disposition of the remaining documentation proposals.

## Repository result

| Change | Result and evidence |
| --- | --- |
| PR #23, source and validation implementation | Merged as `6222a745195e9f15a14069e79210ad45daa16c94`; its complete candidate and postmerge evidence remain in the earlier immutable packets below. |
| PR #24, the other maintainer's README update | Merged as `a664cc99884b2679f2c6ea15c6c3e8b98b768755`; reused and independently checked after the owner's merge. No competing branch overwrote it. |
| PR #26, approved-subset/package binding and fresh asset outputs | The owner merged `41001e1875c544d21ad6b481cfe98c9283b0c58c`, tree `1d9d3f7e030cf65f4737b7fe2446c83ade441579`. Our separate [postmerge review](merged-pr26/review.json) and [execution report](merged-pr26/validation.json) are explicitly postmerge. The owner's full gate is separately attributed below. |
| PR #28, existing marketing reviewer role in the source index | Normally merged as current main `e254df5444f0bfedd5526b0e148b0cdf36cbd31f`, tree `32e3904a8d901b9c6cf75ca1e65829fe98df03f0`, at 18:13:07 UTC. The [independent exact-candidate review](index-fix/published-candidate/review/review.json) was posted before merge; [postmerge parity and issue #6 review](index-fix/postmerge-review/review.json) verify the result. |
| PR #25, corrected architecture documentation | Retained OPEN at reviewed `ba65bb20e9f4e820666cbb3a40154c74676d133d`, tree `b296f348e6ff5f4a642c30af735cffbc7d2627b8`. Source review is APPROVE; Product PR #117 remains an explicit merge prerequisite. |
| PR #27, corrective follow-up | Closed unmerged as an exact duplicate on 18:25:04 UTC. Both distinct branch references contained the identical ba65 commit; all work is carried in retained PR #25. Branches and review history are preserved. No separate owner approval or branch-updater identity is inferred. |
| PR #3, original studio/identity proposal | Remains OPEN on HOLD at `289b22659f0699649abd65ba7a3b7e710839f4d3`, conflicting at the final audit. Valid links and neutral corrections are integrated; unique A-only, foil/material and sound decisions remain unanswered. |

The [18:17 GitHub state](current-state.json) is retained as a dated observation before duplicate closure. The later [consolidation record](consolidation-state.json) and [independent duplicate comparison](architecture-ba65bb2/duplicate-review/report.json) record the exact heads, branch references and deliberate closure. Neither record turns incorporation into accountable acceptance.

## Exact candidate and main validation

These are actual local executions, with expected synthetic negative fixtures identified in their command streams. They are not provider or deployed-consumer results.

| Revision and mode | Actual result | Report |
| --- | --- | --- |
| Initial corrected published architecture candidate `aece3f0e0b14e2154a313ae5f37f8cdebc12fa21` | Full `make check`: 283 tests passed in 33.310 seconds; 117 inventory entries; 385 local links, zero broken; 164 external URLs unchecked. Independent source review retains Product HOLD. | [Root commands](prior/aece3f0/root/report.json), [independent review](prior/aece3f0/review/review.json) |
| Integrated architecture candidate `ba65bb20e9f4e820666cbb3a40154c74676d133d` | Full `make check`: 289 tests passed in 53.302 seconds; inventory 117; 387 local links, zero broken; 167 external URLs unchecked. Actual remote-head review passed inventory, links, governance, 24 guideline tests, source/ancestry/parity/diff and clean checks. | [Root commands](architecture-ba65bb2/root/report.json), [independent review](architecture-ba65bb2/review/review.json) |
| PR #26 actual merged main `41001e1875c544d21ad6b481cfe98c9283b0c58c`, our bounded postmerge review | 35 distribution tests passed in 65.042 seconds, including all six new regressions; 24 guideline tests passed; inventory 117; 378 local links, zero broken; 163 external URLs unchecked. Governance, diff, tree parity and clean checks passed. | [Execution](merged-pr26/validation.json), [review](merged-pr26/review.json) |
| PR #28 exact published candidate `1603948d569ae2eb48693d7f4a40cce45b8111b1` | Full `make check`: 289 tests passed in 47.428 seconds. Independent inventory, links, governance and source/ancestry/diff checks passed on that actual remote commit. | [Root commands](index-fix/published-candidate/root/report.json), [review](index-fix/published-candidate/review/review.json) |
| PR #28 actual main `e254df5444f0bfedd5526b0e148b0cdf36cbd31f` | Full `make check`: 289 tests passed in 65.771 seconds; inventory 117; 379 local links, zero broken; 163 external URLs unchecked. `make check-package`, exact candidate-tree equality, diff and clean checks passed. Three actual release commands failed, as detailed below. | [Postmerge commands and streams](index-fix/postmerge/report.json), [independent postmerge review](index-fix/postmerge-review/review.json) |
| Same actual main, local dependency recovery | `npm ci --offline --ignore-scripts --no-audit --no-fund` passed with the unchanged lockfile. Installed Tailwind is exactly 3.4.19. `make check-consumers-local` then passed actual CSS/Tailwind compile/import, missing-import rejection and exact-byte recovery checks. Normal `make check-consumers` remained exit 2 for real approval/artifact/ACK/font prerequisites. Checkout remained clean. | [Install record](index-fix/postmerge-consumer-recovery/install.json), [recovery commands](index-fix/postmerge-consumer-recovery/report.json) |

Full source commands use the recorded pinned Python environment, `/workspace/scratch/5ecc3c6cf97a/asset-toolchain/bin/python`; the browser cache setting where present is `/tmp/ticketstub-browser-1194`. Each report retains its exact command, environment, revision, time, exit code and original stream hash. Local precommit/first/final corrections and the normal main integration are separately retained under `prior/` and `index-fix/precommit/`; they are not relabeled as published-head results.

### Preserved failed and skipped cases

The first M4 `make check-consumers` failed both because real prerequisite records were missing and because the fresh checkout lacked local Tailwind. The required Tailwind case was **skipped, not passed**. The initial report's short interpretation did not enumerate that additional setup cause. Its report and streams remain unchanged; the [recovery record](index-fix/postmerge-consumer-recovery/report.json) explicitly corrects that interpretation and links the original SHA-256 `659a79b435beecb2e466573ee7d6e615bfe8494c1a45d16f34848c5f4d3ecf90`.

After the recorded offline install, local fixture checks pass and the real consumer gate still fails. The earlier skip is not counted as a pass or erased. All prior source-review findings, actual Product target 404s, original setup/test failures and synthetic negative/recovery runs remain dated and accessible through this and the earlier packets.

## Actual release state

On current main, all three real prerequisite commands still return exit 2:

- `make check-provenance`: actual origin/permission/approval and public allowlist decisions remain absent. The source register still reports 23 uncleared core files; the allowlist is empty and unreviewed.
- `make package-brand`: there is no permitted selected approved subset to package. The command remains blocked rather than producing an approved artifact.
- `make check-consumers`: actual selected version/artifact, font-delivery decision and exact owner/consumer acknowledgments remain absent. Following dependency recovery, its local Tailwind case passes; the remaining failure is not a missing-tool excuse.

The successful M4 deterministic review package contains 25 files: 14 logo sources, seven token files and four guide files. No fonts or references are included. Its archive SHA-256 is `87c4f0ad8e428f9adbd3e1607063372369c5d4022ccdadd67eb7d5fdeacac1e1`; the files digest is `738026492ee5ce8b9e8b39e04e20e994fd48d6954acfc39621acaaa2bc4963b5`. Source is M4, `brand_version` remains unselected, and this is a **review candidate only**. The ZIP and asset binaries are excluded from this public evidence packet.

### Full gate evidence belongs to its actual revision

The PR #26 owner published a complete **postmerge** 17-target gate for M3 at immutable commit `cd744af6da5b1f89f410383fac5937e1ea8d6705`: [readable evidence](https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/cd744af6da5b1f89f410383fac5937e1ea8d6705/evidence/2026-10-12-bk10-candidate-binding/postmerge/README.md), [gate report](https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/cd744af6da5b1f89f410383fac5937e1ea8d6705/evidence/2026-10-12-bk10-candidate-binding/postmerge/gate/report.json). It ran at 17:59:21–18:02:31 UTC: **14 targets pass, 289 tests pass, three required targets fail, aggregate exit 1, 30 blockers, `release_approved=false`**. Four local accessibility cases, their synthetic regressions and 16 local consumer browser cases ran. Root fetched the immutable report and its integrity references; [curated source observation](merged-pr26/owner-full-gate-observation.json) records this without claiming those were our executions.

No full 17-target rerun is asserted for M4's single paragraph change. M4's full source tests, package/consumer/real-blocker checks and independent parity review are above. [Exact source proof](source-proof.json) verifies all 116 other paths unchanged from M3, including all implementations, approval records, distributed payloads and the four public guideline sources. All 14 canonical SVG blobs remain identical to the PR #22 baseline. The PR #26 full gate and the earlier M1 full gate remain attributed to their actual revisions.

## Review and merge accountability

PR #28 changed one governance paragraph to acknowledge the already user-assigned marketing-material supervisor as its content/brand/handoff reviewer and receiver. The [role-source review](role-receipts/independent-wording-review.json) and current governance preserve other reviewer gaps, exact-artifact acknowledgments and source-owned authority. This Brand execution agent is not granted the Marketing supervisor's authority.

The PR #28 [independent review receipt](https://github.com/Jevelopers-neatHack-2026/brand-kit/pull/28#issuecomment-6129925234) was posted at 18:11:11 UTC, before the 18:13:07 merge. Exact-head automated security review completed at 18:11:53 UTC without reported findings. Final guard recorded non-draft/clean at head160, current baseM3, no returned check runs/status contexts/Actions/formal or inline reviews, `protected:false` and no repository/parent rulesets. Normal server-enforced merge used the expected head, with no settings change, review dismissal or bypass. [Merge/state record](current-state.json) preserves these facts.

Attributable agent comments are independent technical source reviews, not formal GitHub self-approval or accountable brand/rights/font/consumer acceptance. Our PR #24 and #26 reviews were after their respective owners' merges and are not backdated. The original owner proposal descriptions and all earlier review findings remain preserved in their PR conversations.

## Remaining criteria and accountable inputs

[The final scope/owner audit](dependencies/final-scope-owner-audit.json) refreshed all ten requested issue bodies, their comments, PR #3 and canonical acceptance. It found no new approval, scope waiver or interface acknowledgment. It distinguishes 64 substantive criteria, 74 mapped rows including ten gate dependency pointers, and 11 additional epic pointers.

| Issue | Exact missing input / responsible role |
| --- | --- |
| #6 / BK-01 | **Closed, six of six scoped inventory criteria remain verified.** The postmerge review rehashed all 95 reference targets: 86 unchanged, nine reviewed intervening changes recorded with both hashes. Inventory closure does not approve the brand release. |
| #7 / BK-06 | Source/rights owners must record exact origin, version, rights holder, acquisition evidence, permitted uses/notices and approval or exclusion. Accountable sanitization/history review and public allowlist decisions remain required. |
| #9 / BK-02 | The nominated approver and required roles must record the six real identity decisions: theme/app scope, variant purposes, palette/type/foil, imagery/artwork and icon direction. Nomination and source presence are not ratification. |
| #11 / BK-04 | Approved source/palette/rights and accountable visual review of the exact export hashes, including small favicon/stamp, compact wordmark, currentColor/background and app-icon cases. |
| #12 / BK-08 | Selected permitted external fonts, available/unavailable cases, real browser 200% zoom, narrow-width/assistive-technology/manual review and exact accountable acceptance. Existing local fixture/contrast results remain available. |
| #13 / BK-05 | Approved usage version/channel/size/background rules and source-backed claim decisions; MM-02/GT-10B content review. Four public sources, 14 claim rows and eight example pairs are implemented. |
| #14 / BK-03B | Actual version, immutable locator/subset/source/hash, compatibility/deprecation and approved rollback decisions; permitted external font provider/families/axes/CSP/privacy/fallback under the no-self-hosting boundary. |
| #15 / BK-09 | Product, Landing and the **existing** Marketing reviewer must ACK or reject the exact permitted artifact/version/import/font/rollback handoff after BK-03B. Early interface review does not require waiting for consumer release or all BK-05 work. |
| #5 / BK-10, then #4 | Record all required scoped outcomes and authenticated receipts; close the gate and then epic only after actual acceptance. The existing closed #8/#10 process/token slices do not grant later release approval. |

Canonical interfaces remain owned by shared-contracts; app assembly by getticketstub.com; master acceptance by integration-evals. [Current policy/canonical comparison](dependencies/policy-and-canonical-refresh.json) found relevant policy and acceptance bytes unchanged. Integration-evals main `f187722613c61e14e3f4087a66d07b2b1e6820f7` retains 47 master criteria, 44 planned and three verified; ART-05 and EVAL-04 remain planned.

## Product PR #117 dependency

The retained PR #25 explicitly requires [Product PR #117](https://github.com/Jevelopers-neatHack-2026/getticketstub.com/pull/117) to merge first. Current observed head is `60d3b6aa074caddca4d362ba8b13b56fe4436177`; actual Product main is `01c65ae2290447c523823bf4601d6373ce4c6ca2`, where the new `docs/architecture/CURRENT-STATE.md` target is absent. The candidate blob is `31d199072287b80237a9b7c65deed2c434a188de`; candidate existence does not satisfy a main-branch link.

Its [build-and-smoke job](https://github.com/Jevelopers-neatHack-2026/getticketstub.com/actions/runs/38287279004/job/114938560052) failed at 17:59:47 UTC. The offline analytics journey run reported 285 passing and two failing phone claim-form cases; later authentication/storage/agent and platform-port checks were skipped. The artifact-upload step's successful conclusion did not produce its configured files. [Dated dependency observations](dependencies/dated-refresh.json) and the root workflow-step snapshot in [state](current-state.json) preserve that distinction. No raw external workflow transcript is republished.

The Product/frontend maintainer must resolve its actual failing cases, complete current-head checks/review, merge normally and supply the resulting main SHA/blob. Brand then verifies both actual main links and refreshes its current candidate/base/reviews/checks before merging PR #25. No foreign implementation or merge was performed, and the upstream prerequisite was not waived.

## Evidence integrity, access and history

[integrity.json](integrity.json) records every included source file, byte count and SHA-256 plus exact original-copy hashes. Command streams retain actual failures and skips. Source snapshots and review JSON exclude full public/private conversation bodies; source documents are linked at immutable commits. This is sanitized, text-only engineering evidence. No credentials, customer data, private transcripts, full external workflow logs, font binaries, unapproved ZIPs, screenshots or asset images are published. A bounded evidence-file review does not satisfy the missing accountable review of all relevant repository history.

The [first publication preflight](publication-preflight-failure.json) rejected two full public comment bodies embedded in the role review before any upload. That failure and original report remain preserved. The separately identified publication copy replaces only those bodies with exact source metadata and text hashes, records the original report digest, and leaves every conclusion and validation result intact. The publication guard remains enforced.

Paid/live provider calls, credential provisioning, external font requests, production deployment, demo publication and submission did not occur. Provider mode and cost are N/A for those absent executions; this makes no product operating-cost claim. Synthetic fixtures never authenticate real rights, identity, manual or consumer acceptance.

Earlier immutable evidence remains preserved:

- [E1 — exact PR #23 candidate, reviews and earlier failures](https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/b6a2cd5b786443abaf4f4023833753c777be910d/evidence/2026-10-12-bk-mvp/candidate/README.md).
- [E2 — actual M1 full gate, six-criterion issue #6 closure and dependency mapping](https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/ca716e1fd218bd9ecdc49675f92f94520998b3d0/evidence/2026-10-12-bk-mvp/postmerge/README.md).
- [E3 — actual M2, PR #24 owner integration and postmerge review](https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/a6e94be639cc516d0c94b0473edf61437ec4a07a/evidence/2026-10-12-bk-mvp/final-main/README.md). Its dated directory name does not denote current main.
- [PR #26 owner's candidate evidence, including earlier failed setup and synthetic regressions](https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/9bb2e7c79ee1c1a34bbde813f0b93f3e9ae447f3/evidence/2026-10-12-bk10-candidate-binding/README.md), plus its separately linked M3 postmerge packet above.
