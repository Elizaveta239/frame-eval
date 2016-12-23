from debugger.pydev_debug_info import FrameDebugger
import os

filename = os.path.abspath(__file__)

debugger = FrameDebugger()
debugger.add_breakpoint(filename, 15)
debugger.add_breakpoint(filename, 21)
debugger.run()


def bar():
    t = 12
    s = 10
    return t + s


def foo():
    a = 1
    b = 2
    c = 3
    bar()
    return a + b + c


foo()
