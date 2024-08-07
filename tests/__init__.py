from espanol_encuentro.constants import default_words_directory


def dictionary_words() -> list[str]:
    directory = default_words_directory()
    return sorted(f.name[:-5] for f in directory.iterdir() if f.suffix == ".yaml")
