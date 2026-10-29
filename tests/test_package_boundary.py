import unittest
from pathlib import Path


class PackageBoundaryTests(unittest.TestCase):
    def test_public_candidate_has_no_private_or_credential_names(self):
        root = Path(__file__).resolve().parents[1]
        forbidden_parts = {".env", ".backups", ".skill-engineering", "cookie", "token", "private"}
        offenders = []
        for path in root.rglob("*"):
            if ".git" in path.parts or not path.is_file():
                continue
            if any(part in forbidden_parts for part in path.parts):
                offenders.append(str(path.relative_to(root)))
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
