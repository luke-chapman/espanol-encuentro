# espanol-encuentro

**espanol-encuentro** lets you build a dictionary from one language to another, e.g. from Spanish to English. It's intended as a tool to help you grow your vocabulary in a foreign language.

## Installation
`espanol-encuentro` is currently installed by cloning the source code and doing an editable installation into a virtual environment:
```
git clone https://github.com/luke-chapman/espanol-encuentro
pip install -e espanol-encuentro
```
The app is then invoked from the command line with a command starting:
```
# Commands begin with 'espanol-encuentro'
espanol-encuentro list

# Or they can begin with the shorter 'ee'
ee list
```
## How to use it
### list
List all words, or a filtered subset
```
ee list
ee list --starting-with ll --part-of-speech noun_m noun_f
```

### lookup
Lookup the word 'lluvia' in the dictionary
```
ee lookup lluvia
```

### delete
Delete a word from the dictionary
```
ee delete lluvia
```

### add
Add a word to the dictionary
```
# Full command line options
ee add lluvia --part-of-speech noun_f --definition rain --examples "¿eschucaste la lluvia anoche?" --related-words llover

# Shorthand
ee add lluvia -p noun_f -d rain -e "¿eschucaste la lluvia anoche?" -r llover
```

## Development
This project uses `hatch` to structure the project. Hatch invokes `ruff`, `mypy` and `black` for linting and `pytest` for testing.

Some useful commands are:
```
hatch run lint
hatch run format
hatch run test
```
