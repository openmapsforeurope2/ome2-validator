'''
Helper module that implements a leaner version of `varname`.
It is less robust, but sufficient for the `vrailang` package.
'''

from dataclasses import dataclass, field
import sys
import inspect
from inspect import Traceback
from types import FrameType
import varname

_USE_VARNAME = False # Use the old varname package rather than the new FastVarname logic

@dataclass
class FastVarname:
    
    varname: str | None = field(init=False)

    def __init__(self, depth=2):
        f: FrameType = sys._getframe(depth)
        fi: Traceback = inspect.getframeinfo(f)
        
        self.varname = None

        if not _USE_VARNAME:
            ctx = fi.code_context
            if ctx and len(ctx):
                line = ctx[0]
                parts = line.split('=', 1)
                if len(parts) > 1:
                    varname_candidate = parts[0].strip()
                    if varname_candidate.isidentifier():
                        self.varname = varname_candidate
        
        if self.varname is None:
            try:
                varname_candidate: str = varname.varname(frame=depth) # type: ignore
                self.varname = varname_candidate
            except varname.ImproperUseError as _: # type: ignore
                pass
