import parser as p

with open('inputs/simple.puml', 'r') as file:
    input = file.read()

res = p.parser.parse(input)

for node in res.nodes:
    print(node)