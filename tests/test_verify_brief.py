import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "verify_brief.py"


def load_module():
    spec = importlib.util.spec_from_file_location("verify_brief", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class VerifyBriefTests(unittest.TestCase):
    def make_files(self, html, registry):
        directory = Path(tempfile.mkdtemp())
        brief = directory / "brief.html"
        manifest = directory / "brief.sources.json"
        brief.write_text(html, encoding="utf-8")
        manifest.write_text(json.dumps(registry), encoding="utf-8")
        return brief, manifest

    def test_accepts_claim_with_listed_source_and_verification_metadata(self):
        verifier = load_module()
        brief, manifest = self.make_files(
            '<p data-claim-id="finding">Claim<sup><a href="#ref1">1</a></sup></p><div class="references-list"><ol><li id="ref1">Trial <a href="https://doi.org/10.1/example">doi</a>; PMID:123</li></ol></div>',
            {"sources": [{"citation": 1, "reference_id": "ref1", "doi": "10.1/example", "pmid": "123", "evidence_level": "Human RCT", "claims": ["Claim"], "claim_ids": ["finding"], "verification_note": "Abstract checked."}]},
        )
        self.assertEqual([], verifier.verify_brief(brief, manifest))

    def test_rejects_citation_without_registry_record(self):
        verifier = load_module()
        brief, manifest = self.make_files('<p>Claim<sup>1</sup></p><ol><li>Trial doi:10.1/example</li></ol>', {"sources": []})
        errors = verifier.verify_brief(brief, manifest)
        self.assertTrue(any("citation 1" in error for error in errors))

    def test_rejects_registry_source_not_listed_in_brief(self):
        verifier = load_module()
        brief, manifest = self.make_files('<p>Claim<sup>1</sup></p><div class="references-list"><ol><li>Trial doi:10.1/example</li></ol></div>', {"sources": [{"citation": 1, "doi": "10.9/not-listed", "evidence_level": "Human RCT", "claims": ["Claim"], "verification_note": "Abstract checked."}]})
        errors = verifier.verify_brief(brief, manifest)
        self.assertTrue(any("does not match" in error for error in errors))

    def test_rejects_missing_claim_or_verification_note(self):
        verifier = load_module()
        brief, manifest = self.make_files('<p>Claim<sup>1</sup></p><ol><li>Trial doi:10.1/example</li></ol>', {"sources": [{"citation": 1, "doi": "10.1/example", "evidence_level": "Human RCT", "claims": [], "verification_note": ""}]})
        errors = verifier.verify_brief(brief, manifest)
        self.assertTrue(any("claims" in error for error in errors))
        self.assertTrue(any("verification_note" in error for error in errors))
    def test_indexes_only_the_dedicated_reference_list(self):
        verifier = load_module()
        brief, manifest = self.make_files(
            '<ul><li>Not a reference</li></ul><p data-claim-id="finding">Claim<sup><a href="#ref1">1</a></sup></p><div class="references-list"><ol><li id="ref1">Trial doi:10.1/example</li></ol></div>',
            {"sources": [{"citation": 1, "reference_id": "ref1", "doi": "10.1/example", "evidence_level": "Human RCT", "claims": ["Claim"], "claim_ids": ["finding"], "verification_note": "Abstract checked."}]},
        )
        self.assertEqual([], verifier.verify_brief(brief, manifest))
    def test_rejects_unrelated_registered_claim(self):
        verifier = load_module()
        brief, manifest = self.make_files(
            '<p data-claim-id="omad">OMAD claim<sup>1</sup></p><div class="references-list"><ol><li id="ref1">Trial doi:10.1/example</li></ol></div>',
            {"sources": [{"citation": 1, "reference_id": "ref1", "doi": "10.1/example", "evidence_level": "Human RCT", "claims": ["Unrelated claim"], "claim_ids": ["different-claim"], "verification_note": "Abstract checked."}]},
        )
        errors = verifier.verify_brief(brief, manifest)
        self.assertTrue(any("claim" in error for error in errors))

    def test_rejects_source_without_claim_ids(self):
        verifier = load_module()
        brief, manifest = self.make_files(
            '<p data-claim-id="finding">Claim<sup><a href="#ref1">1</a></sup></p><div class="references-list"><ol><li id="ref1">Trial doi:10.1/example</li></ol></div>',
            {"sources": [{"citation": 1, "reference_id": "ref1", "doi": "10.1/example", "pmid": "123", "evidence_level": "Human RCT", "claims": ["Claim"], "verification_note": "Abstract checked."}]},
        )
        errors = verifier.verify_brief(brief, manifest)
        self.assertTrue(any("claim_ids" in error for error in errors))

    def test_rejects_partial_claim_mapping(self):
        verifier = load_module()
        brief, manifest = self.make_files(
            '<p data-claim-id="first">First<sup><a href="#ref1">1</a></sup></p><p data-claim-id="second">Second<sup><a href="#ref1">1</a></sup></p><div class="references-list"><ol><li id="ref1">Trial doi:10.1/example</li></ol></div>',
            {"sources": [{"citation": 1, "reference_id": "ref1", "doi": "10.1/example", "pmid": "123", "evidence_level": "Human RCT", "claims": ["First", "Second"], "claim_ids": ["first"], "verification_note": "Abstract checked."}]},
        )
        errors = verifier.verify_brief(brief, manifest)
        self.assertTrue(any("claim_ids" in error and "second" in error for error in errors))

    def test_rejects_unlinked_superscript(self):
        verifier = load_module()
        brief, manifest = self.make_files(
            '<p data-claim-id="finding">Claim<sup>1</sup></p><div class="references-list"><ol><li id="ref1">Trial doi:10.1/example</li></ol></div>',
            {"sources": [{"citation": 1, "reference_id": "ref1", "doi": "10.1/example", "pmid": "123", "evidence_level": "Human RCT", "claims": ["Claim"], "claim_ids": ["finding"], "verification_note": "Abstract checked."}]},
        )
        errors = verifier.verify_brief(brief, manifest)
        self.assertTrue(any("linked" in error for error in errors))

    def test_rejects_duplicate_rendered_reference_ids(self):
        verifier = load_module()
        brief, manifest = self.make_files(
            '<p data-claim-id="first">First<sup><a href="#ref1">1</a></sup></p><p data-claim-id="second">Second<sup><a href="#ref2">2</a></sup></p><div class="references-list"><ol><li id="ref1">Trial A doi:10.1/a</li><li id="ref1">Trial B doi:10.1/b</li></ol></div>',
            {"sources": [
                {"citation": 1, "reference_id": "ref1", "doi": "10.1/a", "pmid": "1", "evidence_level": "Human RCT", "claims": ["First"], "claim_ids": ["first"], "verification_note": "Checked."},
                {"citation": 2, "reference_id": "ref2", "doi": "10.1/b", "pmid": "2", "evidence_level": "Human RCT", "claims": ["Second"], "claim_ids": ["second"], "verification_note": "Checked."},
            ]},
        )
        errors = verifier.verify_brief(brief, manifest)
        self.assertTrue(any("duplicate rendered reference id" in error for error in errors))

    def test_rejects_citations_not_numbered_by_first_appearance(self):
        verifier = load_module()
        brief, manifest = self.make_files(
            '<p data-claim-id="second">Second<sup><a href="#ref2">2</a></sup></p><p data-claim-id="first">First<sup><a href="#ref1">1</a></sup></p><div class="references-list"><ol><li id="ref1">Trial A doi:10.1/a</li><li id="ref2">Trial B doi:10.1/b</li></ol></div>',
            {"sources": [
                {"citation": 1, "reference_id": "ref1", "doi": "10.1/a", "pmid": "1", "evidence_level": "Human RCT", "claims": ["First"], "claim_ids": ["first"], "verification_note": "Checked."},
                {"citation": 2, "reference_id": "ref2", "doi": "10.1/b", "pmid": "2", "evidence_level": "Human RCT", "claims": ["Second"], "claim_ids": ["second"], "verification_note": "Checked."},
            ]},
        )
        errors = verifier.verify_brief(brief, manifest)
        self.assertTrue(any("first appearance" in error for error in errors))

    def test_rejects_duplicate_source_identifiers(self):
        verifier = load_module()
        brief, manifest = self.make_files(
            '<p data-claim-id="first">First<sup><a href="#ref1">1</a></sup></p><p data-claim-id="second">Second<sup><a href="#ref2">2</a></sup></p><div class="references-list"><ol><li id="ref1">Trial A doi:10.1/same PMID:1</li><li id="ref2">Trial A duplicate doi:10.1/same PMID:1</li></ol></div>',
            {"sources": [
                {"citation": 1, "reference_id": "ref1", "doi": "10.1/same", "pmid": "1", "evidence_level": "Human RCT", "claims": ["First"], "claim_ids": ["first"], "verification_note": "Checked."},
                {"citation": 2, "reference_id": "ref2", "doi": "10.1/same", "pmid": "1", "evidence_level": "Human RCT", "claims": ["Second"], "claim_ids": ["second"], "verification_note": "Checked."},
            ]},
        )
        errors = verifier.verify_brief(brief, manifest)
        self.assertTrue(any("duplicate source identifier" in error for error in errors))

    def test_rejects_uncatalogued_reference_entry(self):
        verifier = load_module()
        brief, manifest = self.make_files(
            '<p data-claim-id="first">First<sup><a href="#ref1">1</a></sup></p><div class="references-list"><ol><li id="ref1">Trial A doi:10.1/a PMID:1</li><li id="ref2">Uncatalogued trial</li></ol></div>',
            {"sources": [{"citation": 1, "reference_id": "ref1", "doi": "10.1/a", "pmid": "1", "evidence_level": "Human RCT", "claims": ["First"], "claim_ids": ["first"], "verification_note": "Checked."}]},
        )
        errors = verifier.verify_brief(brief, manifest)
        self.assertTrue(any("uncatalogued reference" in error for error in errors))

    def test_rejects_missing_reference_container_and_duplicate_citation(self):
        verifier = load_module()
        brief, manifest = self.make_files('<p data-claim-id="weight">Claim<sup>1</sup></p><ol><li id="ref1">Trial doi:10.1/example</li></ol>', {"sources": [{"citation": 1, "reference_id": "ref1", "doi": "10.1/example", "evidence_level": "Human RCT", "claims": ["Claim"], "claim_ids": ["weight"], "verification_note": "Abstract checked."}, {"citation": 1, "reference_id": "ref1", "doi": "10.1/example", "evidence_level": "Human RCT", "claims": ["Claim"], "claim_ids": ["weight"], "verification_note": "Abstract checked."}]})
        errors = verifier.verify_brief(brief, manifest)
        self.assertTrue(any("references-list" in error for error in errors))
        self.assertTrue(any("duplicate" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
