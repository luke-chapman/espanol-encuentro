# espanol-encuentro

*espanol-encuentro* lets you build and query a dictionary from one language to another, e.g. from Spanish to English. It's intended as a tool to help you grow your vocabulary in a foreign language. A secondary purpose of *espanol-encuentro* is as a demonstration of the Python programming language for beginners.

## Installation
### Beginner user
*For those unfamiliar with 'git' and 'virtual environments'*

1. Install *Python* on your computer: https://www.python.org/downloads/
2. Download this file *example.py* onto your computer: https://github.com/luke-chapman/espanol-encuentro/blob/master/example.py
3. Open up a *Command Prompt* on your computer
4. Type the following into your terminal, changing it depending on where the *example.py* file is:
```
 python C:\Users\lrrch\Downloads\example.py
```
5. If all has gone well you should see the following help message from the program:
```
python C:\Users\lrrch\Downloads\example.py
usage: example.py [-h] {add,delete,list,lookup} ...

positional arguments:
  {add,delete,list,lookup}

options:
  -h, --help            show this help message and exit
```
6. You are now in a position to run the program! See the section *How to use it*

Notes:
- Writing foolproof instructions for running this program on your computer is hard because of the wide variety of computer specifications and configurations out there
- If you get an error you don't understand, ChatGPT may well be able to help
- In general, I recommend a great degree of patience if you want to get into programming...

### Advanced user
*For those who know the basics of 'git' and 'virtual environments'*

*espanol-encuentro* is installed by cloning the source code and doing an editable installation into a virtual environment:
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
## Scope of functionality
*espanol-encuentro* allows you to build your own Spanish-English dictionary with new words as you learn them. You can then come back and look them up or revise words you've recently encountered for the first time.

*espanol-encuentro* is not intended to be a complete dictionary or language learning resource in any way. If you want to learn Spanish grammar and roll your Spanish `r`s like a native, there are numerous other resources that can help with this.

I limit my use of *espagnol-encuentro* to slowly growing my vocabulary of Spanish nouns, verbs and adjectives.

## How to use it
If you used the basic installation instructions, the below commands should start `python C:\Users\lrrch\Downloads\example.py` rather than `ee`.

### add
Let's add the word *comida* to the dictionary.
```
ee add comida --part-of-speech noun_f --definition food --examples "Me gusta la comida (I like the food)"
```
And another word: *comer*
```
ee add comer --part-of-speech verb --defininition "to eat" --examples "Necesito comer (I need to eat)" --related-words comida
```
You must provide a *part of speech* and *definition* for the word. *Examples* and *related words* are optional.

### lookup
Lookup the word *comida* in the dictionary. You should see the above definition printed
```
ee lookup comida
```
gives
```
{
  "word": "comida",
  "part_of_speech": "noun_f",
  "definition": "food",
  "examples": [
    "Me gusta la comida (I like the food)"
  ]
}
```

### list
List all words
```
ee list
```
List all words in the dictionary beginning with c
```
ee list --starts-with c
```
List all nouns in the dictionary (feminine and masculine)
```
ee list --part-of-speech noun_f noun_m
```

### delete
Delete a word from the dictionary
```
ee delete comida
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

For local development I've also added a `hatch run yeehaw -- {commit message}` mode. This runs a series of pre-commit hooks similar to those which run as part of CI. If all of these pass it commits and pushes to git.
