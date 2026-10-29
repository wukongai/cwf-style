import unittest

from shared.distillation_contract import DistillationError, validate_distillation_request


class DistillationContractTests(unittest.TestCase):
    def test_distillation_is_independent_from_rewrite(self):
        request = {
            "schema_version": "cwf-style-distillation-request/v1",
            "run_id": "distill-run",
            "subject": {"kind": "public_author", "name": "示例作者", "genre": "生活散文", "purpose": "建立可复用档案"},
            "sources": [{"id": "s1", "url": "https://example.com/source", "family": "work-1", "split": "development"}, {"id": "s2", "url": "https://example.com/source-2", "family": "work-2", "split": "holdout"}],
            "outputs": {"profile_id": "demo-style", "status": "research_trial"},
        }
        value = validate_distillation_request(request)
        self.assertEqual(value["subject"]["genre"], "生活散文")

    def test_distillation_does_not_accept_article_rewrite_mode(self):
        request = {"schema_version": "cwf-style-distillation-request/v1", "run_id": "x", "subject": {}, "sources": [], "rewrite_mode": "preserve_structure", "outputs": {}}
        with self.assertRaises(DistillationError):
            validate_distillation_request(request)


if __name__ == "__main__":
    unittest.main()
