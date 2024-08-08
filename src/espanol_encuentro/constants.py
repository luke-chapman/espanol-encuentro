from pathlib import Path


def default_words_directory() -> Path:
    directory = Path(__file__).resolve().parent.parent.parent / "words"
    return directory
