import unittest

from shared.rewrite_contract import ContractError, build_writer_input, validate_request


BASE = {
    "schema_version": "cwf-article-rewrite-request/v1",
    "run_id": "demo-run",
    "source": {"kind": "existing_article", "title": "原文", "text": "这是一篇完整的原文，而不是主题摘要。"},
    "task": {"genre": "生活散文", "audience": "普通读者", "length": {"min_han": 100, "max_han": 300}},
    "rewrite": {
        "mode": "preserve_structure",
        "preserve": {"structure": ["开头场景", "中段转折"], "core_meaning": "保留原意"},
        "change": {"language": True, "structure": False},
        "new_material_policy": "只使用用户提供材料",
    },
    "style": None,
}


class RewriteContractTests(unittest.TestCase):
    def test_preserve_structure_accepts_full_source(self):
        value = validate_request(BASE)
        self.assertEqual(value["rewrite_mode"], "preserve_structure")
        self.assertTrue(value["source_han"] > 0)

    def test_rebuild_requires_reorganization_plan(self):
        request = dict(BASE)
        request["rewrite"] = {
            "mode": "rebuild_from_thread",
            "preserve": {"main_thread": "保留主线", "key_people_events": ["人物与事件"], "core_meaning": "保留原意"},
            "change": {"structure": True},
            "new_material_policy": "只使用用户提供材料",
        }
        with self.assertRaises(ContractError):
            validate_request(request)
        request["rewrite"]["reorganization_plan"] = ["从中段动作开篇", "把原开头意象移到转折", "结尾回收主线"]
        value = validate_request(request)
        self.assertEqual(value["rewrite_mode"], "rebuild_from_thread")

    def test_meaning_rewrite_does_not_require_old_elements(self):
        request = dict(BASE)
        request["rewrite"] = {
            "mode": "rewrite_from_meaning",
            "preserve": {"core_meaning": "保留原文的核心意旨", "stance": "保留立场", "emotional_landing": "保留情感落点"},
            "change": {"structure": True, "materials": True},
            "new_material_policy": "新增材料必须来自用户提供内容",
        }
        value = validate_request(request)
        self.assertEqual(value["rewrite_mode"], "rewrite_from_meaning")

    def test_writer_input_keeps_source_and_mode(self):
        value = build_writer_input(BASE, style_payload=None)
        self.assertEqual(value["task"]["genre"], "生活散文")
        self.assertEqual(value["rewrite"]["mode"], "preserve_structure")
        self.assertIn("完整的原文", value["source_text"])

    def test_rejects_topic_only_source(self):
        request = dict(BASE)
        request["source"] = {"kind": "existing_article", "title": "原文", "summary": "只是一句主题摘要"}
        with self.assertRaises(ContractError):
            validate_request(request)


if __name__ == "__main__":
    unittest.main()
