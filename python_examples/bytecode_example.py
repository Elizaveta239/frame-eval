import dis_copy as dis
from debugger.modify_bytecode import insert_code
from debugger.debug_info import Debugger

debugger = Debugger()


def foo():
    a = 1
    b = 2
    c = 3
    d = 4
    print("Hello!")


def trace():
    debugger.call_trace()


code = foo.__code__
code2 = trace.__code__
new_code = insert_code(code, code2, 2)

print("New code:")
dis.dis(new_code)
exec(new_code)
