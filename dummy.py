
# %%

import pronto
go = pronto.Ontology('http://current.geneontology.org/ontology/go.obo')

# %%
list(go['GO:0048870'].objects(go.get_relationship('part_of')))
term = go["GO:0031929"]
all_rels = term.relationships.keys()
for rel in all_rels:
    print(rel.name)
    terms: pronto.TermSet = term.relationships[rel]
    for term in terms:
        print(term)
        print(term.id)

# %%
go = pronto.Ontology.from_obo_library("go.obo")
go['GO:0048870']
list(go['GO:0048870'].objects(go.get_relationship('part_of')))
