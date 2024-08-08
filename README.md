# espanol-encuentro

**espanol-encuentro** lets you build a dictionary from one language to another, e.g. from Spanish to English. It's intended as a tool to help you grow your vocabulary in a foreign language.

## Installation
### Beginner
1. Install **Python** on your computer: https://www.python.org/downloads/
2. Download this file **example.py** onto your computer: https://github.com/luke-chapman/espanol-encuentro/blob/master/example.py
3. Open up a **Command Prompt** on your computer
4. Type the following into your terminal, changing it depending on where the **example.py** file is:
```
 python C:\Users\lrrch\Downloads\example.py
```
5. If all has gone well you should see the following:
```
python C:\Users\lrrch\OneDrive\Documents\Code\ReposA\espanol-encuentro\example.py
usage: example.py [-h] {add,delete,list,lookup} ...

positional arguments:
  {add,delete,list,lookup}

options:
  -h, --help            show this help message and exit
```

Note that writing foolproof instructions for running this program on your computer is hard because of the wide variety of computer specifications and configurations out there. If you get an error you don't understand, I recommend asking ChatGPT!

### Advanced
`espanol-encuentro` is installed by cloning the source code and doing an editable installation into a virtual environment:
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
hatch run format
hatch run lint
hatch run test
```

The latter two of these commands are run as part of the [GitHubActions continuous integration](https://github.com/luke-chapman/espanol-encuentro/actions/workflows/python-package.yaml); code should pass these checks before hitting master.
