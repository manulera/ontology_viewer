from flask import Flask,jsonify,Response,request,send_file
from flask_cors import CORS
import os
import pronto
import json
import urllib.request

app = Flask(__name__)
CORS(app)
app.config["CACHE_TYPE"] = "null"

@app.route('/', methods = ['POST','GET'])
def main():
    data = request.get_json()

    fypo = pronto.Ontology('./fypo-base.obo')

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





fypo = pronto.Ontology('./fypo-base.obo')

starting_point  = fypo['FYPO:0007111'].subclasses().to_set()
data = []

string_body = '```mermaid\ngraph LR;\n'

def editName(name):
    return "<br>".join(name[i:i+20] for i in range(0, len(name), 20))

for term in starting_point:
    parents = term.superclasses(with_self=False, distance=1).to_set() & starting_point
    for parent in parents:
        string_body+=f'      {parent.id}[{parent.id}<br>{editName(parent.name)}]-->{term.id}[{term.id}<br>{editName(term.name)}];\n'

# for term in starting_point:
#     string_body+=f'      {term.id} : {term.name};\n'

string_body+='```\n'