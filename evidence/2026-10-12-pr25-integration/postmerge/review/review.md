# Independent review of the actual PR #25 merge and verification

**Verdict: APPROVE the actual merge source parity and scoped verification record.** Reviewer: **/root/pr_1956**. Completed 2026-10-12T20:11:47.479704+00:00. No blocking source or execution-record findings remain.

The separate owner merged PR #25 at **2026-10-12 20:05:08 UTC** as `f34c71a0961dc0c67f1ecb293a5bbb633addb663`. Its actual parents are prior main `e254df5444f0bfedd5526b0e148b0cdf36cbd31f` and reviewed head `aa22b3833a7510e1ece215926faab6c6394e5258`. The actual merge tree is `7fcbfa65fd3423fec10b77d90f7655d2b228e84a`, identical to the independently reviewed head and GitHub's prior candidate tree. All 117 source-tree records match Git; 114 paths remain unchanged from prior main. The isolated merge checkout remains clean.

## Chronology and review meaning

My full candidate source review completed at **2026-10-12 20:02:08 UTC**, before the owner merge, but it was not yet published remotely. This postmerge review does not claim that the owner relied on that review or that a formal GitHub maintainer approval existed. At the postmerge API inspection, no new owner review receipt or comment had been published; formal review and current-merge check/status collections were empty. The PR body still had stale pending Product #117 and review statements. Those should be reconciled with true dates and evidence without rewriting earlier failures.

## Actual merge verification

The supervisor's exact-merge execution ran from **2026-10-12T20:09:09.699052+00:00** through **2026-10-12T20:09:57.413383+00:00**. Execution JSON SHA-256: `ffa4f6729002ca0720717e440c155e37c8a3f85c1e1de4e721b79b8ce09fb5d0`. I inspected the runner and independently matched **all 26 stdout/stderr hashes** across its **13 command groups**. I also executed six read-only Git checks for revision/tree, parent ancestry, candidate equality, diff formatting, clean checkout and complete tree parity.

- **10 command groups exit 0.** Full `make check` passes **289 tests in 38.522 seconds** (whole command 41.731493 seconds), with 117 inventory entries and 387 resolved local links / zero broken. Its local checker explicitly leaves 167 external URLs unchecked.
- `make check-package` verifies a deterministic **25-file unapproved review archive**, SHA-256 `b6dfb695e3ed364517473a69dec53310a841af32771b4cd2360296e21ed04311`, file-set digest `738026492ee5ce8b9e8b39e04e20e994fd48d6954acfc39621acaaa2bc4963b5`, source `f34c71a0961dc0c67f1ecb293a5bbb633addb663`.
- The pinned Tailwind 3.4.19 offline installation and local consumer checks pass, including compiled imports, missing-import rejection and exact-byte restoration. These are local fixture mechanics. They do not establish actual consumer adoption, font-provider behavior, an approved rollback target or owner acceptance.
- **Three actual commands remain failures with exit 2:** `make check-provenance`, `make package-brand` and `make check-consumers`. Their output retains 23 uncleared core files, empty/unreviewed allowlist, missing exact release/distribution/font choices and absent exact consumer decisions. They are recorded as failed, even though the expected blocked behavior was observed.

The runner's documentation-verification result is consistent with those records. **`release_approved=false` and `master_acceptance_changed=false`.** The full 17-target release gate was not rerun on this merge; its prior result remains attached to its original revision. No actual provider, browser-font availability, true UI zoom, assistive-technology or accountable consumer acceptance is inferred.

## Preserved audit failure

My first verification-reader attempt exited 1: it selected the first unittest summary (66 tests) rather than the final 289-test summary. The original script hash and failed diagnostic, including the 66/12/24/289 observed summaries, are embedded in review.json. I corrected only the evidence-reader selector to the final summary and reran its read-only verification. The repository tests and captured execution were not changed or rerun by this reviewer. The failed attempt is not counted as a pass.

## Foreign dependency and acceptance boundary

Product #117's actual merge and CURRENT-STATE.md main target satisfy the recorded Brand source-navigation prerequisite. Product run 38300264410 / job 114981202686 still records an authentication/storage/agent-journey failure and a skipped production-server check; analytics journeys passed in that newer run. The older failed run is retained separately. No Product runtime or master acceptance is granted by this Brand merge or this review.

The three merged documents retain the identity, rights, font, selected-version, release and consumer gaps, plus PR #3's unique unapproved direction/foil/sound proposals. This reviewer performed no source edit, remote mutation or provider call.
