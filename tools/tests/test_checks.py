"""Negative and positive tests for the BK-01 checks. Run: python3 -m unittest discover -s tools/tests"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
import check_inventory  # noqa: E402
import check_links  # noqa: E402
from inventory_lib import INVENTORY, ROOT  # noqa: E402


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for rel in ("README.md", "docs/source-of-truth.md", "SPEC.md"):
            (self.tmp / rel).parent.mkdir(parents=True, exist_ok=True)
        (self.tmp / "README.md").write_text("[idx](docs/source-of-truth.md) [spec](SPEC.md#colour)\n")
        (self.tmp / "SPEC.md").write_text("# Colour\n")
        (self.tmp / "docs/source-of-truth.md").write_text("SPEC.md\n")
        self.entries = [self.entry(p) for p in ("README.md", "SPEC.md", "docs/source-of-truth.md", INVENTORY)]
        self.write()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    @staticmethod
    def entry(path):
        return dict(id=path, path=path, type="x", category="c", classification="guideline", description="d",
                    owner_role="o", approval_status="unknown", provenance_status="unknown",
                    release_class="internal", canonical_authority=path)

    def write(self):
        inv = dict(enums={"approval_status": ["unknown"]}, entries=self.entries,
                   source_of_truth=[dict(topic="t", paths=["SPEC.md"])], path_map=[])
        p = self.tmp / INVENTORY
        p.parent.mkdir(exist_ok=True)
        p.write_text(json.dumps(inv))

    def problems(self):
        return "\n".join(check_inventory.check(self.tmp))


class InventoryTests(Fixture):
    def test_valid_fixture_passes(self):
        self.assertEqual(check_inventory.check(self.tmp), [])

    def test_missing_path(self):
        self.entries.append(self.entry("logo/ghost.svg"))
        self.write()
        self.assertIn("path does not exist", self.problems())

    def test_duplicate_entry(self):
        self.entries.append(dict(self.entries[1]))
        self.write()
        self.assertIn("duplicate id", self.problems())
        self.assertIn("duplicate path", self.problems())

    def test_uncatalogued_asset(self):
        (self.tmp / "logo").mkdir()
        (self.tmp / "logo/new.svg").write_text("<svg/>")
        self.assertIn("uncatalogued file: logo/new.svg", self.problems())

    def test_broken_canonical_link(self):
        self.entries[1]["canonical_authority"] = "tokens/missing.json"
        self.write()
        self.assertIn("not a catalogued path", self.problems())

    def test_missing_inventory_is_error(self):
        (self.tmp / INVENTORY).unlink()
        self.assertIn("missing required input", self.problems())

    def test_unknown_must_be_explicit(self):
        del self.entries[1]["approval_status"]
        self.write()
        self.assertIn("missing required field 'approval_status'", self.problems())

    def test_cli_exit_codes(self):
        self.assertEqual(check_inventory.main(["--root", str(self.tmp)]), 0)
        (self.tmp / "stray.txt").write_text("x")
        self.assertEqual(check_inventory.main(["--root", str(self.tmp)]), 1)


class LinkTests(Fixture):
    def test_valid_links_pass(self):
        errors, ext, ok = check_links.check(self.tmp)
        self.assertEqual(errors, [])

    def test_broken_local_link(self):
        (self.tmp / "README.md").write_text("[x](docs/nope.md)\n")
        errors, _, _ = check_links.check(self.tmp)
        self.assertTrue(any("broken local link" in e for e in errors))
        self.assertEqual(check_links.main(["--root", str(self.tmp)]), 1)

    def test_missing_anchor(self):
        (self.tmp / "README.md").write_text("[x](SPEC.md#nothing)\n")
        errors, _, _ = check_links.check(self.tmp)
        self.assertTrue(any("missing anchor" in e for e in errors))

    def test_html_and_css_links(self):
        (self.tmp / "index.html").write_text('<img src="gone.webp"><style>a{background:url(gone2.png)}</style>')
        errors, _, _ = check_links.check(self.tmp)
        self.assertEqual(len([e for e in errors if "index.html" in e]), 2)

    def test_external_not_verified_offline(self):
        (self.tmp / "README.md").write_text("[x](https://example.invalid/a)\n")
        errors, ext, _ = check_links.check(self.tmp)
        self.assertEqual(errors, [])
        self.assertEqual(ext, {"https://example.invalid/a"})

    def test_code_blocks_ignored(self):
        (self.tmp / "README.md").write_text("```\n[x](nope.md)\n```\n`[y](nope2.md)`\n")
        self.assertEqual(check_links.check(self.tmp)[0], [])


class RealRepo(unittest.TestCase):
    def test_repository_passes(self):
        self.assertEqual(check_inventory.check(ROOT), [])
        self.assertEqual(check_links.check(ROOT)[0], [])


if __name__ == "__main__":
    unittest.main()
