from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, TypeVar
from .const import Segment, Runes, Tail

T = TypeVar("T")

@dataclass
class Quoted(Generic[T]):
    ref: list[str | T] | str
    trigger: str
    target: str

@dataclass
class UnmatchedQuoted(Generic[T]):
    ref: list[str | T] | str
    trigger: str

def build_runes(data: Iterable[str | T]) -> Runes[T]: ...
def segment(seq: Runes[T], until: str) -> tuple[Segment[T], Tail[T]] | None: ...
