import os
from pathlib import Path
from typing import Callable, Any
from typing import Optional

from .encoding import auto_decode, _DEFAULT_ENCODING


def load_binary_file(path: str) -> bytes:
    """
    Load binary data from given path
    :param path: file path
    :return: binary data
    """
    return Path(path).read_bytes()


def load_text_file(path: str, encoding: Optional[str] = None) -> str:
    """
    Load text data from given path
    :param path: file path
    :param encoding: data encoding
    :return: text data
    """
    return auto_decode(load_binary_file(path), encoding)


def save_binary_file(path: str, data: bytes):
    """
    Save binary data to given path
    :param path: file path
    :param data: binary data
    """
    return Path(path).write_bytes(data)


def save_text_file(path: str, data: str, encoding: Optional[str] = None):
    """
    Save text data to given path
    :param path: file path
    :param data: text data
    :param encoding: data encoding
    """
    return save_binary_file(path, data.encode(encoding or _DEFAULT_ENCODING))


def yield_file_filter(path: str, condition: Optional[Callable[[str], Any]] = None):
    """
    Yield files match the given condition
    :param path: base path
    :param condition: condition used to check file (default is None, means checking is not needed)
    :return: file path generator
    """
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.access(full_path, os.R_OK):
            if os.path.isfile(full_path):
                if not condition or condition(full_path):
                    yield full_path
            elif os.path.isdir(full_path):
                for _file in yield_file_filter(full_path, condition):
                    yield _file
