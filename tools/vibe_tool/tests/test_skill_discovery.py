import tempfile
import unittest
from pathlib import Path

from vibe_tool.discovery import discover_manifests, discover_skills, resolve_skill


class SkillsDiscoveryTests(unittest.TestCase):
    def _make_manifest(self, root: Path, name: str, skills_txt: str) -> list:
        mdir = root / "manifests" / name
        mdir.mkdir(parents=True)
        (mdir / "CLAUDE.md").write_text("# Test Manifest\n", encoding="utf-8")
        (mdir / "skills.txt").write_text(skills_txt, encoding="utf-8")
        return discover_manifests(root / "manifests")

    def test_required_skills_parsed_from_skills_txt(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifests = self._make_manifest(
                Path(tmp),
                "demo",
                "# comment\npaper-write\n\npaper-compile  # trailing\n",
            )
            self.assertEqual(len(manifests), 1)
            self.assertEqual(manifests[0].required_skills, ["paper-write", "paper-compile"])

    def test_no_skills_txt_means_empty_required_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifests = self._make_manifest(Path(tmp), "plain", "")
            self.assertEqual(manifests[0].required_skills, [])

    def test_discover_skills_across_multiple_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = root / "skills-a" / "foo" / "SKILL.md"
            a.parent.mkdir(parents=True)
            a.write_text("---\nname: foo\n---\n", encoding="utf-8")
            b = root / "skills-b" / "bar" / "SKILL.md"
            b.parent.mkdir(parents=True)
            b.write_text("---\nname: bar\n---\n", encoding="utf-8")

            skills = discover_skills(root / "skills-a", root / "skills-b")
            names = {s.name for s in skills}
            self.assertEqual(names, {"foo", "bar"})

            resolved = resolve_skill((root / "skills-a", root / "skills-b"), "bar")
            self.assertEqual(resolved.name, "bar")


if __name__ == "__main__":
    unittest.main()