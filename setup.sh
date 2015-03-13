#!/bin/bash

source globals.sh

# echo "Creating directories"
# mkdir data

echo "Creating virtualenv"
mkvirtualenv $PROJECT_NAME

echo "Installing requirements"
pip install -r requirements.txt

# echo "Downloading data"
# python 

# curl -L -o $FILENAME https://github.com/onyxfish/journalism/raw/master/examples/realdata/ks_1033_data.csv