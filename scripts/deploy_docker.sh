#!/bin/bash
#!/bin/bash
BRANCH=$(git symbolic-ref --short -q HEAD)
COMMIT_ID=$(git rev-parse --short HEAD)

if [[ "$BRANCH" == "master" ]]; then
    TAGNAME="${COMMIT_ID}"
else
    TAGNAME="$BRANCH"
fi

IMAGETAG="josecarlosme/tungsteno:$TAGNAME"

sudo docker build -t $IMAGETAG ./
sudo docker push $IMAGETAG

if [[ "$BRANCH" == "master" ]]; then
    sudo docker tag $IMAGETAG josecarlosme/tungsteno:latest
    sudo docker push josecarlosme/tungsteno:latest
fi
