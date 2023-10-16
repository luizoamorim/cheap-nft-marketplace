#!/bin/bash

# Format the code using black
#autopep8 . --recursive --in-place --aggressive --aggressive

# Run pylint for linting
pylint marketplace/

# Run the Django tests
python3 manage.py test marketplace
