import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location("skill_run", Path(__file__).with_name("skill_run.py"))
skill_run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(skill_run)


class SkillRunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "example"
        self.skill.mkdir()
        (self.skill / "SKILL.md").write_text("# 원본\n[참조](references/input.bin)\n")
        (self.skill / "references").mkdir()
        (self.skill / "references/input.bin").write_bytes(b"\x00\xffsource")
        self.work = self.root / "work"

    def create(self, skills=None):
        result = skill_run.create_run(skills or [self.skill], self.work, "codex://threads/test", "Asia/Seoul")
        return Path(result["run"])

    def test_complete_copy_preserves_references_and_original(self):
        run = self.create()
        for kind in ("source", "working"):
            self.assertEqual((run / kind / "example/references/input.bin").read_bytes(), b"\x00\xffsource")
        working = run / "working/example/SKILL.md"
        working.write_text(working.read_text() + "{>>실행=진행<<}\n")
        self.assertNotIn("실행", (self.skill / "SKILL.md").read_text())
        self.assertEqual(skill_run.verify_run(run)["verified_files"], 2)

    def test_distinct_runs_do_not_overwrite(self):
        first, second = self.create(), self.create()
        self.assertNotEqual(first, second)
        self.assertTrue(first.is_dir())
        manifest = json.loads((first / "manifest.json").read_text())
        self.assertTrue(manifest["created_at"].endswith("+09:00"))

    def test_modified_snapshot_fails(self):
        run = self.create()
        (run / "source/example/SKILL.md").write_text("altered")
        with self.assertRaisesRegex(ValueError, "content changed"):
            skill_run.verify_run(run)

    def test_added_snapshot_file_fails(self):
        run = self.create()
        (run / "source/example/extra.txt").write_text("unrecorded")
        with self.assertRaisesRegex(ValueError, "file set changed"):
            skill_run.verify_run(run)

    def test_current_original_can_change_without_rewriting_snapshot(self):
        run = self.create()
        (self.skill / "SKILL.md").write_text("new version")
        self.assertIn("원본", (run / "source/example/SKILL.md").read_text())
        self.assertEqual(skill_run.verify_run(run)["verified_files"], 2)

    def test_symlink_and_recursive_output_are_rejected(self):
        (self.skill / "linked").symlink_to(self.skill / "SKILL.md")
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.create()
        self.assertFalse(list(self.work.glob(".skill-run-*")))
        with self.assertRaisesRegex(ValueError, "inside"):
            skill_run.create_run([self.skill], self.skill / "output", "test")

    def test_duplicate_names_are_rejected(self):
        second = self.root / "other/example"
        second.mkdir(parents=True)
        (second / "SKILL.md").write_text("other")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.create([self.skill, second])


if __name__ == "__main__":
    unittest.main()
