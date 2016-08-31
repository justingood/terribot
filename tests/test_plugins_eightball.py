"""Testing for eightball.py plugin."""

import re
import unittest

import sys
sys.path.insert(0, '..')

from plugins.eightball import eightball_pattern


class TestEightBall(unittest.TestCase):
    """Testing for eightball.py plugin."""

    def test_pattern_positive(self):
        """Expected matches.

        Confirm that things we want to match the regex indeed match
        """
        positives = {
            '8ball shoud I?': ('8ball', 'shoud I?'),
            '8ball could you? ': ('8ball', 'could you?'),
            '8-ball would it?': ('8-ball', 'would it?'),
            '8 ball shoud we?': ('8 ball', 'shoud we?'),
            '8 ball could you? ': ('8 ball', 'could you?'),
            '8ball would they?': ('8ball', 'would they?'),
        }
        for test in positives:
            with self.subTest(testcase=test):
                m = re.match(eightball_pattern, test)
                self.assertIsNotNone(m)
                self.assertEqual(m.groups(), positives[test])

    def test_pattern_negative(self):
        """Expected non-matches.

        Confirm that things we don't want to match the regex don't
        """
        negatives = [
            ' 8ball shoud I?',
            '8ball could you ',
            '8ball would it',
            '8  ball shoud we?',
            '9ball could you? ',
            'eightball would they?',
        ]
        for test in negatives:
            with self.subTest(testcase=test):
                m = re.match(eightball_pattern, test)
                self.assertIsNone(m)

if __name__ == '__main__':
    unittest.main(verbosity=2)
