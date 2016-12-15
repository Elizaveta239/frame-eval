# An example of disassembling code object from frame

from dis import dis
import sys


def trace_func(frame, event, arg):
    if event == "call":
        print("Entering new code block: ", frame.f_code.co_filename, frame.f_lineno)
        code = frame.f_code
        dis(code)


def foo():
    a = 1
    b = 2
    return a + b


sys.settrace(trace_func)
foo()
