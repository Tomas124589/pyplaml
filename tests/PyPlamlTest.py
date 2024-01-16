import unittest

import os
from glob import glob
from pyplaml import *


# noinspection PyBroadException
class PyPlamlTest(unittest.TestCase):
    def test_all_examples_lex(self):
        examples = sorted(glob("../examples/plantuml/*.puml"))
        l = PUMLexer()

        for e in examples:
            l.testFile(e, False)

        self.assertTrue(True)

    def test_all_examples_parse(self):
        examples = sorted(glob("../examples/plantuml/*.puml"))
        l = PUMLParser()

        for e in examples:
            try:
                self.assertIsNotNone(l.parse_file(e), "Parser error in {}".format(e))
            except:
                self.assertTrue(False, "Parser exception in {}".format(e))

    def test_all_examples_draw(self):
        examples = sorted(glob("../examples/plantuml/*.puml"))

        for e in examples:
            self.assertEqual(os.system("python ../main.py " + e), 0, "Drawing \"{}\" failed".format(e))
