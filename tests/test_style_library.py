import json
import tempfile
import unittest
from pathlib import Path

from shared.style_library import LibraryError, load_library, resolve_style


class StyleLibraryTests(unittest.TestCase):
    def make_library(self, status="research_trial", availability="callable"):
        root = Path(tempfile.mkdtemp())
        profile = {
            "schema_version": "cwf-public-style-profile/v2",
            "mode": "public_author_research",
            "id": "demo-style",
            "version": "v1",
            "author": "示例作者",
            "scope": ["生活散文"],
            "reviewer_role": "researcher",
            "author_confirmation": False,
            "sources": [{"id": "s1", "family": "demo", "split": "development", "genre": "生活散文", "url": "https://example.com/source", "retrieved_at": "2026-10-30", "observed_text_sha256": "0" * 64, "hash_scope": "sample", "access": "public", "extractor_seen": True}],
            "rules": [{"id": "r1", "instruction": "用具体物事推进", "function": "让材料可见", "scope": "生活散文", "strength": "candidate", "evidence": ["s1"], "boundary": "不虚构经历", "misuse": "不要把每句都写成比喻"}],
            "expression_guides": [{"id": "g1", "genre": "生活散文", "sections": [{"layer": "composition", "text": "先让具体材料承担推进", "rule_ids": ["r1"], "example_ids": []}]}],
        }
        (root / "demo-style.json").write_text(json.dumps(profile, ensure_ascii=False))
        index = {
            "schema_version": "cwf-style-library/v1",
            "entries": [{
                "id": "demo-style",
                "display_name": "示例作者·生活散文",
                "genre": ["生活散文"],
                "profile": "demo-style.json",
                "status": status,
                "availability": availability,
                "preview": "demo-style-preview.md",
                "limitations": ["研究试用，不代表作者确认"],
            }],
        }
        (root / "index.json").write_text(json.dumps(index, ensure_ascii=False))
        return root

    def test_load_and_resolve_callable_style(self):
        root = self.make_library()
        library = load_library(root / "index.json")
        resolved = resolve_style(library, "demo-style", "生活散文")
        self.assertEqual(resolved["profile"]["id"], "demo-style")
        self.assertEqual(resolved["entry"]["status"], "research_trial")

    def test_rejects_unavailable_style(self):
        root = self.make_library(availability="needs_build")
        with self.assertRaises(LibraryError):
            resolve_style(load_library(root / "index.json"), "demo-style", "生活散文")

    def test_rejects_unknown_genre(self):
        root = self.make_library()
        with self.assertRaises(LibraryError):
            resolve_style(load_library(root / "index.json"), "demo-style", "知识科普")


if __name__ == "__main__":
    unittest.main()
