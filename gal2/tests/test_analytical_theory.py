import unittest
from fractions import Fraction as F
from gal2.analytical_theory import bayes_update, inherit_distribution, posterior_odds, bayes_factor_for_confidence, total_variation, bounded_loss_shift_bound, verification_threshold

class AnalyticalTheoryTests(unittest.TestCase):
    def test_bayes_update_exact(self):
        self.assertEqual(bayes_update({"H1":F(1,2),"H0":F(1,2)},{"H1":F(3,4),"H0":F(1,4)}),{"H1":F(3,4),"H0":F(1,4)})
    def test_bayes_support_mismatch_rejected(self):
        with self.assertRaises(ValueError): bayes_update({"H1":F(1)},{"H0":F(1)})
    def test_inheritance_endpoints_and_convexity(self):
        b={"a":F(3,4),"b":F(1,4)}; p={"a":F(1,4),"b":F(3,4)}
        self.assertEqual(inherit_distribution(p,b,F(0)),b)
        self.assertEqual(inherit_distribution(p,b,F(1)),p)
        self.assertEqual(inherit_distribution(p,b,F(1,2)),{"a":F(1,2),"b":F(1,2)})
    def test_bayes_factor_threshold(self):
        bf=bayes_factor_for_confidence(F(1,10),F(9,10))
        self.assertEqual(bf,F(81)); self.assertEqual(posterior_odds(F(1,10),bf),F(9))
        self.assertEqual(verification_threshold(F(1,10),F(9,10)),F(81))
    def test_total_variation(self):
        self.assertEqual(total_variation({"a":F(3,4),"b":F(1,4)},{"a":F(1,4),"b":F(3,4)}),F(1,2))
    def test_shift_bound(self):
        self.assertEqual(bounded_loss_shift_bound(F(2,5),F(1,10)),F(1,5))
        self.assertLessEqual(bounded_loss_shift_bound(F(1,5),F(1,10)),F(0))
    def test_invalid_retention(self):
        with self.assertRaises(ValueError): inherit_distribution({"a":F(1)},{"a":F(1)},F(2))

if __name__=="__main__": unittest.main()
