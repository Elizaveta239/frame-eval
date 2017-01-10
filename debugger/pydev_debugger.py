
ignore_list = ['pydev_debug_info.py', 'pydev_modify_bytecode.py', 'pydev_debugger.py', 'dis.py']


class GlobalDebuggerHolder:
    global_dbg = None


def get_global_debugger():
    return GlobalDebuggerHolder.global_dbg


def set_global_debugger(dbg):
    GlobalDebuggerHolder.global_dbg = dbg


def trace():
    debugger = get_global_debugger()
    debugger.call_trace()


def trace_wrapper():
    import debugger.pydev_debugger
    debugger.pydev_debugger.trace()


class BaseDebugger(object):
    def __init__(self, show_debug_info=True):
        self.show_debug_info = show_debug_info
        self.breakpoints = {}

    def add_breakpoint(self, filename, line):
        if filename not in self.breakpoints.keys():
            self.breakpoints[filename] = []
        self.breakpoints[filename].append(line)

    def get_breakpoints_for_file(self, filename):
        return self.breakpoints.get(filename, [])

    def call_trace(self, *args, **kwargs):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()
