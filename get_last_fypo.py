import requests

# Request ontology file from pombase:
response = requests.get("https://github.com/pombase/fypo/raw/master/fypo-base.obo")
with open("fypo-base.obo", "w") as f:
    f.write(response.text)