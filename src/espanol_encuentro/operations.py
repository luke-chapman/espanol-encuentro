from pathlib import Path

from espanol_encuentro.entry import Entry, PartOfSpeech, get_entries, write_json_entries


def lookup(directory: Path, word: str) -> None:
    entries = get_entries(directory, word)
    for w in entries:
        print(f"\n{w}")


def add(
    directory: Path,
    word: str,
    part_of_speech: PartOfSpeech,
    definition: str,
    examples: list[str],
    related_words: list[str],
) -> None:
    entries = get_entries(directory, word)
    entry = Entry(
        word=word,
        part_of_speech=part_of_speech,
        definition=definition or "",
        examples=examples or [],
        related_words=related_words or [],
    )
    if len(entries) > 0:
        print(f"{len(entries)} entries already exist for '{word}'; appending new entry")
    entries.append(entry)
    entries = [e.format() for e in entries]
    write_json_entries(entries=entries, filename=directory / f"{word}.json")
    print(f"Successfully added an entry for '{entry.word}' to the lookup file")


def search(directory: Path, starts_with: str, part_of_speech: list[str]) -> None:
    words = sorted(d.name[:-5] for d in directory.iterdir() if d.suffix == ".json")
    if starts_with:
        words = [w for w in words if w.startswith(starts_with)]
    if part_of_speech:
        words = [w for w in words if any(e.part_of_speech in part_of_speech for e in get_entries(directory, w))]
    print(f"Found {len(words)} words matching criteria")
    print("")
    for word in words:
        print(word)
    print("")


def delete(directory: Path, word: str) -> None:
    filename = directory / f"{word}.json"
    if filename.is_file():
        filename.unlink()
        print(f"Deleted entry for '{word}' in file {filename}")
    else:
        print(f"No entry for '{word}' found")


def modify(
    directory: Path,
    word: str,
    index: int,
    part_of_speech: PartOfSpeech | None,
    definition: str,
    examples: list[str],
    related_words: list[str],
) -> None:
    entries = get_entries(directory, word)
    if len(entries) == 0:
        print(f"No entries found for word '{word}'; nothing to modify")
        return
    if index < 0 or index >= len(entries):
        print(f"Cannot modify entry with index {index} for word '{word}' with {len(entries)} entries")
        return

    entry = entries[index]
    if part_of_speech:
        entry = entry.model_copy(update={"part_of_speech": part_of_speech})
    if definition:
        entry = entry.model_copy(update={"definition": definition})

    entry.examples.extend(examples)
    entry.related_words.extend(related_words)

    entries[index] = entry.format()

    write_json_entries(entries, directory / f"{word}.json")
