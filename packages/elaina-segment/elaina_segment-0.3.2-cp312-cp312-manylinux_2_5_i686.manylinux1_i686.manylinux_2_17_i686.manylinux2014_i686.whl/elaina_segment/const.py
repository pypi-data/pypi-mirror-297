from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Final, Generic, TypeVar, Union


T = TypeVar("T")

QUOTE = {"'": "'", '"': '"'}
ESCAPE = "\\"
CRLF = {"\n", "\r"}
SPACE = " "
SEPARATORS: Final = "".join(SPACE)


@dataclass
class Quoted(Generic[T]):
    ref: list[str | T] | str
    trigger: str
    target: str

    def __str__(self):
        return f"{self.trigger}{self.ref}{self.target}"


@dataclass
class UnmatchedQuoted(Generic[T]):
    ref: list[str | T] | str
    trigger: str

    def __str__(self):
        return f"{self.trigger}{self.ref}"


Segment = Union[Quoted[T], UnmatchedQuoted[T], str, T]
Rune = Union[str, list[T]]
Runes = list[Rune[T]]
Tail = Union[Callable[[], Runes[T]], None]
