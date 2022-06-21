from flask import Flask,jsonify,request, current_app
from flask_cors import CORS
import pronto

app = Flask(__name__)
CORS(app)
app.config['CACHE_TYPE'] = 'null'

@app.before_first_request
def load_ontologies():
    global ONTOLOGIES
    print('loading FYPO...')
    fypo = pronto.Ontology('https://github.com/pombase/fypo/raw/master/fypo-base.obo')
    print('FYPO loaded')
    print('loading GO...')
    go_ontology = pronto.Ontology('http://current.geneontology.org/ontology/go.obo')
    print('GO loaded')
    ONTOLOGIES = {
        'FYPO': fypo,
        # 'GO': go_ontology
    }

@app.route('/', methods = ['GET'])
def index():
    return current_app.send_static_file('index.html')

def editName(name):
    return '<br>'.join(name[i:i+20] for i in range(0, len(name), 20))

def term_with_link(term: pronto.Term, submitted_ids: list[str]) -> str:
    link_dict = {
        'FYPO': 'https://www.pombase.org/term/',
        'GO' : 'https://www.ebi.ac.uk/QuickGO/term/'
    }
    ontology_name = term.id.split(':')[0]
    text = f'<a href={link_dict[ontology_name]}{term.id}>{term.id}</a><br>{editName(term.name)}'
    if term.id in submitted_ids:
        text = f'<u><strong>{text}</strong></u>'
    return text

def serialize_term(term:pronto.Term) ->dict:
    return hash_dict({
        "id": term.id,
        "name": term.name,
        "definition": term.definition,
        # "equivalent_to": term.equivalent_to
    })

def serialize_relationship(parent: pronto.Term,child: pronto.Term,type: str):
    return hash_dict({
        'parent': parent.id,
        'child': child.id,
        'type': 'is_a'
    })

def hash_dict(unhashed_dict: dict)->frozenset:
    return frozenset(unhashed_dict.items())

def unhash_dict(hashed_dict: frozenset):
    unhashed_dict = dict()
    for key, value in hashed_dict:
        unhashed_dict[key] = value
    return unhashed_dict

@app.route('/request', methods = ['POST'])
def main_request():
    data = request.get_json()
    submitted_ids = data['id'].split(',')

    # We make a set to avoid repetition
    terms = set()
    relationships = set()

    for id in submitted_ids:
        ontology = id.split(':')[0]
        term = ONTOLOGIES[ontology][id]

        if data['requestChildren']:
            children = term.subclasses().to_set()
            for child in children:
                # Parents of this child that are linked to the selected term (that's why it does the intersection with the children)
                parent_subset = child.superclasses(with_self=False, distance=1).to_set() & children
                terms.add(serialize_term(child))
                for parent in parent_subset:
                    terms.add(serialize_term(parent))
                    relationships.add(serialize_relationship(parent,child,'is_a'))

        if data['requestParents']:
            parents = term.superclasses().to_set()
            for parent in parents:
                # Children of this parent that are linked to the selected term (that's why it does the intersection)
                child_subset = parent.subclasses(with_self=False, distance=1).to_set() & parents
                terms.add(serialize_term(parent))
                for child in child_subset:
                    terms.add(serialize_term(child))
                    relationships.add(serialize_relationship(parent,child,'is_a'))

    terms = [unhash_dict(t) for t in terms]
    relationships = [unhash_dict(r) for r in relationships]
    return jsonify({'terms': terms, 'relationships': relationships,})
