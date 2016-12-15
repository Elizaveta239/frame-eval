# An example of disassembling code object from function

from dis import dis
from types import CodeType


def foo():
    a = 1
    b = 2
    return a + b


code = foo.__code__

# Abilities to get bytecode:

print("1. Call dis() for code object directly: ")

dis(code)

print("2. Create the new code object and call dis() for it: ")

new_code = CodeType(
    code.co_argcount,  # integer
    code.co_kwonlyargcount,  # integer
    code.co_nlocals,  # integer
    code.co_stacksize,  # integer
    code.co_flags,  # integer
    code.co_code,  # bytes
    code.co_consts,  # tuple
    code.co_names,  # tuple
    code.co_varnames,  # tuple
    code.co_filename,  # string
    code.co_name,  # string
    code.co_firstlineno,  # integer
    code.co_lnotab,  # bytes
    code.co_freevars,  # tuple
    code.co_cellvars  # tuple
)

dis(new_code)
