To run

```
export FLASK_ENV=development
poetry run flask run
```

To build the image:

```bash
docker build -t manulera/ontologyviewer .

# For dockerhub:
docker push manulera/ontologyviewer
# For building
docker run -d --name ontologyviewercontainer -p 5000:5000 manulera/ontologyviewer
```