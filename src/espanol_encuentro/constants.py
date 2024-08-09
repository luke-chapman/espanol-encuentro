import os
from pathlib import Path


def __default_words_directory_root() -> Path:
    one_drive = os.getenv("ONEDRIVE")
    if one_drive and os.path.exists(one_drive):
        return Path(one_drive).resolve()
    else:
        return Path.home()


def default_words_directory() -> Path:
    root = __default_words_directory_root()
    words = root / ".espanol-encuentro" / "words"
    words.mkdir(parents=True, exist_ok=True)
    return words


def sample_words_directory() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "sample_words"
