# PR #23 — local engineering evidence

This packet records the exact candidate **d25cf8a023a7b1d110c105a1c2a36cb5577df7f3**, tree **9b4e5bffc559494731cfdcc23c5df7582792736c**, based on main **3c48922b54bf0cc7d92bf9de1f59b1bd3cdad4a4**. It supports the source/tooling PR [#23](https://github.com/Jevelopers-neatHack-2026/brand-kit/pull/23). It is an evidence-only branch snapshot, not an approved brand distribution or a source revision whose inventory check is asserted to pass.

## Result

The candidate's 17-command release check completed every command. **Fourteen commands passed; three release prerequisites failed.** The aggregate result is **blocked**, with 29 recorded blockers and `release_approved: false`. The three failing commands are `check-provenance`, `package-brand`, and normal `check-consumers`. Unknown core rights, the empty reviewed export allowlist, unselected version/source/font decisions, missing reviewer receipts and missing consumer ACKs remain actual blockers. Their nonzero exits have not been relabeled as passes.

All engineering checks needed for this source/tooling change passed on the published candidate. The existing main source already excludes production eligibility; merging the tooling does not distribute the review ZIP, grant rights, select brand direction, publish a demo or close the release gate. PR #22's exact-head scoped review provides the existing comment-review workflow precedent; [its review comment](https://github.com/Jevelopers-neatHack-2026/brand-kit/pull/22#issuecomment-6122144808) likewise kept provenance failure separate from a qualifying source-only change.

## Exact candidate verification

Read [the complete gate report](gate/d25cf8a/report.json), [the invocation log](gate/d25cf8a/invocation.log), and [supplemental checks](candidate/supplemental/report.json). The gate retains each actual command, start time, duration, exit code, stdout/stderr hashes, sanitization metadata and source revision. Original failures and later outcomes are separate files.

| Check | Actual result and scope |
| --- | --- |
| Inventory and local links | 117 tracked source paths catalogued; 353 local links resolved, zero broken. The offline checker explicitly leaves 160 external URLs unchecked. Selected immutable GitHub source targets were checked separately; no global external-link pass is claimed. |
| Governance and provenance structure | Honest pending decisions and UNKNOWN rights are structurally valid. Production provenance remains blocked. |
| Token build and profile | Deterministic build, committed-output parity, 82 tokens and CSS/JSON parity in five contexts. Actual Tailwind 3.4.19 compiled all 40 mapped utilities. Existing token values/names are preserved. |
| Full repository suite | 283 Python tests passed. Negative fixtures are synthetic and do not create approvals. Subset test counts below overlap this suite and are not added to it. |
| Asset builds | Two full builds compared deterministically; 14 canonical SVGs rebuilt byte-identically. The manifest lists 184 payload files plus itself: 185 local review files, including 80 QA cases and four required PNG sizes. All 22 asset tests passed. No generated asset binary is included in this text-only packet. |
| Contrast and guidelines | 62 contrast pairs checked with unrounded thresholds; 12 contrast tests and 24 guideline tests passed. Source claim markers and variant/usage documentation were checked; named semantic/claims approval remains pending. |
| General browser fixture | Four actual Chromium OS/explicit theme cases passed, with keyboard focus, reduced motion and a CSS 200% layout proxy. Five real-browser regression scenarios passed their expected outcomes, including invisible focus, clipped content/rings and source drift. Missing-runtime failure evidence is retained. |
| Review archive | Deterministic bounded 25-file review ZIP verified against its source tree, exact entry hashes and file-set digest. This is an unapproved review candidate; normal production packaging remains blocked. |
| Local consumers | Actual plain-CSS imports and Tailwind compilation passed; removing an import failed and exact re-extraction restored it. This is local recovery mechanics, not an approved historical rollback or consumer deployment. |
| Packaged consumer browser | All 16 cases passed with actual Tailwind and Chromium: two fixtures, four OS/override theme modes, desktop and narrow/reduced-motion combinations. No off-origin requests occurred. |
| Evidence preservation | Fifteen independent filesystem probes passed against byte-identical final checker code. They intentionally failed prerequisites before browser/compiler execution. They are filesystem checks, not 15 additional browser passes. |
| Source integrity | Final supplemental `git diff --check` passed and `git status --porcelain --untracked-files=all` was empty. |

Actual runtime: Python 3.12.14; Node 24.19.0; Playwright 1.56.1; Chromium 141.0.7390.37; Tailwind 3.4.19; fonttools 4.66.1; uharfbuzz 0.56.3; Pillow 12.3.0; Inkscape 1.2.2. The asset toolchain and dependency notice metadata are pinned in source and the attached reports. Provider mode is local/offline with synthetic fixture content. Browser/compiler operations are real local executions. No paid/live provider call, deployment, credential provisioning, demo publication or consumer write occurred.

The review ZIP hash is `df618fc529e02f681707b4aeac9f5d58ee3f8c6d301becb058f3890b8fafc52c`; its file-set digest is `bc7cd5a7c7fffe42e8d48059bdebd31b6dc83a24a3ad6d1bf1fc838bc1095dc6`. These identify local review bytes only. Brand version is null and no release tag exists.

## Independent review

Three scoped independent reviewers report APPROVE at the exact published head:

- [Assets, inventory, metadata, output guard and guide-context review](reviews/d25cf8a/assets-metadata.json), by `/root/pr3_reconcile`.
- [Accessibility, consumer fixture, output guard and guide-context review](reviews/d25cf8a/accessibility.json), by `/root/dependency_audit`.
- [Distribution, guidelines, numerical accessibility and consumer/browser review](reviews/d25cf8a/distribution-docs.json), by `/root/asset_pipeline`.

Each report identifies its own authored exclusions and which exact byte comparisons carry forward prior review. The reviews cover one another's implementation without claiming self-approval. Actual final gate execution is recorded separately from review. The connected GitHub account is also the PR author; attributed agent reviews are posted as PR conversation comments, not fabricated formal GitHub self-approvals. They supply engineering review only, not appointments or identity/rights/font/consumer/release acceptance.

The earlier [d7d4fb3 changes-requested reviews](reviews/d7d4fb3/) remain intact. The original consumer runner falsely passed a fully clipped outline and overwrote a synthetic prior report on an explicit-path collision. Both findings were fixed, independently checked, and rerun. See [focus evidence](negative-evidence/consumer-focus-validation.json), [all 15 output guards](negative-evidence/output-guard-15-probes.json), and [the exact-candidate sentinel recheck](negative-evidence/output-preservation-final.json).

## Earlier failures remain evidence

The [prior runs](prior-runs/) and [negative evidence](negative-evidence/) retain the initial broken links and governance fixture, initial distribution errors, asset matrix/PNG false passes, archive/current-eligibility false passes, browser focus/clipping/source-drift false passes, consumer contrast and animated-focus failures, and output-collision finding. The incomplete integration run containing a governance failure is retained as incomplete/failing, not as a completed pass. The d7 release gate also remains [unchanged](gate/d7d4fb3/report.json).

Older source SHAs can identify local author/reviewer worktrees. Their recorded commands, revisions, hashes and modes remain historical diagnostics; they are not relabeled as fresh published-head results. Final qualification uses the published candidate runs. Original local screenshots/archives are not republished in this packet; their hashes and source inputs remain in reports, and the local procedures can regenerate them. No binary image, font, reference asset, ZIP or private transcript is included here.

## Remaining acceptance and owner actions

[The complete criterion map](criterion-map.json) covers all 74 issue checkboxes: 30 have local implementation/evidence and 44 require owner evidence. These counts do not declare acceptance. Every row records implementation paths, predecessor PRs, the remaining input, responsible role and evidence needed. Relative evidence paths resolve within this packet. A separate postmerge supplement is required before any issue closure.

Only inventory/source-of-truth issue #6 is a closure candidate after the merged-source check and independent review. #7, #9, #11–#15, release gate #5 and epic #4 remain open. Existing closed issues #8 and #10 do not fill missing appointments, rights, font or release receipts.

The next owner decisions are concrete: appoint the accountable technical/provenance/consumer/release reviewers; ratify the A+B versus PR #3 identity proposals using the six-decision packet; record real provenance/rights and a reviewed exact allowlist; choose an approved font-delivery policy under the no-self-hosting constraint; select the exact distribution source/version/contract; and obtain Product, Landing and Marketing early contract ACKs. Actual external-font available/unavailable checks, genuine 200% browser zoom, assistive-technology/manual review, approved rollback evidence and final sanitization/release acceptance remain pending.

PR #3 is only partially superseded. PR #22's immutable studio links and the remaining valid source-path corrections are reused. The paper-only app direction, foil/material and sound proposals remain pending accountable decisions. The original owner's conflicting branch is preserved; this packet does not close it as wholly superseded.

Canonical interfaces remain owned by shared-contracts, application assembly by getticketstub.com and master acceptance by integration-evals. Fourteen Product SVGs at read-only revision `b5573270af362295c126e8b0be61b64f748c09a5` match the brand source exactly; this is byte-parity evidence, not a consumer ACK or deployment claim. No foreign source or acceptance state is changed.

## Integrity and sanitization

[Evidence file metadata](evidence-files.json) records the preserved original location, size and SHA-256 of each copied report. [GitHub state](candidate/github-state.json) records the inspected candidate, branch state and absence of configured check runs/status contexts. The gate's stream reports identify any line sanitization and retain original-stream hashes.

[The exact candidate history scan](provenance/history-scan-candidate.json) inspected 160 reachable text blobs and found no newly unreviewed pattern match; nine binary blobs were excluded from text scanning. Previously flagged identical blobs were reviewed as public badge/font queries or reserved-domain synthetic test inputs. [Reference-image observations](provenance/reference-image-review.json) preserve UNKNOWN origin and rights and do not distribute the images. These bounded checks are not a complete security/legal audit or the missing named release approval.
