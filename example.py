# Section 1 - imports
# Let's re-use some pre-existing tools to make life easier for ourselves
#
# For example, we're going to use the 'json' Python library to interact with data in the json format
# json is a beautiful, simple and ubiquitous data format - if you're interested, see https://www.json.org/json-en.html

import json
import sys
from argparse import ArgumentParser
from pathlib import Path


# Section 2 - argument parsing
# Our program will be invoked by command lines such as:
#
# python example.py add comida --part-of-speech noun_f --definition food
#
# We need to tell the program what the arguments in these command lines mean
# 'ArgumentParser' also emits useful help messages or error messages to help the user
#
def run():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("word", help="The Spanish word to lookup")
    add_parser.add_argument("--part-of-speech", "-p", required=True)
    add_parser.add_argument("--definition", "-d", required=True)
    add_parser.add_argument("--examples", "-e", nargs="*")
    add_parser.add_argument("--related-words", "-r", nargs="*")
    add_parser.add_argument("--words-dir", type=Path, help="Directory containing json files for each word")

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("word", help="The Spanish word to delete")
    delete_parser.add_argument("--words-dir", type=Path, help="Directory containing json files for each word")

    lookup_parser = subparsers.add_parser("lookup")
    lookup_parser.add_argument("word", help="The Spanish word to lookup")
    lookup_parser.add_argument("--words-dir", type=Path, help="Directory containing json files for each word")

    list_parser = subparsers.add_parser("search")
    list_parser.add_argument("--starts-with", "-d")
    list_parser.add_argument("--words-dir", type=Path, help="Directory containing json files for each word")

    args = parser.parse_args(sys.argv[1:] or ["--help"])

    # Section 3 - a little bit of a setup
    #
    # espanol-encuentro stores the words in a folder on your computer
    # Let's decide what that folder is and create it if it doesn't exist
    #
    words_dir = args.words_dir or Path.home() / ".espanol-encuentro" / "words"
    words_dir.mkdir(parents=True, exist_ok=True)

    # Section 4: if-else statements
    #
    # What operation are we doing? Either 'add', 'lookup', 'search' or 'delete'
    #
    if args.mode == "add":
        # Section 4a - 'add' operation
        #
        # We create a 'dictionary' object called 'entry' and write it to a json file
        #
        entry = {
            "word": args.word,
            "part_of_speech": args.part_of_speech,
            "definition": args.definition,
        }
        if args.examples:
            entry["examples"] = args.examples
        if args.related_words:
            entry["related_words"] = args.related_words

        word_json = words_dir / f"{args.word}.json"
        with word_json.open("w", encoding="utf-16") as w:
            json.dump(entry, w, indent=2, ensure_ascii=False)
        print(f"Wrote entry for '{args.word}' to {word_json}")

    elif args.mode == "lookup":
        # Section 4b - 'lookup' operation
        #
        # Look for the json file and print its contents if it exists
        #
        word_json = words_dir / f"{args.word}.json"
        if word_json.is_file():
            print(word_json.read_text(encoding="utf-16"))
        else:
            print(f"No entry found for '{args.word}'")

    elif args.mode == "search":
        # Section 4c - 'search' operation
        #
        # Start by listing all the files in the words directory
        # If we specified --starts-with, filter this list accordingly
        #
        words = sorted(d.name[:-5] for d in words_dir.iterdir() if d.suffix == ".json")
        if args.starts_with:
            words = [w for w in words if w.startswith(args.starts_with)]
        print(f"Found {len(words)} words matching criteria")
        print("")
        for word in words:
            print(word)
        print("")

    elif args.mode == "delete":
        # Section 4d - 'delete' operation
        #
        # If there's a file for the word in question, delete it
        #
        word_json = words_dir / f"{args.word}.json"
        if word_json.is_file():
            word_json.unlink()
            print(f"Deleted entry for '{args.word}'")
        else:
            print(f"No entry found for '{args.word}'")

    else:
        # Section 5 - error handling
        #
        # What if the mode isn't add, lookup, search or delete?
        # Let's report this error back to the user (comedy link: https://www.youtube.com/watch?v=x0YGZPycMEU)
        #
        raise ValueError(f"Unexpected mode '{args.mode}'")


# Section 6 - a tiny bit of magic to start and stop the program
#
if __name__ == "__main__":
    sys.exit(run())
