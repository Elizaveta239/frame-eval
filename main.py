from debugger.pydev_debug_info import FrameDebugger
import os

filename = os.path.abspath(__file__)

debugger = FrameDebugger()
debugger.add_breakpoint(filename, 14)
debugger.run()


def foo():
    a = 1
    b = 2
    c = 3
    return a + b + c


foo()