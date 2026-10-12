# Actual PR #25 merge verification

## Revision and ownership

[PR #25](https://github.com/Jevelopers-neatHack-2026/brand-kit/pull/25) merged at **2026-10-12 20:05:08 UTC**, observed through the repository's `CompleteDotTech` account, while this supervisor was preparing the independent source-review publication. This supervisor did not invoke that merge. Its [20:02:08 independent review](../premerge/review/review.md) completed before the merge, but was **not publicly posted before the merge**. No claim is made that this publication informed the merging actor beforehand.

- Actual resulting main: `f34c71a0961dc0c67f1ecb293a5bbb633addb663`.
- Parents, in order: `e254df5444f0bfedd5526b0e148b0cdf36cbd31f`, `aa22b3833a7510e1ece215926faab6c6394e5258`.
- Actual and independently reviewed tree: `7fcbfa65fd3423fec10b77d90f7655d2b228e84a`.
- Three documentation files changed from the prior main; all 114 other tracked files and modes match. The actual checkout was clean before and after verification.

[Merge observations](github-observations.json) and [independent postmerge review](review/review.md) preserve the exact chronology, source comparison and control limitations. Formal GitHub reviews, check runs and status collections were empty at inspection; those are not represented as passes or as formal approval. This publication informs the accountable approver of the attributable source review and postmerge result after the observed merge.

## Executed verification

The [original command record](commands/execution.json), [source tree](commands/source-tree.json), [exact diff](commands/changed-source.diff) and original stdout/stderr files retain commands, working directories, tool versions, timestamps, modes, actual exits and SHA-256 hashes. Execution completed at **20:09:57 UTC**. The runner is preserved unchanged in [the premerge packet](../premerge/run_verification.py).

| Command / assertion | Actual result |
| --- | --- |
| Python, asset-library, Inkscape, Node and npm version probes | Five version command groups; all exited 0. Exact output is retained. |
| `git diff --check e254df5444f0bfedd5526b0e148b0cdf36cbd31f f34c71a0961dc0c67f1ecb293a5bbb633addb663` | Exit 0. |
| `make check` | Exit 0 in 41.731493 seconds. Full discovery: **289 tests passed in 38.522 seconds**, with no suite skips. Includes inventory, links, token builds/drift checks, governance, accessibility, guidelines and negative/recovery regression tests. |
| Inventory / navigation within `make check` | 117 tracked entries; 387 local links resolved, zero broken. **167 external URLs remain UNCHECKED** by this offline checker. |
| `make check-package` | Exit 0; deterministic offline review candidate, 25 files; no release approval. |
| `npm ci --offline --ignore-scripts --no-audit --no-fund` in `tools/tokens-dev` | Exit 0; installed the existing exact lockfile without scripts or network dependency resolution. |
| `make check-consumers-local` | Exit 0; actual Tailwind 3.4.19 compile and four utility assertions, plain CSS links, missing-import rejection and exact-byte restoration passed. Provider/browser/consumer-acceptance outcomes are not inferred. |
| `make check-provenance` | **FAILED, exit 2**: 23 core assets remain uncleared; no reviewed allowlist or dated review evidence. |
| `make package-brand` | **FAILED, exit 2**: selected source provenance/allowlist blocks approved packaging. |
| `make check-consumers` | **FAILED, exit 2**: exact approved source/version, distribution/font decisions, approved artifact, three early consumer ACKs and external-font evidence are missing. Local fixture mechanics still pass. |

The version entries are Python 3.12.14, fonttools 4.66.1, uharfbuzz 0.56.3, Pillow 12.3.0, Inkscape 1.2.2, Node v24.19.0 and npm 11.9.0. The five version-command groups are Python, asset-library group, Inkscape, Node and npm; `diff-check` is a separate command. There are **13 command groups total: 10 exited 0 and three failed with exit 2**. Expected missing-acceptance failures remain `outcome=failed`; the documentation-verification flag never sets `release_approved`.

Expected `FAIL` lines produced inside negative test fixtures are retained with their passing test assertions. They are labeled synthetic fixture evidence. The initial premerge missing-object diagnostic is also retained in its original review record. Earlier failed release and Product workflow results are not overwritten by these successful source checks.

## Review artifact identity

No archive is published by this evidence packet. The local deterministic check reconstructed an explicitly **unapproved** review archive:

- Source: `f34c71a0961dc0c67f1ecb293a5bbb633addb663`.
- Archive SHA-256: `b6dfb695e3ed364517473a69dec53310a841af32771b4cd2360296e21ed04311`.
- Exported file-set digest: `738026492ee5ce8b9e8b39e04e20e994fd48d6954acfc39621acaaa2bc4963b5`.
- File count: 25. This file-set digest is unchanged from the previously verified e254 source; the archive digest changes because its manifest records the actual new source revision.
- `release_approved=false`; `consumer_adoption=false`; `font_provider_checks.performed_this_run=false`.

These are reproducibility and local-import evidence, not an approved release locator, selected brand version, rights decision or consumer pin acceptance. The separate full 17-target release gate remains pinned to [41001e1 evidence](https://github.com/Jevelopers-neatHack-2026/brand-kit/blob/cd744af6da5b1f89f410383fac5937e1ea8d6705/evidence/2026-10-12-bk10-candidate-binding/postmerge/README.md): 14 passes, three failures, 30 blockers. That complete gate was not rerun or relabeled at f34.

## Product and acceptance boundary

Product #117's actual merge and both default/exact CURRENT-STATE targets were verified in the [premerge source observations](../premerge/github-observations.json). This resolves the Brand documentation's navigation prerequisite.

[Product workflow run 38300264410, job 114981202686](https://github.com/Jevelopers-neatHack-2026/getticketstub.com/actions/runs/38300264410/job/114981202686) remains failed: analytics journeys succeeded, the authentication/storage/agent journey step failed, and the dependent production-server step was skipped. No root cause or Product runtime approval is inferred. The Product/frontend runtime owner retains that separate failure.

Approved font availability/unavailability, true browser UI zoom, assistive technology, accountable visual/content review, rights and historical-source review, distribution/version decisions and actual consumer/release receipts remain missing. No provider request, deployment, demo publication, credential provisioning, issue closure or master-acceptance change occurred in this verification.

## Integrity

`manifest.json` records exact original/published hashes for all copied files. `SHA256SUMS` covers every other postmerge packet file. The overall packet also preserves the independently audited premerge packet unchanged and supplies complete overall checksums. No fonts, images, archives, credentials, customer data, private transcripts or foreign workflow logs are included. Execution used an isolated memory-backed checkout because the shared overlay filesystem was full, without deleting other writers' files.
