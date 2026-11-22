from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from scripts.check_asset_snapshot import check, ROOT


class AssetSnapshotTests(unittest.TestCase):
    def test_pinned_source_matches(self):
        self.assertEqual(check(ROOT), [])

    def test_modified_file_is_detected(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "upstream").mkdir()
            (root / "skills/roblox-asset-workflow").mkdir(parents=True)
            (root / "upstream/asset-v3.2.0.json").write_text(
                json.dumps({"tag": "v3.2.0", "files": {"SKILL.md": "0" * 40}}))
            (root / "skills/roblox-asset-workflow/SKILL.md").write_text("not original")
            self.assertTrue(any("differs" in issue for issue in check(root)))


if __name__ == "__main__":
    unittest.main()
