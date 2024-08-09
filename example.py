import json
import sys
from argparse import ArgumentParser
from pathlib import Path


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

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--starts-with", "-d")
    list_parser.add_argument("--words-dir", type=Path, help="Directory containing json files for each word")

    lookup_parser = subparsers.add_parser("lookup")
    lookup_parser.add_argument("word", help="The Spanish word to lookup")
    lookup_parser.add_argument("--words-dir", type=Path, help="Directory containing json files for each word")

    args = parser.parse_args(sys.argv[1:] or ["--help"])

    words_dir = args.words_dir or Path.home() / ".espanol-encuentro" / "words"
    words_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "lookup":
        word_json = words_dir / f"{args.word}.json"
        if word_json.is_file():
            print(word_json.read_text(encoding="utf-16"))
        else:
            print(f"No entry found for '{args.word}'")
    elif args.mode == "add":
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
    elif args.mode == "list":
        words = sorted(d.name[:-5] for d in words_dir.iterdir() if d.suffix == ".json")
        if args.starts_with:
            words = [w for w in words if w.startswith(args.starts_with)]
        print(f"Found {len(words)} words matching criteria")
        print("")
        for word in words:
            print(word)
        print("")
    elif args.mode == "delete":
        word_json = words_dir / f"{args.word}.json"
        if word_json.is_file():
            word_json.unlink()
            print(f"Deleted entry for '{args.word}'")
        else:
            print(f"No entry found for '{args.word}'")
    else:
        raise ValueError(f"Unexpected mode '{args.mode}'")


if __name__ == "__main__":
    sys.exit(run())
