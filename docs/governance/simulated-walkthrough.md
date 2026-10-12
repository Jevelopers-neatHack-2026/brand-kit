# Simulated change walkthrough (BK-07.5)

> **FICTIONAL SIMULATION. Not a historical approval. Not release eligible.**
> Every name, date, hash and verdict below is invented to exercise the process. Nobody reviewed or approved anything here. Do not cite this file as evidence of approval, and do not copy its records into a real decision register. Hashes are placeholders, not hashes of real files. Real reviewer roles are still unfilled (see [responsibility table](../brand-governance.md#responsibility-table-bk-071)).

## Scenario A: unapproved core change is rejected from release

**Proposal (fictional):** replace Ticket Orange `#E4572E` in `tokens/tokens.json` with a different orange. This is a **core identity** change.

| Field | Fictional value |
|---|---|
| Decision ID | SIM-A-core-orange |
| Status | proposal (never reached review) |
| Change class | core identity |
| Base / proposed revision | `0000000000000000000000000000000000000000` / `1111111111111111111111111111111111111111` |
| File and SHA-256 | `tokens/tokens.json`, `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` |
| Reviewers | accountable approver: pending; provenance: pending; technical: unknown; consumers: unknown |
| Release eligible | **no** |

**Walk:**

1. Class is core identity, so approver, provenance reviewer and all affected consumer reviewers are required.
2. The eligibility check asks: is the changed `tokens/tokens.json` hash in an `approved` decision? No: the record is `proposal`, every reviewer row is `pending`, and technical and consumer reviewers are not even appointed.
3. **Result: the change is rejected from the release candidate.** The release keeps the last approved value. Because no real approved version exists today, the release is simply not eligible.
4. Recorded disposition (fictional): `Status: rejected (release gate)`; rationale "missing required approvals"; the proposer may resubmit with evidence.

## Scenario B: approved compatible change, traceable path

**Proposal (fictional):** add a new token `--ts-example-accent` without changing any existing token. **Compatible token addition.**

| Step | Fictional record |
|---|---|
| 1. Proposal | SIM-B-token-add, by `sim-author`, 2099-01-01. Base `2222222222222222222222222222222222222222`, proposed `3333333333333333333333333333333333333333` |
| 2. Files | `tokens/tokens.json`, `tokens/tokens.css`, `tokens/tailwind.preset.js`, each with its own placeholder SHA-256 |
| 3. Review | Technical reviewer `sim-tech` checks the addition is additive. Approver `sim-approver` confirms scope: covers the new token only. Evidence links are fictional |
| 4. Consumers | Consumers notified; none require review for a compatible addition. `sim-consumer` opts out |
| 5. Decision | `approved` on 2099-01-02 (fictional), scope: new token only, hashes as listed |
| 6. Trace | A reader follows decision ID → hashes → diff → reviewers → notification, and a later hash mismatch would revoke it |

Result: in a *real* process this path would make the listed hashes release-eligible. **Here it does not, because every name, date and hash is fictional**, so `Release eligible: no`.

## Scenario C: withdrawal and rollback (fictional)

SIM-B is later revoked because a fictional consumer reports a clash (2099-02-01).

- Affected version: the fictional release containing SIM-B.
- Previously approved version: the fictional release before SIM-B, with its hashes.
- Owner action: the approver records a revocation entry and notifies `sim-consumer`.
- Consumer action: remove or ignore the new token. The producer edits no consumer repository.
- Release readiness for any release containing SIM-B is invalidated.

## Fictional record excerpt

```markdown
FICTIONAL SIMULATION - not a historical approval - not release eligible
- **Decision ID:** SIM-B-token-add
- **Status:** approved (fictional)
- **Release eligible:** no
```
