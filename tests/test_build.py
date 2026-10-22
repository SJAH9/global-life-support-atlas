import unittest

from src.build_atlas import ROOT, build


class AtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = build()

    def test_nine_distinct_domains(self):
        ids = [item["id"] for item in self.payload["domains"]]
        self.assertEqual(len(ids), 9)
        self.assertEqual(len(set(ids)), 9)

    def test_public_source_does_not_open_participation(self):
        project = self.payload["project"]
        self.assertEqual(project["visibility"], "public")
        self.assertFalse(project["participation_enabled"])
        self.assertIsNone(project["launch_date"])

    def test_no_score_without_complete_evidence(self):
        self.assertEqual(self.payload["summary"]["observations"], 0)
        self.assertEqual(self.payload["summary"]["scored_regions"], 0)
        self.assertTrue(all(item["score"] is None for item in self.payload["regions"]))

    def test_information_pages_exist(self):
        for name in ("about.html","method.html","data.html","participate.html"):
            self.assertTrue((ROOT / "web" / name).exists())


if __name__ == "__main__":
    unittest.main()
