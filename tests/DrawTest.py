import unittest

import os
from glob import glob


class DrawTest(unittest.TestCase):
    def test_all_examples_draw(self):
        examples = glob("../examples/*.puml")

        for e in examples:
            self.assertEqual(os.system("python ../main.py " + e), 0)
