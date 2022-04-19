import pronto
import json
import urllib.request

fypo = pronto.Ontology('./fypo-base.obo')

starting_point  = fypo['FYPO:0000054'].subclasses().to_set()
data = []

string_body = ''

for term in starting_point:
    parents = term.superclasses(with_self=False, distance=1).to_set() & starting_point
    for parent in parents:
        string_body+=f'      {parent.id}-->{term.id};\n'

with open('graph.md','w') as out:
    out.write('```mermaid\ngraph TD;\n')
    out.write(string_body)
    out.write('```\n')



