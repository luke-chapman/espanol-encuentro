from pathlib import Path


def default_words_directory() -> Path:
    directory = Path(__file__).resolve().parent.parent.parent / "words"
    directory.mkdir(parents=True, exist_ok=True)
    return directory
