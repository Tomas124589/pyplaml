import os
import unittest
from glob import glob

from pyplaml import *


# noinspection PyBroadException
class PyPlamlTest(unittest.TestCase):
    def setUp(self):
        self.parser = PUMLParser()
        self.examples_sorted = sorted(glob("../examples/plantuml/*.puml"))

    def test_lexer(self):
        for example_file in self.examples_sorted:
            self.parser.lexer.testFile(str(example_file), False)

    def test_parser(self):
        for example_file in self.examples_sorted:
            try:
                self.assertIsNotNone(self.parser.parse_file(example_file), f"Parser error in {example_file}")
            except:
                self.assertTrue(False, f"Parser exception in {example_file}")

    def test_drawing(self):
        for e in self.examples_sorted:
            self.assertEqual(
                os.system("python ../main.py " + e),
                0,
                f"Drawing \"{e}\" failed"
            )
