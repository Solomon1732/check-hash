#!/usr/bin/env python3
"""
Holds the project's exception.
"""
from typing import Final


def format_wrong_type_msg(name: str, expected_type: type, received_type: type):
    """Format a message for a wrong variable type. Useful for assertions or exceptions."""
    return f"expected '{name}' to be {expected_type}, got {received_type} instead"


class UnequalFileHashNumberError(ValueError):
    """Exception class for when sequences differ in length."""

    def __init__(self, *args: object, files_num: int, hashes_num: int) -> None:
        assert isinstance(files_num, int), format_wrong_type_msg(
            name="files_num", expected_type=int, received_type=type(files_num)
        )
        assert isinstance(hashes_num, int), format_wrong_type_msg(
            name="hashes_num", expected_type=int, received_type=type(hashes_num)
        )
        assert (
            files_num >= 0
        ), f"expected a non-negative number of files, got {files_num} instead"
        assert (
            hashes_num >= 0
        ), f"expected a non-negative number of hash values, got {hashes_num} instead"

        super(*args)
        self._files_num: Final[int] = files_num
        self._hashes_num: Final[int] = hashes_num

    @property
    def files_num(self) -> int:
        """Returns the number of files."""
        return self._files_num

    @property
    def hashes_num(self) -> int:
        """Returns the number of hash values."""
        return self._hashes_num


if __name__ == "__main__":
    pass
