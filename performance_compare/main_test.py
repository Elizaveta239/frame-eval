from debugger.pydev_debug_info import Debugger
from performance_compare.tracing_debugger import TracingDebugger
import os
import time

filename = os.path.abspath(__file__)

debugger = Debugger(False)
# debugger = TracingDebugger(False)
debugger.add_breakpoint(filename, 27)
debugger.run()

start = time.time()


def conact_with_space(str1, str2):
    res = str1 + " "
    res = res + str2
    return res


def foo():
    sum = ""
    sum_int = 0
    for i in range(50000):
        sum = conact_with_space(sum, str(i))
        sum_int += i
    return sum


foo()

finish = time.time()
print("Time spend:", finish - start)
