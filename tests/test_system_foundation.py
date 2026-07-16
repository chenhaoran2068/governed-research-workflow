"""Regression checks for released v0.3 foundation and v0.3.1 candidate records."""

from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SYSTEM_ROOT = REPOSITORY_ROOT / "system"
SYSTEM_MANIFEST = REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml"
MODULE_IDS = tuple(f"{index:02d}" for index in range(13))
PRIVATE_MARKERS = ("E:\\\\", "C:\\\\Users", "Research1", "PaCO2")


class SystemFoundationTests(unittest.TestCase):
    def test_each_declared_module_has_a_boundary_record(self) -> None:
        module_directories = sorted(
            path for path in SYSTEM_ROOT.iterdir()
            if path.is_dir() and path.name[:2] in MODULE_IDS
        )
        self.assertEqual([path.name[:2] for path in module_directories], list(MODULE_IDS))
        for module_directory in module_directories:
            self.assertTrue(
                (module_directory / "MODULE.md").is_file(),
                f"Missing boundary record for {module_directory.name}",
            )

    def test_candidate_manifest_uses_the_system_package_root(self) -> None:
        self.assertTrue(SYSTEM_MANIFEST.is_file())
        self.assertFalse((SYSTEM_ROOT / "SYSTEM_MANIFEST.yaml").exists())
        manifest = SYSTEM_MANIFEST.read_text(encoding="utf-8")
        self.assertIn("system_id: governed-research-workflow", manifest)
        self.assertIn("  - standalone", manifest)
        self.assertIn("  - framework_integrated", manifest)
        self.assertIn("framework_compatibility:", manifest)

    def test_system_tree_has_no_private_workspace_markers(self) -> None:
        public_files = [
            *(
                path
                for path in SYSTEM_ROOT.rglob("*")
                if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".json", ".txt"}
            ),
            SYSTEM_MANIFEST,
        ]
        public_text = "\n".join(path.read_text(encoding="utf-8") for path in public_files)
        for marker in PRIVATE_MARKERS:
            self.assertNotIn(marker, public_text)


if __name__ == "__main__":
    unittest.main()
