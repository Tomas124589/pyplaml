import unittest
from pyPlantUML import *


class PyPlantUMLTest(unittest.TestCase):

    def test_input_elements(self):
        p = PUMLParser()
        d = p.parseFile("../examples/01_elements.puml")

        self.assertIsNotNone(d)

    def test_class_tree(self):
        p = PUMLParser()
        d = p.parseFile("../examples/02_class_tree.puml")

        self.assertIsNotNone(d)

    def test_relations(self):
        p = PUMLParser()
        d = p.parseFile("../examples/03_relations.puml")

        self.assertIsNotNone(d)

    def test_relations_extra(self):
        p = PUMLParser()
        d = p.parseFile("../examples/04_relations_extra.puml")

        self.assertIsNotNone(d)

    def test_class_attributes(self):
        p = PUMLParser()
        d = p.parseFile("../examples/05_class_attributes.puml")

        self.assertIsNotNone(d)

    def test_class_tree_with_attributes(self):
        p = PUMLParser()
        d = p.parseFile("../examples/06_class_tree_with_attributes.puml")

        self.assertIsNotNone(d)
