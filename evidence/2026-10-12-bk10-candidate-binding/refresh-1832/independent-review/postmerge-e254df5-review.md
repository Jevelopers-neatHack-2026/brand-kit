# Independent postmerge evidence review

**Decision: APPROVE evidence integrity and the stated local verification scope.** No blocking finding was identified. This is not a new brand, rights, font, asset, public-claim, consumer, release or global acceptance approval.

Reviewer: `/root/implementation_refresh`. The reviewer authored neither PR #28's source paragraph nor the supplied postmerge runner/logs. This review used read-only GitHub/source inspection, evidence reading, and digest/parity checks. It did not rerun the broad test suite or modify source/remote resources.

## Exact source and integrity

- Merged main: `e254df5444f0bfedd5526b0e148b0cdf36cbd31f`; tree `32e3904a8d901b9c6cf75ca1e65829fe98df03f0`.
- Candidate `1603948d569ae2eb48693d7f4a40cce45b8111b1` has exactly the same tree. GitHub independently confirms the merge parents `41001e1875c544d21ad6b481cfe98c9283b0c58c` and `1603948d569ae2eb48693d7f4a40cce45b8111b1`.
- There are 117 tracked files. Only `docs/source-of-truth.md` differs from prior verified main; 116 tracked files are unchanged. The change is one governance paragraph, one addition/deletion.
- `source-tree.json` matches the actual Git tree, and `changed-source.diff` matches the Git diff byte-for-byte. The current checkout is clean. The reviewed runner records clean source before and after its execution; the reviewer independently confirmed the current clean state.
- `execution.json` SHA-256: `d49082b46f596870fadc8a732318bd4a5679e5b1aaac798c1e134dc25c786cc3`.
- All 12 recorded stdout/stderr SHA-256 values match actual files. Digests for all 15 selected evidence files are in the JSON review. The runner's SHA-256 is `e33a41442d4533678245a1a2e09df72a063329577e746d69cd0d437b8c35a419`.

## Actual recorded outcomes

All six recorded commands exited 0. `make check` completed with **289 named tests passed in 40.998s**; inventory 117, local links 379 resolved/zero broken, and 163 external URLs explicitly unchecked. Token validation covered 82 tokens; contrast validation recorded 36 palette pairs and 26 semantic pairs.

`make check-package` completed with a deterministic 25-file **offline review candidate**, full source pin `e254df5444f0bfedd5526b0e148b0cdf36cbd31f`, archive SHA-256 `87c4f0ad8e428f9adbd3e1607063372369c5d4022ccdadd67eb7d5fdeacac1e1`, and file-set digest `738026492ee5ce8b9e8b39e04e20e994fd48d6954acfc39621acaaa2bc4963b5`. It explicitly reports `release_approved=false`.

The inventory/link failure lines emitted within the unit-test transcript belong to deliberately invalid synthetic fixtures. The complete named suite reports `OK`, with no failed or skipped test result. These fixtures do not supply actual approval records.

## Scope, prior failures and publication review

The actual historical 17-target gate at `41001e1875c544d21ad6b481cfe98c9283b0c58c` remains **blocked: 14 passed, three failed, 30 blockers**. `check-provenance`, `package-brand`, and `check-consumers` each exited 2. These results were checked against the preserved prior report and are not relabelled or attributed to a new gate run.

Full release-gate/browser/provider/manual checks were not rerun for this unchanged implementation. Missing actual font availability, true 200% browser zoom, assistive-technology, visual/claims review, identity, rights, release and consumer acceptance remains unmet. No external/global acceptance changes.

All 15 selected text files were inspected. The repository secret-pattern scan matched 11 public font/badge URLs because they contain query parameters; individual review found only known font-family/display and badge-style/color parameters. No credentials, signed URLs, customer data or private transcripts were observed. This bounded review does not authenticate external reviewer decisions. Original logs and hashes remain unchanged.
