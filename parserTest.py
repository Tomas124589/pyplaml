import parser as p

with open('inputs/02_relations.puml', 'r') as file:
    input = file.read()

diagram = p.parser.parse(input)
