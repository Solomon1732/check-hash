#!/usr/bin/env python3
"""
Main module of the program.
"""
import argparse
import enum
import sys
from collections.abc import Generator
from pathlib import Path

import compare_hashes
from exceptions import UnequalFileHashNumberError


@enum.unique
class _HashFunction(enum.StrEnum):
    """Aaccepted hash functions."""

    MD5 = enum.auto()
    SHA1 = enum.auto()
    SHA225 = enum.auto()
    SHA256 = enum.auto()
    SHA384 = enum.auto()
    SHA512 = enum.auto()


def main() -> None:
    """Main function of the module."""
    parser = argparse.ArgumentParser(
        description="A program for checking one or more files hash against a known hash value"
    )
    parser.add_argument(
        "--hash-function",
        default=_HashFunction.SHA256.value,
        choices=[hash_func.value for hash_func in _HashFunction],
        help=(
            "A set of hash functions to use on the chosen file or files."
            " The default function is sha256"
        ),
    )
    parser.add_argument(
        "--files",
        action="extend",
        nargs="+",
        type=Path,
        required=True,
        help=(
            "A file or files to be compared against a set of hash values. The number of files has"
            " to match that of supplied hash values. If it isn't, the program exits with an error."
            " Seperate the files with spaces"
        ),
    )
    parser.add_argument(
        "--expected_hashes",
        action="extend",
        nargs="+",
        required=True,
        help=(
            "A hash value or values to compare against one or more files' calculated hash."
            " The number of the former must match that of the latter. If it isn't,"
            " the program exits with an error. Seperate the hashes with spaces"
        ),
    )
    args = parser.parse_args()
    if len(args.files) != len(args.expected_hashes):
        raise UnequalFileHashNumberError(
            files_num=len(args.files), hashes_num=len(args.expected_hashes)
        )
    files: Generator[Path, None, None] = (
        file.resolve(strict=True) for file in args.files
    )
    expected_hashes: list[str] = args.expected_hashes
    hash_func: str = args.hash_function

    compare_hashes.compare_files_to_hashes(
        files=files, expected_hashes=expected_hashes, hash_func=hash_func
    )


if __name__ == "__main__":
    try:
        main()
    except UnequalFileHashNumberError as err:
        # Even though this variable exists in a context of error handling, it is still in the
        # global scope. Since pylint treats it as such, and isn't aware of context, it is necessary
        # to disable the check
        # pylint: disable-next=invalid-name
        err_msg = (
            f"Error: Unequal number of files and hashes. {err.files_num} files,"
            f" {err.hashes_num} hashes."
        )
        sys.exit(err_msg)
    except FileNotFoundError as err:
        sys.exit(f"Error: {err}")
