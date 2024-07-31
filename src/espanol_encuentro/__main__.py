import sys
from argparse import ArgumentParser
from typing import get_args

from espanol_encuentro.entry import PartOfSpeech, default_words_directory, Entry, write_yaml_entries, get_entries


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("word", help="The Spanish word to lookup")

    subparsers = parser.add_subparsers(dest="mode")
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--part-of-speech", "-p", choices=get_args(PartOfSpeech), required=True)
    add_parser.add_argument("--short-definition", "-s", required=True)
    add_parser.add_argument("--long-definition", "-l", nargs="*")
    add_parser.add_argument("--examples", "-e", nargs="*")
    add_parser.add_argument("--related-words", "-r", nargs="*")

    args = parser.parse_args()

    directory = default_words_directory()
    directory.mkdir(parents=True, exist_ok=True)
    entries = get_entries(directory, args.word)

    if not args.mode:
        for w in entries:
            print(f"\n{w}")
    elif args.mode == "add":
        entry = Entry(
            word=args.word,
            part_of_speech=args.part_of_speech,
            short_definition=args.short_definition,
            long_definition=args.long_definition or [],
            examples=args.examples or [],
            related_words=args.related_words or [],
        )
        if len(entries) > 0:
            print(f"{len(entries)} entries already exist for '{args.word}'; appending new entry")
        entries.append(entry)
        entries = sorted(e.format() for e in entries)
        write_yaml_entries(entries=entries, filename=directory / f"{args.word}.yaml")
        print(f"Successfully added an entry for '{entry.word}' to the lookup file")
    else:
        raise ValueError(f"Invalid mode {args.mode}")


if __name__ == "__main__":
    sys.exit(main())
