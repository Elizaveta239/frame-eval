from debugger.pydev_debugger import BaseDebugger, set_global_debugger, trace
import sys


class FrameDebugger(BaseDebugger):
    def __init__(self, show_debug_info=True):
        super().__init__(show_debug_info)
        set_global_debugger(self)

    def call_trace(self):
        frame = sys._getframe(2)
        if self.show_debug_info:
            print(frame.f_code.co_filename, frame.f_lineno, frame.f_locals)

    def run(self):
        # Set frame evaluation function after debugger initialization
        import frame
        frame.main()

    def stop(self):
        import frame
        frame.stop_frame_eval()
