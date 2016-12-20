import sys

ignore_list = ['debug_info.py', 'modify_bytecode.py']


class GlobalDebuggerHolder:
    global_dbg = None


def get_global_debugger():
    return GlobalDebuggerHolder.global_dbg


def set_global_debugger(dbg):
    GlobalDebuggerHolder.global_dbg = dbg


def trace():
    global debugger
    debugger.call_trace()


class Debugger(object):
    def __init__(self):
        set_global_debugger(self)
        self.breakpoints = {}

    def call_trace(self):
        frame = sys._getframe(1)
        print(frame.f_code.co_filename, frame.f_lineno, frame.f_locals)

    def add_breakpoint(self, filename, line):
        self.breakpoints[filename] = line

    def get_breakpoints(self):
        return self.breakpoints

    def run(self):
        import frame
        # Set frame evaluation function after debugger initialization
        frame.main(trace.__code__)
