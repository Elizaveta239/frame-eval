from debugger.pydev_debug_info import Debugger

debugger = Debugger()
debugger.add_breakpoint('/home/user/work/frame-eval/main.py', 12)
debugger.run()


def foo():
    a = 1
    b = 2
    c = 3
    d = 4
    return a + b + c + d


foo()
