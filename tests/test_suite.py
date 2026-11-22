"""Regression tests of multi-skill metadata and reference validation."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.validate_suite import validate, ROOT, EXPECTED


class SuiteValidationTests(unittest.TestCase):
    def test_current_package(self):
        self.assertEqual(validate(ROOT), [])
        self.assertEqual(len(EXPECTED), 3)

    def test_missing_skill_detected(self):
        with TemporaryDirectory() as temp:
            self.assertTrue(any("Expected skill names" in x for x in validate(Path(temp), {"missing-skill"})))

    def test_bad_metadata_detected(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "skills" / "demo-skill"
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text("---\nname: other\ndescription: Sample\n---\n\n# Demo\n")
            self.assertTrue(any("metadata name invalid" in x for x in validate(root, {"demo-skill"})))

    def test_broken_or_escaping_link_detected(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "skills" / "demo-skill"
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(
                "---\nname: demo-skill\ndescription: Demo\n---\n\n[Missing](references/no.md) [Escape](../../README.md)\n")
            results = validate(root, {"demo-skill"})
            self.assertTrue(any("missing or unsafe" in x for x in results))


if __name__ == "__main__":
    unittest.main()
