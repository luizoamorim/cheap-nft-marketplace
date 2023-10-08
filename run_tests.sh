#!/bin/bash

# Format the code using black
black nftmktplace/

# Run pylint for linting
pylint marketplace/

# Run the Django tests
python3 manage.py test marketplace
