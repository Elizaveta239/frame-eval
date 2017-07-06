import dis
from debugger.pydev_modify_bytecode import insert_code
from debugger.pydev_debug_info import FrameDebugger

my_debugger = FrameDebugger()


def foo():
    a = 0
    for i in range(10):
        print(i)
        a += i
    print("finish!'")


def my_trace():
    from debugger.pydev_debugger import trace_wrapper
    trace_wrapper()


code = foo.__code__
code2 = my_trace.__code__
success, new_code = insert_code(code, code2, 11)

print("New code:")
dis.dis(new_code)
exec(new_code)
