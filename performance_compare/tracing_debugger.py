import sys

ignore_list = ['pydev_debug_info.py', 'pydev_modify_bytecode.py', 'tracing_debugger.py']


class TracinglDebuggerHolder:
    global_dbg = None


def get_tracing_debugger():
    return TracinglDebuggerHolder.global_dbg


def set_tracing_debugger(dbg):
    TracinglDebuggerHolder.global_dbg = dbg


class TracingDebugger(object):
    def __init__(self, show_debug_info=True):
        set_tracing_debugger(self)
        self.show_debug_info = show_debug_info
        self.breakpoints = {}

    def call_trace(self, frame, event, arg):
        breakpoints_list = self.breakpoints.get(frame.f_code.co_filename, None)
        if breakpoints_list:
            if frame.f_lineno in breakpoints_list:
                if self.show_debug_info:
                    print(frame.f_code.co_filename, frame.f_lineno, frame.f_locals)
        return self.call_trace

    def add_breakpoint(self, filename, line):
        if filename not in self.breakpoints.keys():
            self.breakpoints[filename] = []
        self.breakpoints[filename].append(line)

    def get_breakpoints_for_file(self, filename):
        return self.breakpoints.get(filename, [])

    def run(self):
        # Set tracing function
        sys.settrace(self.call_trace)
