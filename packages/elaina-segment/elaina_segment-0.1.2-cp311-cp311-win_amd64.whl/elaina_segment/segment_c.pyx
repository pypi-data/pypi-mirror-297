# cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, infer_types=True, binding=True

from __future__ import annotations
from cpython.list cimport PyList_Append, PyList_New, PyList_GetSlice, PyList_GET_SIZE, PyList_GET_ITEM, PyList_SetSlice
from cpython.unicode cimport PyUnicode_Join, PyUnicode_Substring, PyUnicode_Check, PyUnicode_GET_LENGTH, PyUnicode_READ_CHAR, PyUnicode_FromKindAndData, PyUnicode_4BYTE_KIND, PyUnicode_FindChar
from cpython.dict cimport PyDict_Contains, PyDict_GetItem

from dataclasses import dataclass
from typing import Any
from .const import QUOTE


cdef ESCAPE = <Py_UCS4>0x5C


@dataclass
cdef class Quoted:
    ref: list[str | Any] | str
    trigger: str
    target: str

    def __str__(self):
        return f"{self.trigger}{self.ref}{self.target}"


@dataclass
cdef class UnmatchedQuoted:
    ref: list[str | Any] | str
    trigger: str

    def __str__(self):
        return f"{self.trigger}{self.ref}"



def build_runes(list data):
    cdef:
        list res = PyList_New(<Py_ssize_t>0)
        list s = PyList_New(<Py_ssize_t>0)
        list d = PyList_New(<Py_ssize_t>0)
        bint _s = <bint>0

    for i in data:
        if PyUnicode_Check(i) == 1:
            if PyList_GET_SIZE(d) > 0:
                PyList_Append(res, d)
                d = PyList_New(<Py_ssize_t>0)
            PyList_Append(s, i)
            _s = <bint>1
        else:
            if PyList_GET_SIZE(s) > 0:
                PyList_Append(res, PyUnicode_Join("", s))
                s = PyList_New(<Py_ssize_t>0)
            PyList_Append(d, i)
            _s = <bint>0

    if _s == 1:
        PyList_Append(res, PyUnicode_Join("", s))
    elif PyList_GET_SIZE(d) > 0:
        PyList_Append(res, d)

    return res


cdef inline str ucs4_to_str(Py_UCS4 ucs4_char):
    cdef const void* buffer = <const void*>(&ucs4_char)
    return PyUnicode_FromKindAndData(PyUnicode_4BYTE_KIND, buffer, <Py_ssize_t>1)


def segment(list seq, str until):
    cdef Py_ssize_t seq_n = PyList_GET_SIZE(seq)
    if seq_n == 0:
        return
    
    cdef:
        Py_ssize_t head_len = <Py_ssize_t>0
        Py_ssize_t tail_len
        Py_ssize_t until_len = PyUnicode_GET_LENGTH(until)
        Py_ssize_t united_tail_len
        Py_ssize_t x
        Py_ssize_t y
        Py_ssize_t quoted_size
        Py_ssize_t ix
        Py_ssize_t united_tail_rune_len
        Py_ssize_t first_break_str = <Py_ssize_t>(-1)
        Py_ssize_t first_break_obj_x = <Py_ssize_t>(-1)
        Py_ssize_t first_break_obj_y = <Py_ssize_t>(-1)
        Py_ssize_t tail_index = <Py_ssize_t>0

        Py_UCS4 c
        Py_UCS4 head_first
        Py_UCS4 prev
        Py_UCS4 quote

        bint head_is_str = <bint>0
        bint valid_until = <bint>(until_len > 0)

        str head_tail
        list united_tail
        list quoted
        object united_tail_rune

        object head = ""
        list tail = seq

    while head_len == 0:
        if tail_index >= seq_n:
            return

        head = <object>PyList_GET_ITEM(seq, tail_index)
        tail_index += 1

        if valid_until == 1:
            head_is_str = PyUnicode_Check(head)
            if head_is_str == 1:
                head = (<str>head).lstrip(until)
                head_len = PyUnicode_GET_LENGTH(head)
            else:
                head_len = PyList_GET_SIZE(head)
    
    tail = PyList_GetSlice(seq, tail_index, seq_n)
    tail_len = seq_n - tail_index
    united_tail_len = tail_len + 1

    if head_is_str == 1:
        head_first = PyUnicode_READ_CHAR(head, <Py_ssize_t>0)
        head_tail = PyUnicode_Substring(head, <Py_ssize_t>1, head_len)

        if PyDict_Contains(QUOTE, head_first):
            quote = PyUnicode_READ_CHAR(<str>PyDict_GetItem(QUOTE, head_first), <Py_ssize_t>0)

            united_tail = [head_tail] + tail
            quoted = PyList_New(<Py_ssize_t>0)

            x = <Py_ssize_t>0
            while x < united_tail_len:
                united_tail_rune = <object>PyList_GET_ITEM(united_tail, x)
                if PyUnicode_Check(united_tail_rune) == 1:
                    united_tail_rune_len = PyUnicode_GET_LENGTH(united_tail_rune)
                    if united_tail_rune_len > 0:
                        y = <Py_ssize_t>0

                        while y < united_tail_rune_len:
                            c = PyUnicode_READ_CHAR(united_tail_rune, y)
                            if c == quote:
                                if y != 0:
                                    if PyUnicode_READ_CHAR(united_tail_rune, y - 1) == ESCAPE:
                                        y += 1
                                        continue
                
                                    PyList_Append(quoted, PyUnicode_Substring(united_tail_rune, <Py_ssize_t>0, y))

                                if y + 1 == united_tail_rune_len:
                                    return Quoted(quoted, ucs4_to_str(head_first), ucs4_to_str(quote)), lambda: PyList_GetSlice(united_tail, x + 1, tail_len + 1)

                                return Quoted(quoted, ucs4_to_str(head_first), ucs4_to_str(quote)), lambda: (
                                    [PyUnicode_Substring(united_tail_rune, y + 1, united_tail_rune_len)]
                                ) + PyList_GetSlice(united_tail, x + 1, tail_len + 1)
                            
                            elif (
                                first_break_str == -1 and
                                first_break_obj_x == -1 and
                                valid_until == 1 and
                                PyUnicode_FindChar(until, c, <Py_ssize_t>0, until_len, 1) != -1
                            ):
                                first_break_str = y

                            y += 1
                    
                        PyList_Append(quoted, united_tail_rune)
                else:
                    quoted_size = PyList_GET_SIZE(quoted)
                    if first_break_str == -1 and first_break_obj_x == -1:
                        first_break_obj_x = quoted_size
                        first_break_obj_y = x

                    PyList_SetSlice(quoted, quoted_size, quoted_size, united_tail_rune)
                
                x += 1
            
            if first_break_obj_x != -1:
                return UnmatchedQuoted(PyList_GetSlice(quoted, <Py_ssize_t>0, first_break_obj_x + 1), ucs4_to_str(head_first)), lambda: [
                    PyList_GetSlice((l := <list>PyList_GET_ITEM(united_tail, first_break_obj_y)), <Py_ssize_t>1, PyList_GET_SIZE(l))
                ] + PyList_GetSlice(united_tail, first_break_obj_y + 1, PyList_GET_SIZE(united_tail))
            
            elif first_break_str != -1:
                return UnmatchedQuoted(
                    PyUnicode_Substring(head_tail, <Py_ssize_t>0, first_break_str), ucs4_to_str(head_first)
                ), lambda: [PyUnicode_Substring(head_tail, first_break_str, head_len - 1)] + tail

        elif valid_until == 1:
            ix = <Py_ssize_t>1
            prev = head_first

            while ix < head_len:
                c = PyUnicode_READ_CHAR(head, ix)
                if prev != ESCAPE and PyUnicode_FindChar(until, c, <Py_ssize_t>0, until_len, 1) != -1:
                    return PyUnicode_Substring(head, <Py_ssize_t>0, ix), lambda: [
                        PyUnicode_Substring(head, ix + 1, head_len)
                    ] + tail

                ix += 1
                prev = c
    else:
        head_len = PyList_GET_SIZE(head)

        if head_len > 1:
            tail = [<list>PyList_GetSlice(head, <Py_ssize_t>1, head_len)] + tail
            head = <object>PyList_GET_ITEM(head, <Py_ssize_t>0)

            return head, lambda: tail
        
        head = <object>PyList_GET_ITEM(head, <Py_ssize_t>0)

    if tail_len == 0:
        return head, None

    return head, lambda: tail
