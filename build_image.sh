#!/bin/bash

COMMIT=$(git log -n1 --pretty='%h')
REPO="trstringer/vm-manage"

source venv/bin/activate

pip freeze | grep -v "pkg-resources" > requirements.txt

docker build -t "$REPO:$COMMIT" -t "$REPO:latest" .
docker push "$REPO:$COMMIT"
docker push "$REPO:latest"
