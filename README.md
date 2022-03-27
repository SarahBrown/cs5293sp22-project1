# cs5293sp22-project1

### Author: Sarah Brown

# Directions to Install and Use Package
To download and use package, follow the steps below:

1. git clone https://github.com/SarahBrown/cs5293sp22-project1.git
2. cd cs5293sp22-project1/
3. pipenv install
4. pipenv run python -m spacy download en_core_web_sm

5. 
pipenv run python redactor.py --input 'resources/*.txt' \
                    --names --dates --phones --genders --address\
                    --concept 'kids' \
                    --output 'files/' \
                    --stats stderr

# Web or External Libraries


# Approach to Development

## Readaction Flags

### Readaction of Whitespace

## Concepts
Concepts are a selected, singular word to represent an idea to be redacted. 

## Stats 

## Functions


# Assumptions Made and Known Bugs


# Tests

