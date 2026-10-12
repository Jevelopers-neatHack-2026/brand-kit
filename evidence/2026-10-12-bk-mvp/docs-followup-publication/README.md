# E4 publication integrity and environment records

The [177-file source evidence packet](../docs-followup/README.md) passed the independent [publication review](review.json). Its integrity manifest remains byte-for-byte unchanged, SHA-256 `a59028ef528f9a50973438b5df69d1d21006518b38e7b98a3c78a1a0cee46a2d`. The review report SHA-256 is `41d11dd67df617eeccf73d096b085b7484dcd08d89c941796e69c8545e0cdcf2`.

[Attributable summary](attributable-summary.txt) records the reviewer’s exact scope and authorship exclusions. This is evidence publication review only; it supplies no identity, rights, font, consumer, repository-history or release acceptance.

The root [prepublication integrity check](root-prepublication-integrity.json) and [sensitive-pattern scan](root-sensitive-pattern-scan.json) are dated pre-review checks, so their then-pending independent-review field remains preserved. The subsequent independent review is the completed disposition.

The [initial tree-preparation failure](publish-preparation-failure.json) was caused by starting before the pending Git fetch completed. The fetch then completed and local preparation passed; no remote mutation occurred during the failed attempt.

The separate [staging environment recovery](environment-space-recovery.json) is root-authored operational metadata. A full overlay filesystem prevented a new staging-directory creation. All source and test evidence remained intact; publication staging and its isolated Git index/object store moved to available memory-backed temporary storage. This extra operational record is outside the independent reviewer’s claimed 177-file source scope. It is not a source validation failure, test pass or release decision.

The durable artifact is this Git commit. The adjacent source packet and all earlier evidence remain preserved; no ZIP, font, image, credential, customer record, private transcript or raw external workflow log is added here. [Addendum hashes](integrity.json) identify each file. The original 177-file packet is unchanged by these separately scoped receipts.
