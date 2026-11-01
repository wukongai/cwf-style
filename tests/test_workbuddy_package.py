import re
import unittest
from pathlib import Path


class WorkBuddyPackageTests(unittest.TestCase):
    REQUIRED_FRONTMATTER = {
        "name",
        "display_name",
        "display_name_zh",
        "display_name_en",
        "description",
        "description_zh",
        "description_en",
        "author",
        "version",
    }

    def test_each_skill_has_workbuddy_metadata_and_contract(self):
        root = Path(__file__).resolve().parents[1]
        for skill_dir in sorted((root / "skills").iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            contract = skill_dir / "skill.contract.yaml"
            self.assertTrue(skill_md.exists(), skill_dir)
            self.assertTrue(contract.exists(), skill_dir)
            text = skill_md.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), skill_md)
            frontmatter = text.split("---\n", 2)[1]
            fields = set(re.findall(r"^([A-Za-z_][A-Za-z0-9_]*):", frontmatter, re.MULTILINE))
            self.assertTrue(self.REQUIRED_FRONTMATTER <= fields, (skill_md, self.REQUIRED_FRONTMATTER - fields))
            self.assertIn("utility_claim: false", contract.read_text(encoding="utf-8"))

    def test_workbuddy_install_guide_names_the_supported_user_directory(self):
        root = Path(__file__).resolve().parents[1]
        guide = (root / "docs" / "WORKBUDDY.md").read_text(encoding="utf-8")
        self.assertIn("$HOME/.workbuddy/skills/", guide)
        self.assertIn("cwf-style-distillation", guide)
        self.assertIn("cwf-article-rewrite", guide)


if __name__ == "__main__":
    unittest.main()
