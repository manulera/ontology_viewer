from flask import Flask,jsonify,request, current_app
from flask_cors import CORS
import pronto
import requests
import io
app = Flask(__name__)
CORS(app)
app.config['CACHE_TYPE'] = 'null'

@app.before_first_request
def load_ontologies():
     global ONTOLOGIES
     ONTOLOGIES = {
         'FYPO': pronto.Ontology('https://github.com/pombase/fypo/raw/master/fypo-base.obo'),
         'GO': pronto.Ontology('http://current.geneontology.org/ontology/go.obo')
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
        text = f'<strong>{text}</strong>'
    return text

@app.route('/request', methods = ['POST'])
def main_request():
    data = request.get_json()
    string_body = '```mermaid\ngraph TD;\n'
    submitted_ids = data['id'].split(',')

    # We make a set to avoid repetition
    output_lines = set()

    for id in submitted_ids:
        ontology = id.split(':')[0]
        term = ONTOLOGIES[ontology][id]

        if data['requestChildren']:
            children = term.subclasses().to_set()

            for child in children:
                # Parents of this child that are linked to the selected term (that's why it does the intersection with the children)
                parent_subset = child.superclasses(with_self=False, distance=1).to_set() & children
                for parent in parent_subset:
                    output_lines.add(f'      {parent.id}["{term_with_link(parent,submitted_ids)}"]-->{child.id}["{term_with_link(child,submitted_ids)}"];')
        if data['requestParents']:
            parents = term.superclasses().to_set()
            for parent in parents:
                # Children of this parent that are linked to the selected term (that's why it does the intersection)
                child_subset = parent.subclasses(with_self=False, distance=1).to_set() & parents
                for child in child_subset:
                    output_lines.add(f'      {parent.id}["{term_with_link(parent,submitted_ids)}"]-->{child.id}["{term_with_link(child,submitted_ids)}"];')

    string_body+="\n".join(output_lines)
    string_body+='\n```\n'

    return jsonify({
        'mermaid_text': string_body,
    })
