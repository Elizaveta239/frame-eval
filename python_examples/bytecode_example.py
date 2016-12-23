import dis
from debugger.pydev_modify_bytecode import insert_code
from debugger.pydev_debug_info import FrameDebugger

debugger = FrameDebugger()


def foo():
    a = 0
    for i in range(10):
        print(i)
        a += i
    print("finish!'")


def trace():
    debugger.call_trace()


code = foo.__code__
code2 = trace.__code__
new_code = insert_code(code, code2, 11)

print("New code:")
dis.dis(new_code)
exec(new_code)
