#!/usr/bin/env python3
"""Validate the BK-06 provenance register and the production export allowlist.

Offline and deterministic: reads files only; nothing is installed, published or sent.
Standard library only (Python 3.9+).

    python3 tools/check_provenance.py --register-only   structural validation; honest UNKNOWNs pass
    python3 tools/check_provenance.py                    production eligibility; fails closed
    python3 tools/check_provenance.py --report           per-file include/exclude decision report
    python3 tools/check_provenance.py --print-hashes     current sha256 of every in-scope file

Exit 0 only when every check of the chosen mode passes, 1 otherwise. The production mode
passes only with a reviewed, non-empty allowlist of exact path+hash entries whose register
records carry real approval, and with the rights of every core asset cleared.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inventory_lib import ROOT, list_files  # noqa: E402

REGISTER = "provenance/register.json"
ALLOWLIST = "provenance/allowlist.json"
UNKNOWN = "UNKNOWN"

CLASSES = {"first-party-canonical", "first-party-generated", "first-party-derived", "first-party-readme",
           "licensed-dependency", "licence-notice", "reference-unknown", "third-party-candidate", "internal"}
ELIGIBLE_CLASSES = {"first-party-canonical", "first-party-generated", "first-party-derived", "first-party-readme"}
EXCLUDED_CLASSES = {"licensed-dependency", "licence-notice", "reference-unknown", "third-party-candidate", "internal"}
APPROVAL_STATUS = {UNKNOWN, "approved", "rejected"}
RELEASE = {"candidate", "excluded"}
FONT_EXT = (".ttf", ".otf", ".woff", ".woff2", ".eot")
REQUIRED = ["path", "sha256", "size_bytes", "introduced_in", "classification", "core", "origin", "origin_evidence",
            "creator_rights_holder", "source_version", "derivation", "tooling", "notice_required", "notice_files",
            "rights_status", "intended_uses", "permitted_uses", "restrictions", "reviewer", "approval",
            "disposition", "notes"]
ALLOW_EMPTY = {"notice_files", "notes"}
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
RESTRICTED_RE = re.compile(r"^restricted:[A-Za-z0-9._-]{1,64}$")
URL_RE = re.compile(r"^https://[A-Za-z0-9.-]+(/[^\s?#]*)?(#[A-Za-z0-9._-]+)?$")
SECRET_PATTERNS = [
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("API key/secret assignment", re.compile(r"(?i)\b(api[_-]?key|secret|passw(or)?d|token|bearer)\b\s*[:=]\s*\S{8,}")),
    ("URL with credentials or query", re.compile(r"https?://[^\s/]*@|https?://[^\s]*\?[^\s]*=")),
    ("email address", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def path_problem(root: Path, rel) -> str | None:
    """Why `rel` is not a safe repository-relative file path, or None."""
    if not isinstance(rel, str) or not rel:
        return "path is empty or not a string"
    if any(ord(c) < 32 for c in rel) or "\\" in rel:
        return "path has control or backslash characters"
    if rel.startswith("/") or re.match(r"^[A-Za-z]:", rel) or rel.startswith("~"):
        return "path is absolute"
    parts = rel.split("/")
    if any(p in ("", ".", "..") for p in parts):
        return "path has empty, '.' or '..' segments (traversal)"
    cur = root
    for p in parts:
        cur = cur / p
        if cur.is_symlink():
            return "path goes through a symlink"
    try:
        if not (root.resolve() / rel).resolve().is_relative_to(root.resolve()):
            return "path escapes the repository"
    except (OSError, ValueError):
        return "path cannot be resolved"
    return None


def load_json(root: Path, rel: str):
    p = root / rel
    if not p.is_file():
        return None, [f"missing required input: {rel}"]
    try:
        return json.loads(p.read_text(encoding="utf-8")), []
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return None, [f"{rel}: invalid JSON: {exc}"]


def strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from strings(k)
            yield from strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from strings(v)


def sanitize_problems(doc, rel: str) -> list[str]:
    errs = []
    for s in strings(doc):
        for name, pat in SECRET_PATTERNS:
            if pat.search(s):
                errs.append(f"{rel}: string looks like a {name}; use a sanitized reference (not printed)")
    return errs


def evidence_problem(root: Path, ref, tracked: set[str]) -> str | None:
    """Evidence must be UNKNOWN, a tracked repo path, a public https URL or an opaque restricted:<id>."""
    if ref == UNKNOWN or (isinstance(ref, str) and RESTRICTED_RE.match(ref)):
        return None
    if not isinstance(ref, str) or not ref:
        return "evidence reference is empty or not a string"
    if ref.startswith("https://"):
        return None if URL_RE.match(ref) else "evidence URL must be plain https without credentials or query"
    base = ref.split("#", 1)[0]
    if path_problem(root, base):
        return f"evidence path '{ref}' is unsafe: {path_problem(root, base)}"
    if base not in tracked:
        return f"evidence path '{ref}' is not a tracked file"
    return None


def evidence_list(value) -> list:
    return value if isinstance(value, list) else [value]


def scope_files(root: Path, prefixes, tracked: set[str]) -> set[str]:
    return {f for f in tracked if f.startswith(tuple(prefixes))}


def validate_register(root: Path, reg, tracked: set[str]) -> list[str]:
    errs: list[str] = []
    if not isinstance(reg, dict):
        return [f"{REGISTER}: top level must be an object"]
    if reg.get("schema_version") != 1:
        errs.append(f"{REGISTER}: schema_version must be 1")
    if reg.get("hash_algorithm") != "sha256":
        errs.append(f"{REGISTER}: hash_algorithm must be 'sha256'")
    if not isinstance(reg.get("synthetic"), bool):
        errs.append(f"{REGISTER}: 'synthetic' must be true or false")
    if not reg.get("source_revision"):
        errs.append(f"{REGISTER}: missing source_revision")
    prefixes = reg.get("scope_prefixes")
    if not isinstance(prefixes, list) or not prefixes or not all(isinstance(p, str) and p.endswith("/") for p in prefixes):
        return errs + [f"{REGISTER}: scope_prefixes must be a non-empty list of 'dir/' prefixes"]
    records = reg.get("records")
    if not isinstance(records, list) or not records:
        return errs + [f"{REGISTER}: 'records' must be a non-empty list"]
    errs += sanitize_problems(reg, REGISTER)

    seen: set[str] = set()
    for i, r in enumerate(records):
        where = f"records[{i}] ({r.get('path', '?') if isinstance(r, dict) else '?'})"
        if not isinstance(r, dict):
            errs.append(f"{where}: must be an object")
            continue
        for key in REQUIRED:
            if key not in r:
                errs.append(f"{where}: missing field '{key}'")
            elif r[key] in (None, "", {}) or (r[key] == [] and key not in ALLOW_EMPTY):
                errs.append(f"{where}: field '{key}' is empty; write UNKNOWN when the value is not known")
        rel = r.get("path")
        bad = path_problem(root, rel)
        if bad:
            errs.append(f"{where}: {bad}")
            continue
        if rel in seen:
            errs.append(f"{where}: duplicate path")
        seen.add(rel)
        if not any(rel.startswith(p) for p in prefixes):
            errs.append(f"{where}: path is outside scope_prefixes")
        cls = r.get("classification")
        if cls not in CLASSES:
            errs.append(f"{where}: classification '{cls}' not in {sorted(CLASSES)}")
        if not isinstance(r.get("core"), bool):
            errs.append(f"{where}: 'core' must be true or false")
        actual = root / rel
        if not actual.is_file():
            errs.append(f"{where}: file does not exist")
        else:
            digest = r.get("sha256")
            if not isinstance(digest, str) or not SHA_RE.match(digest):
                errs.append(f"{where}: sha256 must be 64 lowercase hex characters")
            elif digest != sha256_file(actual):
                errs.append(f"{where}: sha256 does not match the file bytes (stale register); actual {sha256_file(actual)}")
            if r.get("size_bytes") != actual.stat().st_size:
                errs.append(f"{where}: size_bytes does not match the file")
        if r.get("rights_status") not in (UNKNOWN, "cleared"):
            errs.append(f"{where}: rights_status must be UNKNOWN or cleared")
        if r.get("notice_required") not in (UNKNOWN, "yes", "no"):
            errs.append(f"{where}: notice_required must be UNKNOWN, yes or no")
        nf = r.get("notice_files")
        if not isinstance(nf, list):
            errs.append(f"{where}: notice_files must be a list")
        elif r.get("notice_required") == "yes" and not nf:
            errs.append(f"{where}: notice_required is yes but notice_files is empty")
        approval = r.get("approval")
        if isinstance(approval, dict):
            for key in ("status", "evidence", "date"):
                if approval.get(key) in (None, ""):
                    errs.append(f"{where}: approval.{key} is empty; write UNKNOWN")
            if approval.get("status") not in APPROVAL_STATUS:
                errs.append(f"{where}: approval.status must be one of {sorted(APPROVAL_STATUS)}")
            if approval.get("status") == "approved":
                for key in ("evidence", "date"):
                    if approval.get(key) in (UNKNOWN, None, ""):
                        errs.append(f"{where}: approved but approval.{key} is UNKNOWN")
                if r.get("reviewer") in (UNKNOWN, None, ""):
                    errs.append(f"{where}: approved but reviewer is UNKNOWN")
            for ev in evidence_list(approval.get("evidence", UNKNOWN)):
                p = evidence_problem(root, ev, tracked)
                if p:
                    errs.append(f"{where}: approval.evidence: {p}")
        elif "approval" in r:
            errs.append(f"{where}: approval must be an object")
        for ev in evidence_list(r.get("origin_evidence", UNKNOWN)):
            p = evidence_problem(root, ev, tracked)
            if p:
                errs.append(f"{where}: origin_evidence: {p}")
        disp = r.get("disposition")
        release = disp.get("release") if isinstance(disp, dict) else None
        if not isinstance(disp, dict) or release not in RELEASE or not disp.get("rationale"):
            errs.append(f"{where}: disposition needs release in {sorted(RELEASE)} and a rationale")
        # Classification rules: reference/internal/third-party/licensed never become release candidates.
        if cls in EXCLUDED_CLASSES and release != "excluded":
            errs.append(f"{where}: classification '{cls}' must have disposition.release 'excluded'")
        if rel.endswith(FONT_EXT) and (release != "excluded" or cls != "licensed-dependency"):
            errs.append(f"{where}: runtime font files are source-only: classification licensed-dependency, release excluded")
        if rel.startswith("references/") and cls in ELIGIBLE_CLASSES:
            errs.append(f"{where}: files in references/ cannot be classified first-party from their location or appearance")
        if cls == "reference-unknown" and r.get("rights_status") != UNKNOWN:
            errs.append(f"{where}: reference-unknown must keep rights_status UNKNOWN")
        if cls in ELIGIBLE_CLASSES and r.get("origin") in (None, ""):
            errs.append(f"{where}: first-party classification needs a recorded origin (or UNKNOWN)")

    for r in records:
        if not isinstance(r, dict) or not isinstance(r.get("notice_files"), list):
            continue
        for n in r["notice_files"]:
            if n not in seen:
                errs.append(f"{r.get('path')}: notice file '{n}' is not a register record")
    covered = set()
    for r in records:
        if isinstance(r, dict) and isinstance(r.get("notice_files"), list):
            covered.update(r["notice_files"])
    for r in records:
        if isinstance(r, dict) and r.get("classification") == "licence-notice" and r.get("path") not in covered:
            errs.append(f"{r.get('path')}: licence notice is not named by any record's notice_files")

    in_scope = scope_files(root, prefixes, tracked)
    for f in sorted(in_scope - seen):
        errs.append(f"unregistered file: {f}")
    for f in sorted(seen - in_scope):
        errs.append(f"registered path is not a tracked in-scope file: {f}")
    return errs


def validate_allowlist_shape(root: Path, al, register_paths: set[str]) -> list[str]:
    if not isinstance(al, dict):
        return [f"{ALLOWLIST}: top level must be an object"]
    errs = []
    if al.get("schema_version") != 1:
        errs.append(f"{ALLOWLIST}: schema_version must be 1")
    if not isinstance(al.get("synthetic"), bool):
        errs.append(f"{ALLOWLIST}: 'synthetic' must be true or false")
    review = al.get("review")
    if not isinstance(review, dict) or not all(review.get(k) not in (None, "") for k in ("reviewer", "evidence", "date")):
        errs.append(f"{ALLOWLIST}: review needs reviewer, evidence and date (UNKNOWN is allowed in shape checks)")
    entries = al.get("entries")
    if not isinstance(entries, list):
        return errs + [f"{ALLOWLIST}: 'entries' must be a list"]
    errs += sanitize_problems(al, ALLOWLIST)
    seen = set()
    for i, e in enumerate(entries):
        where = f"allowlist entries[{i}] ({e.get('path', '?') if isinstance(e, dict) else '?'})"
        if not isinstance(e, dict):
            errs.append(f"{where}: must be an object")
            continue
        bad = path_problem(root, e.get("path"))
        if bad:
            errs.append(f"{where}: {bad}")
            continue
        if e["path"] in seen:
            errs.append(f"{where}: duplicate path")
        seen.add(e["path"])
        if e["path"] not in register_paths:
            errs.append(f"{where}: path is not in the register")
        if not isinstance(e.get("sha256"), str) or not SHA_RE.match(e["sha256"]):
            errs.append(f"{where}: sha256 must be 64 lowercase hex characters")
        if not e.get("use"):
            errs.append(f"{where}: needs a 'use' naming the permitted use")
    return errs


def production_problems(root: Path, reg, al, allow_synthetic: bool = False) -> list[str]:
    """Fail-closed eligibility. Assumes the register and allowlist shapes already validated."""
    errs: list[str] = []
    if (reg.get("synthetic") or al.get("synthetic")) and not allow_synthetic:
        errs.append("synthetic fixture data can never be release evidence")
    by_path = {r["path"]: r for r in reg["records"]}
    core_blocking = [r["path"] for r in reg["records"]
                     if r.get("core") and (r.get("rights_status") != "cleared" or r.get("approval", {}).get("status") != "approved")]
    if core_blocking:
        errs.append(f"core asset rights/approval not cleared for {len(core_blocking)} core file(s), e.g. {core_blocking[0]}; "
                    "an otherwise complete register does not lift this")
    entries = al.get("entries") or []
    if not entries:
        errs.append("allowlist is empty: no reviewed export candidate exists")
    review = al.get("review") or {}
    for key in ("reviewer", "evidence", "date"):
        if review.get(key) in (UNKNOWN, None, ""):
            errs.append(f"allowlist review.{key} is UNKNOWN: the exact candidate list has not been reviewed")
    if al.get("status") != "reviewed":
        errs.append("allowlist status is not 'reviewed'")
    listed = {e["path"]: e for e in entries}
    for path, e in listed.items():
        where = f"allowlist {path}"
        r = by_path.get(path)
        if r is None:
            continue
        actual = root / path
        if not actual.is_file():
            errs.append(f"{where}: file missing")
            continue
        digest = sha256_file(actual)
        if e["sha256"] != digest:
            errs.append(f"{where}: allowlist hash does not match the file bytes (stale)")
        if r["sha256"] != digest or e["sha256"] != r["sha256"]:
            errs.append(f"{where}: register hash does not match the file bytes (stale)")
        cls = r["classification"]
        if cls not in ELIGIBLE_CLASSES:
            errs.append(f"{where}: classification '{cls}' is excluded from release (reference, internal, third-party, licensed or notice)")
        if path.endswith(FONT_EXT):
            errs.append(f"{where}: runtime font files are never exported (no self-hosted fonts)")
        if r["disposition"]["release"] != "candidate":
            errs.append(f"{where}: register disposition is '{r['disposition']['release']}'")
        a = r["approval"]
        if a.get("status") != "approved" or any(v in (UNKNOWN, None, "") for v in (a.get("evidence"), a.get("date"), r.get("reviewer"))):
            errs.append(f"{where}: no approval with evidence, date and reviewer in the register")
        if r.get("rights_status") != "cleared":
            errs.append(f"{where}: rights_status is not cleared")
        for field in ("intended_uses", "permitted_uses", "restrictions"):
            if r.get(field) in (UNKNOWN, None, "", []):
                errs.append(f"{where}: {field} is UNKNOWN")
        pu = r.get("permitted_uses")
        if isinstance(pu, list) and e.get("use") not in pu:
            errs.append(f"{where}: use '{e.get('use')}' is not among the register's permitted_uses")
        if r.get("notice_required") == UNKNOWN:
            errs.append(f"{where}: notice_required is UNKNOWN")
        elif r.get("notice_required") == "yes":
            for n in r.get("notice_files", []):
                if n not in listed:
                    errs.append(f"{where}: required notice '{n}' is not in the allowlist")
    return errs


def run(root: Path, production: bool, allow_synthetic: bool = False) -> list[str]:
    """allow_synthetic exists for the unit tests only; the CLI never sets it."""
    tracked = set(list_files(root))
    reg, e1 = load_json(root, REGISTER)
    al, e2 = load_json(root, ALLOWLIST)
    errs = e1 + e2
    if reg is not None:
        errs += validate_register(root, reg, tracked)
    if al is not None:
        paths = {r.get("path") for r in reg.get("records", []) if isinstance(r, dict)} if isinstance(reg, dict) else set()
        errs += validate_allowlist_shape(root, al, paths)
    if production:
        if errs:
            return errs + ["production check not evaluated further: fix structural problems first"]
        errs += production_problems(root, reg, al, allow_synthetic)
    return errs


def report(root: Path) -> int:
    reg, e1 = load_json(root, REGISTER)
    al, e2 = load_json(root, ALLOWLIST)
    if e1 or e2 or not isinstance(reg, dict) or not isinstance(al, dict):
        print("\n".join(e1 + e2) or "register or allowlist unreadable")
        return 1
    listed = {e.get("path") for e in al.get("entries", []) if isinstance(e, dict)}
    for r in reg["records"]:
        verdict = "INCLUDE" if r["path"] in listed else "EXCLUDE"
        print(f"{verdict}  {r['classification']:<22} approval={r['approval']['status']:<8} {r['path']}")
        print(f"         {r['disposition']['rationale']}")
    print(f"allowlisted: {len(listed)} of {len(reg['records'])} registered files")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=ROOT)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--register-only", action="store_true", help="structural validation only")
    mode.add_argument("--report", action="store_true", help="print the include/exclude decision report")
    mode.add_argument("--print-hashes", action="store_true", help="print sha256 of in-scope files (refresh aid)")
    args = ap.parse_args(argv)
    root = args.root.resolve()
    if args.print_hashes:
        reg, errs = load_json(root, REGISTER)
        prefixes = reg.get("scope_prefixes", []) if isinstance(reg, dict) else []
        for f in sorted(scope_files(root, prefixes, set(list_files(root)))):
            if (root / f).is_file():
                print(f"{sha256_file(root / f)}  {f}")
        return 0
    if args.report:
        return report(root)
    production = not args.register_only
    errs = run(root, production)
    name = "check-provenance" if production else "check-provenance-register"
    if errs:
        for e in errs:
            print(f"FAIL {e}")
        print(f"{name}: {len(errs)} problem(s)" + (" -- NOT release eligible" if production else ""))
        return 1
    if production:
        print("check-provenance: reviewed allowlist and core evidence pass (this is not a release approval)")
    else:
        print("check-provenance-register: OK (structure, coverage and hashes; UNKNOWN values are allowed here and are not approvals)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
