import frame
from debugger.debug_info import Debugger

debugger = Debugger()


def trace():
    debugger.call_trace()


frame.main(trace.__code__)


def foo():
    a = 1
    b = 2
    c = 3
    d = 4
    return a + b + c + d


foo()
