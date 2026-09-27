import unittest
from src.feedback_state import update_state, trajectory

class FeedbackStateTests(unittest.TestCase):
    def test_core_update(self):
        self.assertAlmostEqual(update_state(1,0.2,3).after,1.6)

    def test_hold_regime(self):
        s=update_state(2,0.01,100,epsilon=0.02)
        self.assertTrue(s.held);self.assertEqual(s.applied_update,0);self.assertEqual(s.after,2)

    def test_bounded_update(self):
        s=update_state(0,10,2,max_update=0.5)
        self.assertEqual(s.raw_update,20);self.assertEqual(s.applied_update,0.5)

    def test_memory_is_explicit_separate_term(self):
        s=update_state(1,0,1,memory_input=4,memory_gain=0.25)
        self.assertEqual(s.after,2)

    def test_trajectory_equals_cumulative_updates(self):
        self.assertEqual(trajectory(0,[1,-0.5],[2,2]),[0,2.0,1.0])

    def test_bad_parameters_fail(self):
        with self.assertRaises(ValueError):update_state(0,1,1,epsilon=-1)
        with self.assertRaises(ValueError):trajectory(0,[1],[1,2])

if __name__=="__main__":unittest.main()
