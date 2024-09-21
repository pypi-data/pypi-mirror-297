from .const import ESCAPE as ESCAPE
from .const import QUOTE as QUOTE
from .const import SEPARATORS as SEPARATORS
from .const import Rune as Rune
from .const import Runes as Runes
from .const import Segment as Segment

try:
    from .segment_c import build_runes as build_runes
    from .segment_c import segment as segment
    from .segment_c import Quoted as Quoted
    from .segment_c import UnmatchedQuoted as UnmatchedQuoted
except ImportError:
    from .segment_py import build_runes as build_runes
    from .segment_py import segment as segment
    from .segment_py import UnmatchedQuoted as UnmatchedQuoted
    from .segment_py import Quoted as Quoted
