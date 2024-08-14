# espanol-encuentro

*espanol-encuentro* lets you build and query a dictionary from Spanish to English. It's intended as a tool to help you grow your vocabulary in a foreign language. A secondary purpose is to demonstrate the Python programming language for beginners.

## Installation
### Beginner user
*For those unfamiliar with 'git' and 'virtual environments', there is a simplified version of this app contained within a single file you can use*

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
usage: example.py [-h] {add,delete,lookup,search} ...

positional arguments:
  {add,delete,lookup,search}

options:
  -h, --help            show this help message and exit
```
6. You are now in a position to run the program! See the section *How to use it*

Notes that writing foolproof instructions for running this program on your computer is hard because of the wide variety of computer specifications and configurations out there. If you get an error you don't understand, ChatGPT may well be able to help

### Advanced user
*For those who know the basics of 'git' and 'virtual environments'*

*espanol-encuentro* is installed by cloning the source code and doing an editable installation into a virtual environment:
```
git clone https://github.com/luke-chapman/espanol-encuentro
pip install -e espanol-encuentro
```
The app is then invoked from the command line with a command starting `espanol-encuentro` or the shorthand `ee`.

## Scope of functionality
*espanol-encuentro* lets you build up a Spanish-English dictionary of Spanish words as you learn them.

You can `add`, `delete` and `modify` entries in the dictionary. You can also `lookup` a single entry, as well as doing a `search` for certain types of words in the dictionary

I limit my use of *espagnol-encuentro* to slowly growing my vocabulary of Spanish nouns, verbs and adjectives. For a more comprehensive dictionary or language learning resource there are many options available online (I use  [SpanishDict](https://www.spanishdict.com/)).

## How to use it
*If you used the basic installation instructions, the below commands should start `python C:\Users\lrrch\Downloads\example.py` rather than `ee`.*

### add
Let's add the word *comida* to the dictionary.
```
ee add comida --part-of-speech noun_f --definition food
```
And another word: *comer*
```
ee add comer --part-of-speech verb --definition "to eat" --examples "Necesito comer (I need to eat)" --related-words comida
```
You must provide a *part of speech* and *definition* for the word. *Examples* and *related words* are optional.

You can add the same word more than once if it has multiple definitions. For example, the Spanish verb `esperar` means both *to wait* and *to hope*, so we can run both of the following commands:
```
ee add esperar --part-of-speech verb --definition "to wait" --examples "Estoy esperando el bus (I'm waiting for the bus)"
ee add esperar --part-of-speech verb --definition "to hope" --examples "Esperamos que llueva mañana (We hope it rains tomorrow)" --related-words esperanza
```

### lookup
Let's lookup the word *comida* in the dictionary. We should see the above definition printed
```
ee lookup comida

{
  "word": "comida",
  "part_of_speech": "noun_f",
  "definition": "food"
}
```
If a word has multiple definitions they will all be shown, e.g.:
```
ee lookup esperar

{
  "word": "esperar",
  "part_of_speech": "verb",
  "definition": "to wait",
  "examples": [
    "Estoy esperando el bus (I'm waiting for the bus)"
  ]
}

{
  "word": "esperar",
  "part_of_speech": "verb",
  "definition": "to hope",
  "examples": [
    "Esperamos que llueva mañana (We hope it rains tomorrow)"
  ],
  "related_words": [
    "esperanza"
  ]
}
```


### search
Search for all words in the dictionary
```
ee search
```
Search for all words in the dictionary beginning with c
```
ee search --starts-with c
```
Search for all nouns in the dictionary (feminine and masculine)
```
ee search --part-of-speech noun_f noun_m
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
