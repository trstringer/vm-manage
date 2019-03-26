#!/bin/bash

COMMIT=$(git log -n1 --pretty='%h')
REPO="trstringer/vm-manage"

docker push "$REPO:$COMMIT"
docker push "$REPO:latest"
