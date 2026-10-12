# Local consumer fixture browser evidence

All examples are synthetic and use platform fallback fonts with off-origin requests blocked. These files provide local engineering evidence only; they are not rights, provider, consumer adoption or release approvals.

- `baseline-4e96666/`: initial preparation correctly refused an untracked dependency symlink. No browser cases ran. The symlink was replaced by an ignored dependency directory containing package links.
- `baseline-4e96666-clean/`: first 16-case run; prior checker measured normal-motion theme colors before the existing 240ms transition settled. Reduced-motion failures were decisive; normal-motion intermediate colors are retained as diagnostic history. `original-driver-before-settled-theme.cjs` preserves that checker.
- `baseline-4e96666-settled/`: baseline rerun with the final checker waiting 350ms for normal-motion colors to settle. Canonical CTA and logo failures reproduce; all inputs and source are pinned.
- `fixed-candidate/`: first correction at `6bf3239e2ca966e22e1d244d3fd4ef0825b76262`; all contrast/logo/canvas/narrow/reduced checks passed, but normal-motion focus measurements caught the remaining transition-all outline fade. This failed result is retained.
- `fixed-focus-candidate/`: repaired background-only transition at `853a474`; all 16 cases passed.
- `final-candidate/`: adds explicit expected button/logo counts at `2122142133bbf393667eafebf32563e1ce46ca48`; read its report for the exact outcome and immutable source, archive, template and screenshot hashes.
- `final-local-consumer.json`: actual pinned Tailwind compilation, local imports and delete/restore CSS recovery at the final source. Any local pass remains explicitly unapproved; owner/font evidence stays blocked.

Command form: `PLAYWRIGHT_BROWSERS_PATH=/tmp/ticketstub-browser-1194 node <checker.cjs> <clean-repository-root> <new-evidence-directory>`. The final checker is committed at `tools/check_consumer_browser.cjs` and included here for baseline reproducibility.
