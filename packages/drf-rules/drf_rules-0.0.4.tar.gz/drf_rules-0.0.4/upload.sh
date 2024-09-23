#!/bin/bash -e

rm -rf dist/
source ../envPer/bin/activate
python -m build
twine upload dist/*
