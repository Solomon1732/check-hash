#!/usr/bin/env python3
"""
Functions to compares hashes to files.
"""
import hashlib
from collections.abc import Generator
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple

import exceptions


class _HashesMismatch(NamedTuple):
    """Holds a file, its expected hash and the hash calculated from it."""

    file: Path
    file_hash: str
    expected_hash: str


def _digest_hex_file_hash(file: Path, hash_func: str) -> str:
    """Returns a hexadecimal digest of a file's hash."""
    assert isinstance(file, Path), exceptions.format_wrong_type_msg(
        name="file", expected_type=Path, received_type=type(file)
    )
    assert isinstance(hash_func, str), exceptions.format_wrong_type_msg(
        name="hash_func", expected_type=str, received_type=type(hash_func)
    )
    assert (
        file.is_absolute()
    ), f"expected absolute path, got relative path instead. File path: {file}"

    with file.open("rb") as file_to_digest:
        file_hash = hashlib.file_digest(file_to_digest, hash_func)
    return file_hash.hexdigest()


def _check_hash_mismatches(
    files: Iterable[Path], expected_hashes: Iterable[str], hash_func: str
) -> Generator[_HashesMismatch, None, None]:
    """Iterate over the files, calculate their digests according to a predetermined hash function,
    compare them to expected hash values, and yield mismatches. If the number of files and expected
    hashes differs, a ValueError is raised.
    """
    assert isinstance(files, Iterable), exceptions.format_wrong_type_msg(
        name="files", expected_type=Iterable[Path], received_type=type(files)
    )
    assert isinstance(expected_hashes, Iterable), exceptions.format_wrong_type_msg(
        name="expected_hashes",
        expected_type=Iterable[str],
        received_type=type(expected_hashes),
    )
    assert isinstance(hash_func, str), exceptions.format_wrong_type_msg(
        name="hash_func", expected_type=str, received_type=type(hash_func)
    )

    for file, expected_hash in zip(files, expected_hashes, strict=True):
        file_hash = _digest_hex_file_hash(file=file, hash_func=hash_func)
        if file_hash != expected_hash.lower():
            yield _HashesMismatch(
                file=file, file_hash=file_hash, expected_hash=expected_hash
            )


def compare_files_to_hashes(
    files: Iterable[Path], expected_hashes: Iterable[str], hash_func: str
) -> None:
    """Compare files to expected hash values. If the number of files and expected hashes differs, a
    ValueError is raised.
    """
    assert isinstance(files, Iterable), exceptions.format_wrong_type_msg(
        name="files", expected_type=Iterable[Path], received_type=type(files)
    )
    assert isinstance(expected_hashes, Iterable), exceptions.format_wrong_type_msg(
        name="expected_hashes",
        expected_type=Iterable[str],
        received_type=type(expected_hashes),
    )
    assert isinstance(hash_func, str), exceptions.format_wrong_type_msg(
        name="hash_func", expected_type=str, received_type=type(hash_func)
    )

    for file, file_hash, expected_hash in _check_hash_mismatches(
        files=files, expected_hashes=expected_hashes, hash_func=hash_func
    ):
        print("File doesn't match expected value:", file)
        print("File hash:", file_hash)
        print("Expected value:", expected_hash)
        print()


if __name__ == "__main__":
    pass
