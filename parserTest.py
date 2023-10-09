import parser as p
from pprint import pprint

fPath = 'inputs/01_elements.puml'
fPath = 'inputs/02_relations.puml'
# fPath = 'inputs/03_relations_extra.puml'
# fPath = 'inputs/04_labels.puml'
# fPath = 'inputs/_test.puml'

with open(fPath, 'r') as file:
    input = file.read()

diagram = p.parser.parse(input)

pprint(diagram.objects)