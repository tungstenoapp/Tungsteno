#!/bin/bash
sudo docker build -t josecarlosme/tungsteno:alpha ./
sudo docker push josecarlosme/tungsteno:alpha

cd docs/
sudo docker build -t josecarlosme/tungsteno-docs:latest ./
sudo docker push josecarlosme/tungsteno-docs:latest
