import sys


class Debugger(object):
    def __init__(self):
        self.breakpoints = {}

    def call_trace(self):
        frame = sys._getframe(1)
        print(frame.f_code.co_filename, frame.f_lineno, frame.f_locals)
