from flask import Flask,jsonify,request
from flask_cors import CORS
import pronto
import requests
import io
app = Flask(__name__)
CORS(app)
app.config["CACHE_TYPE"] = "null"

@app.route('/', methods = ['POST','GET'])
def main():
    data = request.get_json()

    fypo = pronto.Ontology("https://github.com/geneontology/go-ontology/raw/master/src/ontology/go-edit.obo")

    starting_point = fypo[data['id']].subclasses().to_set()

    string_body = '```mermaid\ngraph LR;\n'

    def editName(name):
        return "<br>".join(name[i:i+20] for i in range(0, len(name), 20))

    for term in starting_point:
        print(term)
        parents = term.superclasses(with_self=False, distance=1).to_set() & starting_point
        for parent in parents:
            string_body+=f'      {parent.id}[{parent.id}<br>{editName(parent.name)}]-->{term.id}[{term.id}<br>{editName(term.name)}];\n'


    string_body+='```\n'

    return jsonify({
        "mermaid_text": string_body,
    })
