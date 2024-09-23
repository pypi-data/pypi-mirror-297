# cython: language_level=3
# distutils: language = c++

from dataclasses import dataclass
from cython cimport boundscheck, wraparound
from libcpp.deque cimport deque as cpp_deque
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
    def buffer(self):
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
    def buffer(self):
        return self.buffer

    @property
    def val(self):
        return self.val

    cpdef void apply(self):
        cdef PyObject* obj
        obj = self.buffer.ahead.front()
        self.buffer.ahead.pop_front()
        Py_DECREF(<object>obj)  # Decrease reference count when popping

cdef class Buffer:
    cdef list runes
    cdef cpp_deque[PyObject*] ahead  # Use PyObject* instead of object

    def __init__(self, data):
        self.runes = build_runes(data)
        # self.ahead is automatically initialized; no need to assign to it

    @classmethod
    def from_runes(cls, list runes):
        cdef Buffer ins = cls.__new__(cls)
        ins.runes = runes
        # self.ahead is automatically initialized; no need to assign to it
        return ins

    def __repr__(self):
        cdef list ahead_list = []
        cdef PyObject* obj
        for obj in self.ahead:
            ahead_list.append(<object>obj)
        return f"Buffer({self.runes}, ahead={ahead_list})"

    cpdef Buffer copy(self):
        return Buffer.from_runes(self.runes)

    cpdef object next(self, until=SEPARATORS):
        cdef object val
        cdef object res
        cdef object tail
        cdef PyObject* obj

        if self.ahead.size() > 0:
            obj = self.ahead[0]
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
        self.ahead.push_front(obj)
