# cython: language_level=3
# distutils: language = c++

from dataclasses import dataclass
from cython cimport boundscheck, wraparound
from libcpp.stack cimport stack as cpp_stack
from cpython.ref cimport PyObject, Py_INCREF, Py_DECREF
from . import SEPARATORS, Quoted, UnmatchedQuoted, segment
from .segment_c cimport build_runes
from .err import OutOfData

# Disable certain checks for performance optimization
@boundscheck(False)
@wraparound(False)
@dataclass
cdef class SegmentToken:
    cdef Buffer buffer
    cdef object val
    cdef object tail  # Callable[[], list] or None

    @property
    def buffer(self) -> Buffer:
        return self.buffer

    @property
    def val(self):
        return self.val

    cpdef void apply(self):
        if self.tail is not None:
            self.buffer.runes = self.tail()
        else:
            self.buffer.runes = []

@boundscheck(False)
@wraparound(False)
@dataclass
cdef class AheadToken:
    cdef Buffer buffer
    cdef object val

    @property
    def buffer(self) -> Buffer:
        return self.buffer

    @property
    def val(self):
        return self.val

    cpdef void apply(self):
        cdef PyObject* obj
        obj = self.buffer.ahead.top()
        self.buffer.ahead.pop()
        Py_DECREF(<object>obj)  # Decrease reference count when popping

cdef class Buffer:
    cdef list runes
    cdef cpp_stack[PyObject*] ahead  # Use PyObject* instead of object

    def __init__(self, data, runes: bool = True):
        self.runes = data
        if runes:
            self._to_runes()

    cdef _to_runes(self):
        self.runes = build_runes(self.runes)

    def __repr__(self):
        cdef list ahead_list = []
        return f"Buffer({self.runes}, ahead={ahead_list})"

    cpdef Buffer copy(self):
        return Buffer(self.runes, runes=False)

    cpdef object next(self, until=SEPARATORS):
        cdef object val
        cdef object res
        cdef object tail
        cdef PyObject* obj

        if self.ahead.size() > 0:
            obj = self.ahead.top()
            Py_INCREF(<object>obj)  # Increase reference count when accessing
            return AheadToken(self, <object>obj)

        res = segment(self.runes, until)
        if res is None:
            raise OutOfData()

        val, tail = res
        return SegmentToken(self, val, tail)

    def pushleft(self, *segments):
        cdef list s = []
        cdef object seg
        for seg in segments:
            if isinstance(seg, (UnmatchedQuoted, Quoted)):
                s.append(str(seg))
            elif seg:
                s.append(seg)

        self.runes = build_runes(s) + self.runes

    cpdef void add_to_ahead(self, object val):
        cdef PyObject* obj = <PyObject*>val
        Py_INCREF(<object>obj)  # Increase reference count when storing
        self.ahead.push(obj)

    def __dealloc__(self):
        cdef PyObject* obj
        while self.ahead.size() > 0:
            obj = self.ahead.top()
            self.ahead.pop()
            Py_DECREF(<object>obj)  # Decrease reference count when deallocating
