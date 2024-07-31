import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import get_args

from espanol_encuentro.entry import PartOfSpeech, default_filename, read_yaml_entries, Entry, write_yaml_entries


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--filename", type=Path, help="Override to the location of the yaml lookup file")

    subparsers = parser.add_subparsers(dest="mode")

    lookup_parser = subparsers.add_parser("lookup")
    lookup_parser.add_argument("word", help="The Spanish word to lookup")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("word", help="The Spanish word to add")
    add_parser.add_argument("--part-of-speech", "-p", choices=get_args(PartOfSpeech))
    add_parser.add_argument("--short-definition", "-s")
    add_parser.add_argument("--long-definition", "-l", nargs="*")
    add_parser.add_argument("--examples", "-e", nargs="*")
    add_parser.add_argument("--related-words", "-r", nargs="*")

    args = parser.parse_args()

    filename = args.filename or default_filename()
    entries = read_yaml_entries(filename) if filename.exists() else []

    if args.mode == "lookup":
        words = [e for e in entries if e.word.lower() == args.word.lower()]
        print(f"Found {len(words)} entries for '{args.word}'")
        for w in words:
            print(f"\n{w}")
    elif args.mode == "add":
        entry = Entry(
            word=args.word,
            part_of_speech=args.part_of_speech or "",
            short_definition=args.short_definition or "",
            long_definition=args.long_definition or [],
            examples=args.examples or [],
            related_words=args.related_words or []
        )
        entries.append(entry)
        entries = sorted(entries, key=lambda e: (e.word, e.part_of_speech, e.short_definition))

        write_yaml_entries(entries=entries, filename=filename)
        print(f"Successfully added word {entry.word} to the lookup file")
    else:
        raise ValueError(f"Invalid mode {args.mode}")


if __name__ == "__main__":
    sys.exit(main())
