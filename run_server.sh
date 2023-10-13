#!/bin/bash

# Format the code using black
autopep8 nftmktplace/

# Run pylint for linting
pylint marketplace/

# Run the Django tests
python3 manage.py test marketplace

# Run 
python3 manage.py runserver 8080

