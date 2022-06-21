## Running from docker

From any directory in your computer:

```bash
# download the image from dockerhub
docker pull manulera/ontologyviewer
# Start the container
docker run -d --name ontologyviewercontainer -p 5000:5000 manulera/ontologyviewer
```

Now you should be able to use the application at http://localhost:5000/. First time you try to open the URL it may take a bit longer, since it is loading the ontologies.

When you are done, go to the Docker user interface:

* Go to containers:
  * Stop ontologyviewercontainer
  * Delete ontologyviewercontainer
* Go to images
  * Delete manulera/ontologyviewer

## What you can do so far

* You can introduce the term IDs for FYPO, comma separated, then click `Submit`.This will return the tree.
* You can copy the code to paste the tree in a github ticket by clicking on `Copy mermaid code`.
* Tickboxes allow minimal configuration.

## What I did not figure out how to do

* For now it only gets `is_a` relationship (I guess good enough for now in FYPO), but it would be good to access other relationships as well. I can see how to access the other relationships towards the parent, but not towards the children. I have made this ticket asking: https://github.com/althonos/pronto/issues/177
* I don't know where the logical definitions are stored in the FYPO repository. I would have liked to also retrieve multiple logical definitions so it would be easier to compare them than going back and forward on protege. Something to check in the future.

## Running locally

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