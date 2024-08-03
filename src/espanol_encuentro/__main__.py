import sys
from argparse import ArgumentParser
from typing import get_args

from espanol_encuentro.constants import words_directory
from espanol_encuentro.entry import PartOfSpeech
from espanol_encuentro.operations import lookup, delete, do_list, add


def main() -> None:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode")

    lookup_parser = subparsers.add_parser("lookup")
    lookup_parser.add_argument("word", help="The Spanish word to lookup")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("word", help="The Spanish word to lookup")
    add_parser.add_argument("--part-of-speech", "-p", choices=get_args(PartOfSpeech), required=True)
    add_parser.add_argument("--short-definition", "-s")
    add_parser.add_argument("--long-definition", "-l", nargs="*")
    add_parser.add_argument("--examples", "-e", nargs="*")
    add_parser.add_argument("--related-words", "-r", nargs="*")

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--starts-with", "-s")
    list_parser.add_argument("--part-of-speech", "-p", choices=get_args(PartOfSpeech), nargs="*")

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("word", help="The Spanish word to delete")

    args = parser.parse_args()

    directory = words_directory()

    if args.mode == "lookup":
        lookup(directory, args.word)
    elif args.mode == "add":
        add(directory=directory, word=args.word,
            part_of_speech=args.part_of_speech, short_definition=args.short_definition or "",
            long_definition=args.long_definition or [],
            examples=args.examples or [], related_words=args.related_words or [])
    elif args.mode == "list":
        do_list(directory, args.starts_with or "", args.part_of_speech or [])
    elif args.mode == "delete":
        lookup(directory, args.word)
        delete(directory, args.word)
    else:
        raise ValueError(f"Invalid mode '{args.mode}'")


if __name__ == "__main__":
    sys.exit(main())
