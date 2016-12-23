from debugger.pydev_debugger import BaseDebugger, set_global_debugger
import sys


class TracingDebugger(BaseDebugger):
    """
    The debugger implementation based on sys.settrace() function
    """

    def __init__(self, show_debug_info=True):
        super().__init__(show_debug_info)
        set_global_debugger(self)

    def call_trace(self, frame, event, arg):
        breakpoints_list = self.breakpoints.get(frame.f_code.co_filename, None)
        if breakpoints_list:
            if frame.f_lineno in breakpoints_list:
                if self.show_debug_info:
                    print(frame.f_code.co_filename, frame.f_lineno, frame.f_locals)
        return self.call_trace

    def run(self):
        # Set tracing function
        sys.settrace(self.call_trace)

    def stop(self):
        sys.settrace(None)
