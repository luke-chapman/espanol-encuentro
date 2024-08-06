import sys
from argparse import ArgumentParser
from pathlib import Path

import yaml


def run():
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest="mode")

    lookup_parser = subparsers.add_parser("lookup")
    lookup_parser.add_argument("word", help="The Spanish word to lookup")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("word", help="The Spanish word to lookup")
    add_parser.add_argument("--part-of-speech", "-p", required=True)
    add_parser.add_argument("--short-definition", "-s", required=True)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--starts-with", "-s")

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("word", help="The Spanish word to delete")

    parser.add_argument("--words-dir", type=Path, help="Directory containing yaml files for each word")
    args = parser.parse_args()

    words_dir = args.words_dir or Path(__file__).resolve().parent / "words"
    words_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "lookup":
        word_yaml = words_dir / f"{args.word}.yaml"
        if word_yaml.is_file():
            print(word_yaml.read_text())
        else:
            print(f"No entry found for '{args.word}'")
    elif args.mode == "add":
        entry = {
            "word": args.word,
            "part_of_speech": args.part_of_speech,
            "short_definition": args.short_definition,
        }
        word_yaml = words_dir / f"{args.word}.yaml"
        with word_yaml.open("w") as w:
            yaml.safe_dump(entry, w, sort_keys=False, allow_unicode=True)
        print(f"Wrote entry for '{args.word}' to {word_yaml}")
    elif args.mode == "list":
        words = sorted(d.name[:-5] for d in words_dir.iterdir() if d.suffix == ".yaml")
        if args.starts_with:
            words = [w for w in words if w.startswith(args.starts_with)]
        print(f"Found {len(words)} words matching criteria")
        print("")
        for word in words:
            print(word)
        print("")
    elif args.mode == "delete":
        word_yaml = words_dir / f"{args.word}.yaml"
        if word_yaml.is_file():
            word_yaml.unlink()
            print(f"Deleted entry for '{args.word}'")
        else:
            print(f"No entry found for '{args.word}'")
    else:
        raise ValueError(f"Unexpected mode '{args.mode}'")


if __name__ == "__main__":
    sys.exit(run())
