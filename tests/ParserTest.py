import unittest
from pyPlantUML import *


class pyPlantUMLTest(unittest.TestCase):

    def test_input_elements(self):
        p = PUMLParser()
        d = p.parseFile("inputs/01_elements.puml")

        self.assertIsNotNone(d)

    def test_class_tree(self):
        p = PUMLParser()
        d = p.parseFile("inputs/02_class_tree.puml")

        self.assertIsNotNone(d)

    def test_relations(self):
        p = PUMLParser()
        d = p.parseFile("inputs/03_relations.puml")

        self.assertIsNotNone(d)

    def test_relations_extra(self):
        p = PUMLParser()
        d = p.parseFile("inputs/04_relations_extra.puml")

        self.assertIsNotNone(d)

    def test_class_attributes(self):
        p = PUMLParser()
        d = p.parseFile("inputs/05_class_attributes.puml")

        self.assertIsNotNone(d)
