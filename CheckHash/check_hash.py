#!/usr/bin/env python3
"""
Main module of the program.
"""
import argparse
import enum
import pathlib


@enum.unique
class HashFunction(enum.StrEnum):
    """A collection of accepted hash functions."""

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
        default=HashFunction.SHA256.value,
        choices=[hash_func.value for hash_func in HashFunction],
        help=(
            "A set of hash functions to use on the chosen file or files."
            " The default function is sha256"
        ),
    )
    parser.add_argument(
        "--files",
        action="extend",
        nargs="+",
        type=pathlib.Path,
        required=True,
        help=(
            "A file or files to be compared against a set of hash values. The number of files has"
            " to match that of supplied hash values. If it isn't, the program exits with an error"
        ),
    )
    parser.add_argument(
        "--hash-values",
        action="extend",
        nargs="+",
        required=True,
        help=(
            "A hash value or values to compare against one or more files' calculated hash."
            " The number of the former must match that of the latter. If it isn't,"
            " the program exits with an error"
        ),
    )
    # pylint: disable=W0612
    args = parser.parse_args()


if __name__ == "__main__":
    main()
