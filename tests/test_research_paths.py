"""端末切替で研究データを作成・変更せず、入力場所だけを変えられることを確認する。"""

import json
from pathlib import Path
import tempfile
import unittest

from src.research_paths import load_paths


class ResearchPathsTests(unittest.TestCase):
    def test_profiles_change_roots_without_creating_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "paths.json"
            keys = ["project_root", "data_root", "output_root", "cache_root"]
            config.write_text(json.dumps({"profiles": {
                profile: {key: str(root / profile / key) for key in keys}
                for profile in ["mac", "server"]
            }}))
            mac = load_paths(config, "mac")
            server = load_paths(config, "server")
            relative = Path("runs/study/hash/run/raw/history.csv")
            self.assertEqual((mac.data_root / relative).relative_to(mac.data_root), relative)
            self.assertEqual((server.data_root / relative).relative_to(server.data_root), relative)
            self.assertNotEqual(mac.data_root, server.data_root)
            self.assertFalse(mac.data_root.exists())
            self.assertFalse(server.output_root.exists())

    def test_missing_profile_and_unsafe_defaults_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "paths.json"
            keys = ["project_root", "data_root", "output_root", "cache_root"]
            for value in ["", "relative/path", "/absolute/path/to/example", None]:
                with self.subTest(value=value):
                    config.write_text(json.dumps({"profiles": {"mac": {
                        key: value for key in keys
                    }}}))
                    with self.assertRaises(ValueError):
                        load_paths(config, "mac")
            with self.assertRaises(ValueError):
                load_paths(config, "server")


if __name__ == "__main__":
    unittest.main()
