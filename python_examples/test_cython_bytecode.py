# An example of disassembling code object in Cython

import frame

def foo():
    a = 1
    b = 2
    return a + b

frame.get_bytecode_for_python_code_obj(foo.__code__)
