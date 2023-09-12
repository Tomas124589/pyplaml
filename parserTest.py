import parser as p

with open('inputs/simple.puml', 'r') as file:
    input = file.read()

diagram = p.parser.parse(input)

diagram.draw()