# BK-10 candidate artifact binding — engineering evidence

This packet supports a scoped source/tooling fix. **Brand release remains BLOCKED; `release_approved` is false.** It contains sanitized text records, not an approved brand distribution. No identity, rights, font, consumer or release approval is granted by this evidence branch.

## Exact candidate and independent review

- Tested published source: [`19c0bf1f0a89d00cadb1da1bb4028c8fdfccf465`](https://github.com/Jevelopers-neatHack-2026/brand-kit/commit/19c0bf1f0a89d00cadb1da1bb4028c8fdfccf465).
- Parent: `a664cc99884b2679f2c6ea15c6c3e8b98b768755`; tree: `1d9d3f7e030cf65f4737b7fe2446c83ade441579`.
- [Independent technical/docs review](review/published/review.md) and [structured review](review/published/review.json): APPROVE, no blocking implementation findings, by `pr_reconciliation`, which authored none of the six changed files. This is an attributed agent review, not a formal GitHub self-approval or accountable brand sign-off.
- The preserved local commit `6df0b84cd556b9405903a425965bed85eb018014` has the identical source tree and diff. CLI push lacked a configured write credential; authenticated Git Data publication retained the exact tree but produced the distinct published commit above. Exact published-SHA checks are recorded separately.

## Problem and result

A synthetic reproduction demonstrated that a valid 21-file approved subset was compared with a larger 25-file review proposal, creating 22 false stale-receipt blockers. The gate now validates the actual `package-brand` output against a reconstructed approved subset and binds manual/consumer receipts to that subset's exact digest. Missing, modified, symlinked or failed package output remains blocking. An unavailable approved subset produces explicit diagnostic-only review output and a blocked result.

Asset exports now use a fresh path within each run's evidence directory. Source-revision changes cannot accidentally reuse a prior run's output directory. Regression coverage preserves the prior failure and rejects missing/tampered output, failed commands, stale ACKs and unsafe nested error details.

Documentation records the pre-existing marketing reviewer/receiver assignment and exact landing source observations. It does not appoint this Brand agent to a foreign role, approve six-family font drift, waive minimum sizes or resolve the pending identity decision.

## Actual published-candidate run

See [command and runtime](candidate/command.json), [complete 17-target report](candidate/gate/report.json), [command transcript](candidate/gate-command.log), and each adjacent stdout/stderr record.

- Run: 2026-10-12 17:44:59–17:47:47 UTC; source clean before and after.
- Aggregate result: **exit 1, blocked, 14 passing targets, 3 failing release prerequisites, 30 blockers**. No required failure was converted into a pass.
- Passing targets: `check-inventory`, `check-links`, `check-governance`, `build-tokens`, `check-tokens`, `check-tokens-tailwind`, `build-assets`, `check-assets`, `check-accessibility`, `check-accessibility-browser`, `check-guidelines`, `test`, `check-package`, `check-consumers-browser`.
- `make test`: **289 tests passed**, including six new gate regressions.
- `check-provenance`, `package-brand`, `check-consumers`: **exit 2 / fail**, because rights/allowlist/approval/version/consumer prerequisites are absent. These are actual failed release prerequisites, not failed source regression tests and not release passes.
- Local browser evidence: [four accessibility fixture cases](candidate/browser/accessibility-report.json), [synthetic accessibility negative/drift cases](candidate/browser/accessibility-regressions-report.json), and [16 local consumer fixture cases](candidate/browser/consumer-report.json). External fonts and actual deployed consumers were not exercised; true browser UI zoom, assistive technology and accountable visual acceptance remain separate unmet evidence.
- Review ZIP metadata only: 25 files; files digest `738026492ee5ce8b9e8b39e04e20e994fd48d6954acfc39621acaaa2bc4963b5`; archive SHA-256 `2b2e62a6766bb424e3fa361bdc15b4bec30ef8f9930bfe1f41d3bdf56ecd3e7f`; no brand version and no approved subset. The ZIP and unapproved asset binaries are not included here.
- Pinned local tools: Python 3.12.14, fonttools 4.66.1, uharfbuzz 0.56.3, Pillow 12.3.0, Inkscape 1.2.2, Node 24.19.0, npm 11.9.0, Playwright 1.56.1, Chromium 141.0.7390.37 (build 1194), Tailwind 3.4.19. Exact cache hash and failed installation attempt are in [setup](setup).

## Provenance, limits and prior failures

This is local source/build/test evidence. Synthetic approval-shaped receipts are temporary validator inputs, not program approvals. Live/paid providers, commerce, production deployment, demo publication, credential provisioning and consumer writes did not occur. Provider mode and provider cost are N/A because no such provider execution occurred; ordinary tooling installation is recorded separately.

The baseline `make check` failure caused by missing `uharfbuzz` and the failed Chromium network installer are retained under [prior/baseline](prior/baseline) and [setup](setup). Later pinned-runtime runs do not erase them. The original failing approved-subset reproduction and pre-fix tests are under [regressions](regressions), explicitly SYNTHETIC. Earlier local-candidate and reviewer runs remain under [prior](prior) and [review](review), with their original revision attribution.

`manifest.json` records original and published hashes and any withheld sensitive-looking line numbers. `SHA256SUMS` hashes every published text file except itself. The repository's existing secret-pattern filter was applied to publication copies; suspicious complete log lines were withheld, originals remain private locally. No credentials, customer data, transcripts, signed URLs or generated distribution binaries are included. This packet is not the separately required accountable review of all relevant repository history.

## Acceptance and next owners

This completes only the described BK-10/BK-03B/BK-09 implementation corrections. It does not close whole leaves, gate #5, epic #4, ART-05 or EVAL-04. Current prerequisites are recorded by the source gate itself; no foreign/global acceptance is changed.

| Work | Remaining input and responsible role |
| --- | --- |
| [Identity #9](https://github.com/Jevelopers-neatHack-2026/brand-kit/issues/9#issuecomment-6118216028) | Accountable brand approver and design/accessibility/consumer reviewers record the A/B/C scope choice and exact six-decision disposition. |
| [Rights #7](https://github.com/Jevelopers-neatHack-2026/brand-kit/issues/7) | Provenance owner supplies actual acquisition, permitted-use and approval references; 23 core files remain uncleared and the approved allowlist is empty/unreviewed. |
| [Distribution/fonts #14](https://github.com/Jevelopers-neatHack-2026/brand-kit/issues/14) | Brand/technical/provenance owners select an exact version and permitted subset and ratify compliant font delivery. The user's no-self-hosted-runtime-font instruction persists. |
| [Assets #11](https://github.com/Jevelopers-neatHack-2026/brand-kit/issues/11), [accessibility #12](https://github.com/Jevelopers-neatHack-2026/brand-kit/issues/12), [guidelines/claims #13](https://github.com/Jevelopers-neatHack-2026/brand-kit/issues/13) | Required named visual, font-available/unavailable, accessibility and claim review is still absent; passing local fixtures cannot supply these decisions. |
| [Consumers #15](https://github.com/Jevelopers-neatHack-2026/brand-kit/issues/15) | Product, landing and the already assigned marketing supervisor review the exact permitted artifact/hash, font/fallback and upgrade contract and record their own early interface ACKs. No consumer deployment is made a prerequisite of this local review. |
| [Gate #5](https://github.com/Jevelopers-neatHack-2026/brand-kit/issues/5) / [epic #4](https://github.com/Jevelopers-neatHack-2026/brand-kit/issues/4) | Release owner verifies required leaf and named manual evidence before closing the gate and then epic. Master acceptance stays with integration-evals. |

PR #3 remains open on hold under its [current hunk disposition](https://github.com/Jevelopers-neatHack-2026/brand-kit/pull/3#issuecomment-6129482528): neutral work was integrated through #22/#23; unique A-only/foil/sound rules remain unapproved. Its original author branch was preserved. Concurrent PR #25 has its own [active corrective owner](https://github.com/Jevelopers-neatHack-2026/brand-kit/pull/25#issuecomment-6129548550) and unmerged Product #117 prerequisite; this change does not overwrite that lane.

Postmerge verification will be recorded in a later immutable evidence commit. This packet currently describes the published candidate only. The evidence branch is a record location, not the source branch to run the inventory gate against.
