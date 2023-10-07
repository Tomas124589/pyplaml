import parser as p

with open('inputs/01_basic.puml', 'r') as file:
    input = file.read()

diagram = p.parser.parse(input)