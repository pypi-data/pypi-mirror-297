try:
    from .buffer_c import Buffer as Buffer
    from .buffer_c import AheadToken as AheadToken
    from .buffer_c import SegmentToken as SegmentToken
except ImportError:
    from .buffer_py import Buffer as Buffer
    from .buffer_py import AheadToken as AheadToken
    from .buffer_py import SegmentToken as SegmentToken