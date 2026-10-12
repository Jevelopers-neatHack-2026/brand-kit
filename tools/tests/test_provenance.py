"""Tests for tools/check_provenance.py. Run: python3 -m unittest discover -s tools/tests

Every fixture is SYNTHETIC: invented files, invented reviewer, invented evidence. None of it is a real
approval, rights clearance or review, and the production check refuses synthetic data unless a test
explicitly opts in.
"""
import contextlib
import io
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
import check_provenance as cp  # noqa: E402

SYN = "SYNTHETIC FIXTURE - NOT A REAL APPROVAL"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


class Fixture(unittest.TestCase):
    FILES = {"logo/mark.svg": b"<svg>synthetic mark</svg>", "logo/notice.txt": b"synthetic notice text",
             "references/ref.webp": b"synthetic reference bytes", "fonts/F.ttf": b"synthetic font bytes",
             "fonts/F-OFL.txt": b"synthetic font notice", "docs/evidence.md": b"synthetic evidence doc"}

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for rel, data in self.FILES.items():
            (self.tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.tmp / rel).write_bytes(data)
        self.reg = {"schema_version": 1, "synthetic": True, "hash_algorithm": "sha256", "source_revision": "synthetic",
                    "scope_prefixes": ["logo/", "references/", "fonts/"], "statement": SYN,
                    "records": [
                        self.rec("logo/mark.svg", "first-party-canonical", release="candidate", approved=True,
                                 notice_required="yes", notice_files=["logo/notice.txt"]),
                        self.rec("logo/notice.txt", "licence-notice", release="excluded", notice_required="no"),
                        self.rec("references/ref.webp", "reference-unknown", release="excluded"),
                        self.rec("fonts/F.ttf", "licensed-dependency", release="excluded", notice_required="yes",
                                 notice_files=["fonts/F-OFL.txt"]),
                        self.rec("fonts/F-OFL.txt", "licence-notice", release="excluded", notice_required="no")]}
        self.reg["records"][3]["core"] = False
        self.al = {"schema_version": 1, "synthetic": True, "status": "reviewed", "source_revision": "synthetic",
                   "statement": SYN,
                   "review": {"reviewer": "synthetic-reviewer", "evidence": "docs/evidence.md", "date": "2000-01-01"},
                   "entries": [self.entry("logo/mark.svg"), self.entry("logo/notice.txt")]}
        self.write()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def rec(self, path, cls, release, approved=False, notice_required="no", notice_files=()):
        data = self.FILES[path]
        r = dict(path=path, sha256=sha(data), size_bytes=len(data), introduced_in="synthetic", classification=cls,
                 core=cls.startswith("first-party"), origin=SYN, origin_evidence=["docs/evidence.md"],
                 creator_rights_holder=SYN, source_version=cp.UNKNOWN, derivation=cp.UNKNOWN, tooling=cp.UNKNOWN,
                 notice_required=notice_required, notice_files=list(notice_files),
                 rights_status="cleared" if approved else cp.UNKNOWN,
                 intended_uses=["synthetic use"], permitted_uses=["synthetic use"] if approved else cp.UNKNOWN,
                 restrictions=["synthetic restriction"] if approved else cp.UNKNOWN,
                 reviewer="synthetic-reviewer" if approved else cp.UNKNOWN,
                 approval=dict(status="approved" if approved else cp.UNKNOWN,
                               evidence="docs/evidence.md" if approved else cp.UNKNOWN,
                               date="2000-01-01" if approved else cp.UNKNOWN),
                 disposition=dict(release=release, rationale=SYN), notes=[SYN])
        if cls == "licence-notice":
            r["core"] = False
        return r

    def entry(self, path):
        return {"path": path, "sha256": sha(self.FILES[path]), "use": "synthetic use"}

    def approve_notice(self):
        # a notice that ships must itself be an eligible, approved record
        n = self.reg["records"][1]
        n.update(classification="first-party-canonical", rights_status="cleared", permitted_uses=["synthetic use"],
                 restrictions=["synthetic restriction"], reviewer="synthetic-reviewer", core=False)
        n["approval"] = dict(status="approved", evidence="docs/evidence.md", date="2000-01-01")
        n["disposition"]["release"] = "candidate"

    def write(self):
        (self.tmp / "provenance").mkdir(exist_ok=True)
        (self.tmp / cp.REGISTER).write_text(json.dumps(self.reg))
        (self.tmp / cp.ALLOWLIST).write_text(json.dumps(self.al))

    def structural(self):
        return "\n".join(cp.run(self.tmp, False))

    def production(self, synthetic_ok=True):
        return "\n".join(cp.run(self.tmp, True, allow_synthetic=synthetic_ok))


class RegisterTests(Fixture):
    def test_valid_register_passes(self):
        self.assertEqual(self.structural(), "")

    def test_unknowns_are_honest_and_pass(self):
        self.assertEqual(self.structural(), "")  # reference + font records are all UNKNOWN

    def test_missing_hash_field(self):
        del self.reg["records"][0]["sha256"]
        self.write()
        self.assertIn("missing field 'sha256'", self.structural())

    def test_malformed_hash(self):
        self.reg["records"][0]["sha256"] = "abc"
        self.write()
        self.assertIn("64 lowercase hex", self.structural())

    def test_stale_bytes(self):
        (self.tmp / "logo/mark.svg").write_bytes(b"changed after registration")
        self.assertIn("does not match the file bytes", self.structural())

    def test_unregistered_file(self):
        (self.tmp / "logo/new.svg").write_bytes(b"x")
        self.assertIn("unregistered file: logo/new.svg", self.structural())

    def test_registered_file_removed(self):
        (self.tmp / "references/ref.webp").unlink()
        out = self.structural()
        self.assertIn("file does not exist", out)

    def test_empty_field_must_say_unknown(self):
        self.reg["records"][2]["origin"] = ""
        self.write()
        self.assertIn("write UNKNOWN", self.structural())

    def test_missing_register_input(self):
        (self.tmp / cp.REGISTER).unlink()
        self.assertIn("missing required input", self.structural())
        self.assertIn("missing required input", self.production())

    def test_missing_allowlist_input(self):
        (self.tmp / cp.ALLOWLIST).unlink()
        self.assertIn("missing required input", self.structural())

    def test_invalid_json(self):
        (self.tmp / cp.REGISTER).write_text("{")
        self.assertIn("invalid JSON", self.structural())

    def test_path_traversal_in_register(self):
        for bad in ("../outside.svg", "/etc/passwd", "logo/../../x", "logo//x.svg", "logo\\x.svg"):
            self.reg["records"][0]["path"] = bad
            self.write()
            self.assertTrue(cp.run(self.tmp, False), bad)

    def test_path_traversal_in_allowlist(self):
        self.al["entries"][0]["path"] = "../x"
        self.write()
        self.assertIn("traversal", self.structural())

    def test_symlink_escape(self):
        outside = Path(tempfile.mkdtemp())
        try:
            (outside / "secret.svg").write_bytes(b"x")
            (self.tmp / "logo/link.svg").symlink_to(outside / "secret.svg")
            self.reg["records"].append(self.rec("logo/mark.svg", "first-party-canonical", "candidate"))
            self.reg["records"][-1]["path"] = "logo/link.svg"
            self.write()
            self.assertIn("symlink", self.structural())
        finally:
            shutil.rmtree(outside)

    def test_reference_cannot_be_first_party(self):
        self.reg["records"][2]["classification"] = "first-party-canonical"
        self.write()
        self.assertIn("cannot be classified first-party", self.structural())

    def test_reference_must_be_excluded(self):
        self.reg["records"][2]["disposition"]["release"] = "candidate"
        self.write()
        self.assertIn("must have disposition.release 'excluded'", self.structural())

    def test_font_must_stay_source_only(self):
        self.reg["records"][3]["disposition"]["release"] = "candidate"
        self.write()
        self.assertIn("source-only", self.structural())

    def test_approved_needs_evidence(self):
        self.reg["records"][0]["approval"]["evidence"] = cp.UNKNOWN
        self.write()
        self.assertIn("approved but approval.evidence is UNKNOWN", self.structural())

    def test_notice_required_needs_files(self):
        self.reg["records"][0]["notice_files"] = []
        self.write()
        self.assertIn("notice_files is empty", self.structural())

    def test_notice_file_must_be_registered(self):
        self.reg["records"][0]["notice_files"] = ["logo/ghost.txt"]
        self.write()
        self.assertIn("not a register record", self.structural())

    def test_secret_like_string_rejected_without_echo(self):
        token = "ghp_" + "a" * 30
        self.reg["records"][2]["notes"] = [f"see {token}"]
        self.write()
        out = self.structural()
        self.assertIn("GitHub token", out)
        self.assertNotIn(token, out)

    def test_email_and_url_credentials_rejected(self):
        self.reg["records"][2]["notes"] = ["contact someone@example.com"]
        self.write()
        self.assertIn("email address", self.structural())
        self.reg["records"][2]["notes"] = ["https://x.example/a?sig=1234"]
        self.write()
        self.assertIn("URL with credentials or query", self.structural())

    def test_evidence_must_be_safe_reference(self):
        self.reg["records"][2]["origin_evidence"] = ["docs/ghost.md"]
        self.write()
        self.assertIn("not a tracked file", self.structural())
        self.reg["records"][2]["origin_evidence"] = ["restricted:contract-17"]
        self.write()
        self.assertEqual(self.structural(), "")


class ProductionTests(Fixture):
    def setUp(self):
        super().setUp()
        self.approve_notice()
        self.write()

    def test_valid_synthetic_fixture_passes_only_when_opted_in(self):
        self.assertEqual(self.production(), "")
        self.assertIn("synthetic fixture data can never be release evidence", self.production(synthetic_ok=False))

    def test_real_repository_fails_production_closed(self):
        # The shipped allowlist is empty and core rights are UNKNOWN, so production must never pass here.
        # (Structure of the real register is covered by `make check-provenance-register`.)
        root = HERE.parents[2]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cp.main(["--root", str(root)]), 1)
        al = json.loads((root / cp.ALLOWLIST).read_text())
        self.assertEqual(al["entries"], [])
        self.assertFalse(al["synthetic"])

    def test_empty_allowlist_fails(self):
        self.al["entries"] = []
        self.write()
        self.assertIn("allowlist is empty", self.production())

    def test_unreviewed_allowlist_fails(self):
        self.al["review"]["reviewer"] = cp.UNKNOWN
        self.al["status"] = "draft"
        self.write()
        out = self.production()
        self.assertIn("review.reviewer is UNKNOWN", out)
        self.assertIn("not 'reviewed'", out)

    def test_unknown_approval_fails(self):
        self.reg["records"][0]["approval"] = dict(status=cp.UNKNOWN, evidence=cp.UNKNOWN, date=cp.UNKNOWN)
        self.write()
        self.assertIn("no approval with evidence", self.production())

    def test_unknown_core_rights_block_even_with_valid_allowlist(self):
        self.reg["records"][0]["rights_status"] = cp.UNKNOWN
        self.write()
        out = self.production()
        self.assertIn("core asset rights/approval not cleared", out)
        self.assertIn("rights_status is not cleared", out)

    def test_core_unknown_elsewhere_blocks(self):
        extra = self.rec("logo/mark.svg", "first-party-canonical", "candidate")
        extra["path"] = "logo/extra.svg"
        (self.tmp / "logo/extra.svg").write_bytes(self.FILES["logo/mark.svg"])
        self.reg["records"].append(extra)
        self.write()
        self.assertIn("core asset rights/approval not cleared", self.production())

    def test_internal_only_fails(self):
        self.reg["records"][0]["classification"] = "internal"
        self.write()
        self.assertIn("excluded", self.production())

    def test_thirdparty_candidate_fails(self):
        self.reg["records"][0]["classification"] = "third-party-candidate"
        self.write()
        self.assertIn("excluded", self.production())

    def test_reference_in_allowlist_fails(self):
        self.al["entries"].append(self.entry_for_ref())
        self.write()
        self.assertIn("excluded from release", self.production())

    def entry_for_ref(self):
        return {"path": "references/ref.webp", "sha256": sha(self.FILES["references/ref.webp"]), "use": "synthetic use"}

    def test_font_in_allowlist_fails(self):
        self.al["entries"].append({"path": "fonts/F.ttf", "sha256": sha(self.FILES["fonts/F.ttf"]), "use": "x"})
        self.write()
        self.assertIn("never exported", self.production())

    def test_missing_notice_fails(self):
        self.al["entries"] = [self.entry("logo/mark.svg")]
        self.write()
        self.assertIn("required notice 'logo/notice.txt' is not in the allowlist", self.production())

    def test_notice_requirement_unknown_fails(self):
        self.reg["records"][0]["notice_required"] = cp.UNKNOWN
        self.reg["records"][0]["notice_files"] = []
        self.write()
        self.assertIn("notice_required is UNKNOWN", self.production())

    def test_allowlist_hash_missing_or_wrong_fails(self):
        self.al["entries"][0]["sha256"] = "0" * 64
        self.write()
        self.assertIn("allowlist hash does not match", self.production())
        del self.al["entries"][0]["sha256"]
        self.write()
        self.assertIn("sha256 must be 64", "\n".join(cp.run(self.tmp, True, allow_synthetic=True)))

    def test_stale_bytes_fail_production(self):
        (self.tmp / "logo/mark.svg").write_bytes(b"edited after approval")
        out = self.production()
        self.assertIn("does not match", out)

    def test_use_not_permitted_fails(self):
        self.al["entries"][0]["use"] = "something else"
        self.write()
        self.assertIn("not among the register's permitted_uses", self.production())

    def test_missing_permitted_uses_fails(self):
        self.reg["records"][0]["permitted_uses"] = cp.UNKNOWN
        self.write()
        self.assertIn("permitted_uses is UNKNOWN", self.production())

    def test_unreviewed_entry_not_in_register_fails(self):
        self.al["entries"].append({"path": "logo/ghost.svg", "sha256": "0" * 64, "use": "x"})
        self.write()
        self.assertIn("not in the register", self.production())

    def test_path_traversal_fails(self):
        self.al["entries"][0]["path"] = "../../etc/passwd"
        self.write()
        self.assertIn("traversal", self.production())

    def test_missing_inputs_fail(self):
        (self.tmp / cp.ALLOWLIST).unlink()
        self.assertIn("missing required input", self.production())


if __name__ == "__main__":
    unittest.main()
