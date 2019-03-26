#!/bin/bash

COMMIT=$(git log -n1 --pretty='%h')
REPO="trstringer/vm-manage"

docker run -p 8000:8000 --rm --name vm-manage -it "$REPO:$COMMIT"
