import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import get_args

from espanol_encuentro.entry import PartOfSpeech, default_words_directory, Entry, write_yaml_entries, get_entries


def lookup(directory: Path, word: str) -> None:
    entries = get_entries(directory, word)
    for w in entries:
        print(f"\n{w}")


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

    directory = default_words_directory()
    directory.mkdir(parents=True, exist_ok=True)

    if args.mode == "lookup":
        lookup(directory, args.word)
    elif args.mode == "add":
        entries = get_entries(directory, args.word)
        if not args.short_definition and not args.long_definition:
            raise ValueError(f"Must provide either a --short-definition or a --long-definition")
        entry = Entry(
            word=args.word,
            part_of_speech=args.part_of_speech,
            short_definition=args.short_definition or "",
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
    elif args.mode == "list":
        words = sorted(d.name[:-5] for d in directory.iterdir() if d.suffix == ".yaml")
        if args.starts_with:
            words = [w for w in words if w.startswith(args.starts_with)]
        if args.part_of_speech:
            words = [w for w in words if any(e.part_of_speech in args.part_of_speech for e in get_entries(directory, w))]
        print(f"Found {len(words)} matching criteria")
        print("")
        for word in words:
            print(word)
        print("")
    elif args.mode == "delete":
        filename = directory / f"{args.word}.yaml"
        lookup(directory, args.word)
        if filename.is_file():
            filename.unlink()
            print(f"Deleted entry for {args.word} in file {filename}")
        else:
            print(f"No entry for '{args.word}' found")
    else:
        raise ValueError(f"Invalid mode {args.mode}")


if __name__ == "__main__":
    sys.exit(main())
