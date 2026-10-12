#!/usr/bin/env python3
"""Check the shape of the brand governance documents (stdlib only).

Verifies required sections and fields, relative links and anchors, that the
simulation is labelled fictional and never release eligible, and that no
unlabelled approval claim appears. It cannot verify that anyone approved
anything. Exit 0 when all checks pass, 1 otherwise. Reads files only.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOV = ROOT / "docs" / "brand-governance.md"
TPL = ROOT / "docs" / "governance" / "decision-template.md"
SIM = ROOT / "docs" / "governance" / "simulated-walkthrough.md"

GOV_HEADINGS = ["Responsibility table (BK-07.1)", "Decision lifecycle (BK-07.2)",
                "Change classes (BK-07.3)",
                "Deprecation, replacement, rollback and revocation (BK-07.4)",
                "Release eligibility check", "Closure blockers"]
TPL_FIELDS = ["Decision ID", "Status", "Change class", "Base revision",
              "Proposed revision", "Files and hashes", "Rationale",
              "Scope of approval", "Rights and provenance", "Affected consumers",
              "Reviewers", "Decision date", "Release eligible"]
MARKER = "FICTIONAL SIMULATION"


def slug(h):
    s = re.sub(r"[^\w\- ]", "", h.lower()).strip().replace(" ", "-")
    return s


def check_links(path, errors):
    text = path.read_text()
    for m in re.finditer(r"\[[^\]]*\]\(([^)\s]+)\)", text):
        t = m.group(1)
        if re.match(r"[a-z]+://", t):
            continue
        f, _, frag = t.partition("#")
        target = (path.parent / f).resolve() if f else path
        if not target.exists():
            errors.append(f"{path.name}: broken link {t}")
        elif frag and target.suffix == ".md":
            slugs = {slug(h) for h in re.findall(r"^#+\s+(.*)$", target.read_text(), re.M)}
            if frag not in slugs:
                errors.append(f"{path.name}: missing anchor {t}")


def main():
    errors = []
    for p in (GOV, TPL, SIM):
        if not p.exists():
            errors.append(f"missing required file {p.relative_to(ROOT)}")
    if errors:
        print("\n".join(errors)); return 1
    gov, tpl, sim = GOV.read_text(), TPL.read_text(), SIM.read_text()
    for h in GOV_HEADINGS:
        if not re.search(rf"^## {re.escape(h)}\s*$", gov, re.M):
            errors.append(f"governance doc missing heading: {h}")
    for f in TPL_FIELDS:
        if f not in tpl:
            errors.append(f"template missing field: {f}")
    for ref in ("Unknown", "@CompleteDotTech", "LaJefa", "Lars", "issuecomment-6113526793",
                "issuecomment-6116787775", "No self-hosted fonts", "Refs #8"):
        if ref not in gov and ref != "Refs #8":
            errors.append(f"governance doc missing required statement: {ref}")
    if MARKER not in sim:
        errors.append("simulation missing FICTIONAL SIMULATION marker")
    if re.search(r"Release eligible\W*\**\s*\|?\s*\**yes", sim, re.I):
        errors.append("simulation claims release eligible: yes")
    if "Release eligible" not in sim:
        errors.append("simulation missing Release eligible: no statement")
    if re.search(r"^- \*\*Status:\*\* approved\s*$", sim, re.M):
        errors.append("simulation has approved status without (fictional)")
    for p in (GOV, TPL, SIM):
        check_links(p, errors)
    for e in errors:
        print("FAIL:", e)
    if not errors:
        print("governance docs OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
