from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, TypeVar
from .const import Quoted, Tail, UnmatchedQuoted, Segment, Runes, ESCAPE, QUOTE

T = TypeVar("T")


def build_runes(data: Iterable[str | T]) -> Runes[T]:
    res = []
    s, d = [], []
    _s = False
    for i in data:
        if isinstance(i, str):
            if d:
                res.append(d)
                d = []
            s.append(i)
            _s = True
        else:
            if s:
                res.append("".join(s))
                s = []
            d.append(i)
            _s = False

    if _s:
        res.append("".join(s))
    elif d:
        res.append(d)

    return res


def segment(seq: Runes[T], until: str) -> tuple[Segment, Tail[T]] | None:
    if not seq:
        return

    head_is_str = False

    head, *tail = seq
    if until:
        head_is_str = isinstance(head, str)
        if head_is_str:
            head = head.lstrip("".join(until))  # type: ignore

    while not head:
        if not tail:
            return

        head, *tail = tail
        if until:
            head_is_str = isinstance(head, str)
            if head_is_str:
                head = head.lstrip("".join(until))  # type: ignore

    if head_is_str:
        if TYPE_CHECKING:
            assert isinstance(head, str)

        head_first, head_tail = head[0], head[1:]
        if head_first in QUOTE:
            quote = QUOTE[head_first]

            first_break_str = None
            first_break_obj = None
            u: list[str | list[T]] = [head_tail, *tail]
            quoted: list[str | T] = []

            for x, h in enumerate(u):
                # h = u[x]
                # print(h, first_break_obj, first_break_str)
                if isinstance(h, str):
                    if h:  # 这里为 else 分支屏蔽了 h = "" 的情况，维护了其中 h: runes 的类型。
                        for y, char in enumerate(h):
                            # print(f"{char=!r}")
                            # h: str => h[y - 1]: str | never(if y == 0)
                            if char == quote:
                                if y != 0:
                                    if h[y - 1] == ESCAPE:
                                        continue

                                    quoted.append(h[:y])

                                return Quoted(quoted, head_first, quote), (
                                    lambda: ([t] if (t := h[y + 1 :]) else []) + u[x + 1 :]
                                )

                            elif first_break_str is None and first_break_obj is None and char in until:
                                first_break_str = y

                        quoted.append(h)
                else:
                    # h: runes - empty
                    if first_break_str is None and first_break_obj is None:
                        first_break_obj = len(quoted), x

                    quoted.extend(h)

            if first_break_obj is not None:
                m, n = first_break_obj
                return UnmatchedQuoted(quoted[: m + 1], head_first), lambda: [
                    u[n][1:],
                    *u[n + 1 :],
                ]

            if first_break_str is not None:
                return UnmatchedQuoted(head_tail[:first_break_str], head_first), lambda: [
                    head_tail[first_break_str + 1 :],
                    *tail,
                ]

            return head, lambda: tail

        if until:
            ix = 1
            prev = head_first
            for char in head_tail:
                if char in until and prev != ESCAPE:
                    return head[:ix], lambda: [head[ix + 1 :], *tail]

                ix += 1
                prev = char

        if tail:
            return head, lambda: tail
        else:
            return head, None
    else:
        head, *tail = head[0], head[1:], *tail

        if not tail:
            return head, None

        return head, lambda: tail
