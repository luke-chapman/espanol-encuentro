import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import get_args

from espanol_encuentro.constants import default_words_directory
from espanol_encuentro.entry import PartOfSpeech
from espanol_encuentro.operations import add, delete, do_list, lookup, modify, sanitise


def main() -> int:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode")
    parser.add_argument("--words-dir", type=Path, help="Directory containing yaml files for each word")

    lookup_parser = subparsers.add_parser("lookup")
    lookup_parser.add_argument("word", help="The Spanish word to lookup")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("word", help="The Spanish word to lookup")
    add_parser.add_argument("--part-of-speech", "-p", choices=get_args(PartOfSpeech), required=True)
    add_parser.add_argument("--short-definition", "-s", required=True)
    add_parser.add_argument("--long-definition", "-l", nargs="*")
    add_parser.add_argument("--examples", "-e", nargs="*")
    add_parser.add_argument("--related-words", "-r", nargs="*")

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--starts-with", "-s")
    list_parser.add_argument("--part-of-speech", "-p", choices=get_args(PartOfSpeech), nargs="*")

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("word", help="The Spanish word to delete")

    modify_parser = subparsers.add_parser("modify")
    modify_parser.add_argument("word", help="The Spanish word to delete")
    modify_parser.add_argument(
        "--index",
        "-i",
        default=0,
        help="The index of the entry to modify, from within the list of entries for the word",
    )
    modify_parser.add_argument("--part-of-speech", "-p", choices=get_args(PartOfSpeech))
    modify_parser.add_argument("--short-definition", "-s")
    modify_parser.add_argument("--long-definition", "-l", nargs="*")
    modify_parser.add_argument("--examples", "-e", nargs="*")
    modify_parser.add_argument("--related-words", "-r", nargs="*")

    _ = subparsers.add_parser("sanitise")

    args = parser.parse_args()

    directory = args.words_dir or default_words_directory()

    if args.mode == "lookup":
        lookup(directory, args.word)
    elif args.mode == "add":
        add(
            directory=directory,
            word=args.word,
            part_of_speech=args.part_of_speech,
            short_definition=args.short_definition or "",
            long_definition=args.long_definition or [],
            examples=args.examples or [],
            related_words=args.related_words or [],
        )
    elif args.mode == "list":
        do_list(directory, args.starts_with or "", args.part_of_speech or [])
    elif args.mode == "delete":
        lookup(directory, args.word)
        delete(directory, args.word)
    elif args.mode == "modify":
        modify(
            directory=directory,
            word=args.word,
            index=args.index,
            part_of_speech=args.part_of_speech,
            short_definition=args.short_definition or "",
            long_definition=args.long_definition or [],
            examples=args.examples or [],
            related_words=args.related_words or [],
        )
    elif args.mode == "sanitise":
        sanitise(directory)
    else:
        raise ValueError(f"Invalid mode '{args.mode}'")

    return 0


if __name__ == "__main__":
    sys.exit(main())
