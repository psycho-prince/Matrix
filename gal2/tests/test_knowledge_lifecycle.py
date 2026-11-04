import unittest
from dataclasses import replace
from gal2.knowledge_lifecycle import FactKey, KnowledgeStore, run_experiment

class KnowledgeLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.key=FactKey("France","capital","geography")
        self.truth={self.key:"Paris"}
    def test_acquisition_requires_heldout_verification(self):
        s=KnowledgeStore("a0",0); c=s.acquire(self.key,"Paris","e1")
        self.assertFalse(c.verified); self.assertTrue(s.verify(c,self.truth).verified)
    def test_wrong_claim_is_rejected(self):
        s=KnowledgeStore("a0",0); c=s.acquire(self.key,"Lyon","e2")
        s.verify(c,self.truth); self.assertEqual(s.answer(self.key)["status"],"unknown")
    def test_unknown_does_not_guess(self):
        self.assertEqual(KnowledgeStore("a",0).answer(self.key)["status"],"unknown")
    def test_conflicting_verified_claims_block_answer(self):
        s=KnowledgeStore("a",0); a=s.acquire(self.key,"Paris","e1"); b=s.acquire(self.key,"Lyon","e2")
        s.verify(a,self.truth); s.claims[-1]=replace(b,verified=True)
        self.assertEqual(s.answer(self.key)["status"],"conflict")
    def test_inheritance_resets_verification_and_keeps_provenance(self):
        s=KnowledgeStore("parent",0); c=s.acquire(self.key,"Paris","e1"); s.verify(c,self.truth)
        child=s.inherit("child",1,"verified_only"); copied=child.claims[0]
        self.assertFalse(copied.verified); self.assertEqual(copied.source_agent,"parent")
        self.assertIn("parent",copied.lineage); self.assertEqual(copied.evidence_id,"e1")
    def test_verified_only_and_all_memory_differ(self):
        s=KnowledgeStore("p",0); s.acquire(self.key,"Paris","e1")
        self.assertEqual(len(s.inherit("v",1,"verified_only").claims),0)
        self.assertEqual(len(s.inherit("a",1,"all_memory").claims),1)
    def test_reproducibility_and_arms(self):
        a=run_experiment(3,2,3); b=run_experiment(3,2,3)
        self.assertEqual(a["results_sha256"],b["results_sha256"])
        self.assertEqual(set(a["summary"]),{"none","verified_only","all_memory","noisy_transfer"})
        self.assertEqual(len(a["raw_results"]),8)

if __name__=="__main__": unittest.main()
