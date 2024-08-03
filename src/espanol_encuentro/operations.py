from pathlib import Path

from espanol_encuentro.entry import Entry, PartOfSpeech, get_entries, write_yaml_entries


def lookup(directory: Path, word: str) -> None:
    entries = get_entries(directory, word)
    for w in entries:
        print(f"\n{w}")


def add(
    directory: Path,
    word: str,
    part_of_speech: PartOfSpeech,
    short_definition: str,
    long_definition: list[str],
    examples: list[str],
    related_words: list[str],
) -> None:
    entries = get_entries(directory, word)
    if not short_definition and not long_definition:
        raise ValueError("Must provide either a --short-definition or a --long-definition")
    entry = Entry(
        word=word,
        part_of_speech=part_of_speech,
        short_definition=short_definition or "",
        long_definition=long_definition or [],
        examples=examples or [],
        related_words=related_words or [],
    )
    if len(entries) > 0:
        print(f"{len(entries)} entries already exist for '{word}'; appending new entry")
    entries.append(entry)
    entries = sorted(e.format() for e in entries)
    write_yaml_entries(entries=entries, filename=directory / f"{word}.yaml")
    print(f"Successfully added an entry for '{entry.word}' to the lookup file")


def do_list(directory: Path, starts_with: str, part_of_speech: list[str]) -> None:
    words = sorted(d.name[:-5] for d in directory.iterdir() if d.suffix == ".yaml")
    if starts_with:
        words = [w for w in words if w.startswith(starts_with)]
    if part_of_speech:
        words = [w for w in words if any(e.part_of_speech in part_of_speech for e in get_entries(directory, w))]
    print(f"Found {len(words)} matching criteria")
    print("")
    for word in words:
        print(word)
    print("")


def delete(directory: Path, word: str) -> None:
    filename = directory / f"{word}.yaml"
    if filename.is_file():
        filename.unlink()
        print(f"Deleted entry for '{word}' in file {filename}")
    else:
        print(f"No entry for '{word}' found")
