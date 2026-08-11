"""Regression checks for the released v0.3 foundation and v0.3.1 records."""

from pathlib import Path
import re
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SYSTEM_ROOT = REPOSITORY_ROOT / "system"
SYSTEM_MANIFEST = REPOSITORY_ROOT / "SYSTEM_MANIFEST.yaml"
MODULE_IDS = tuple(f"{index:02d}" for index in range(13))
PRIVATE_PATH_PATTERN = r"(?i)(?:[a-z]:\\|/(?:home|users)/)"


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
        self.assertIn("system_version: 1.14.0", manifest)

    def test_v15_guidance_documents_are_present_and_route_only_to_human_review(self) -> None:
        workflow_root = SYSTEM_ROOT / "03_workflows"
        manuscript = workflow_root / "MANUSCRIPT_OPERATIONAL_CHECKLISTS.md"
        boundary = workflow_root / "RESEARCH_PROGRAM_BOUNDARY_AND_SHARED_MATERIALS_CONTROL.md"
        for path in (manuscript, boundary):
            self.assertTrue(path.is_file(), path)
            text = path.read_text(encoding="utf-8").lower()
            self.assertIn("human", text)
            self.assertIn("does not", text)

        self.assertIn("optional", manuscript.read_text(encoding="utf-8").lower())
        self.assertIn("isolated by default", boundary.read_text(encoding="utf-8").lower())

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
        self.assertIsNone(re.search(PRIVATE_PATH_PATTERN, public_text))


if __name__ == "__main__":
    unittest.main()
