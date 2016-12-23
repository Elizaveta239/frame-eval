from debugger.pydev_debug_info import Debugger
from performance_compare.tracing_debugger import TracingDebugger
import os
import time

filename = os.path.abspath(__file__)


# The main performance test from the issue PY-14286


def foo():
    # do some busy work in parallel
    print("Started main task")
    x = 0
    for i in range(10000000):
        x += 1
    print("Completed main task")


def time_running(text):
    start = time.time()
    foo()
    finish = time.time()
    print(text, finish - start)


time_running("Time without debugging: ")

tracing_debugger = TracingDebugger(False)
tracing_debugger.add_breakpoint(filename, 15)
tracing_debugger.run()

time_running("Time with debugger based on sys.settrace(): ")
tracing_debugger.stop()

debugger = Debugger(False)
debugger.add_breakpoint(filename, 15)
debugger.run()

time_running("Time with debugger based on frame evaluation: ")
debugger.stop()
