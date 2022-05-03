from flask import Flask,jsonify,request, current_app
from flask_cors import CORS
import pronto
import requests
import io
app = Flask(__name__)
CORS(app)
app.config["CACHE_TYPE"] = "null"

@app.route('/', methods = ['GET'])
def index():
    return current_app.send_static_file('index.html')


@app.route('/request', methods = ['POST'])
def main_request():
    data = request.get_json()

    fypo = pronto.Ontology("http://current.geneontology.org/ontology/go.obo")

    children = fypo[data['id']].subclasses().to_set()

    string_body = '```mermaid\ngraph LR;\n'

    def editName(name):
        return "<br>".join(name[i:i+20] for i in range(0, len(name), 20))

    for child in children:
        # Parents of this child that are linked to the selected term (that's why it does the intersection with the children)
        parent_subset = child.superclasses(with_self=False, distance=1).to_set() & children
        for parent in parent_subset:
            string_body+=f'      {parent.id}[{parent.id}<br>{editName(parent.name)}]-->{child.id}[{child.id}<br>{editName(child.name)}];\n'

    parents = fypo[data['id']].superclasses().to_set()
    for parent in parents:
        # Children of this parent that are linked to the selected term (that's why it does the intersection)
        child_subset = parent.subclasses(with_self=False, distance=1).to_set() & parents
        for child in child_subset:
            string_body+=f'      {parent.id}[{parent.id}<br>{editName(parent.name)}]-->{child.id}[{child.id}<br>{editName(child.name)}];\n'

    string_body+='```\n'

    return jsonify({
        "mermaid_text": string_body,
    })
