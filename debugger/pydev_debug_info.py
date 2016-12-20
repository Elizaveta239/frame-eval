import sys

ignore_list = ['pydev_debug_info.py', 'pydev_modify_bytecode.py']


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
        if filename not in self.breakpoints.keys():
            self.breakpoints[filename] = []
        self.breakpoints[filename].append(line)

    def get_breakpoints_for_file(self, filename):
        return self.breakpoints.get(filename, [])

    def run(self):
        # Set frame evaluation function after debugger initialization
        import frame
        frame.main(trace.__code__)
