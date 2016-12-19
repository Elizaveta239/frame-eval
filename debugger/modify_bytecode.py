import dis
from types import CodeType


def _modify_co_names_for_debugger(orig_code, insert_code):
    """
    Modify co_names for using `debugger` and `call_trace` in the correct place
    This function should be rewritten in a more common way!
    """
    orig_names_len = len(orig_code.co_names)
    code_with_new_names = list(insert_code.co_code[:6])  # remove `return` commands from function bytecode
    code_with_new_names[1] = orig_names_len  # Load `debugger` name
    code_with_new_names[3] = orig_names_len + 1  # Load `call_trace` name
    new_names = orig_code.co_names + insert_code.co_names
    return bytes(code_with_new_names), new_names


def _modify_new_lines(code_to_modify, code_insert, before_line):
    new_list = list(code_to_modify.co_lnotab)
    if before_line * 2 < len(new_list):
        new_list[before_line * 2] += len(code_insert)
    return bytes(new_list)


def insert_code(code_to_modify, code_to_insert, before_line):
    """
    Insert piece of code `code_to_insert` to `code_to_modify` right inside the line `before_line` before the
    instruction on this line by modifying original bytecode

    :param code_to_modify: Code to modify
    :param code_to_insert: Code to insert
    :param before_line: Number of line for code insertion
    :return: modified code
    """
    linestarts = dict(dis.findlinestarts(code_to_modify))
    abs_after_line = code_to_modify.co_firstlineno + before_line
    offset = None
    for off, line_no in linestarts.items():
        if line_no == abs_after_line:
            offset = off

    code_insert, new_names = _modify_co_names_for_debugger(code_to_modify, code_to_insert)
    new_bytes = code_to_modify.co_code[:offset] + code_insert + code_to_modify.co_code[offset:]

    new_lnotab = _modify_new_lines(code_to_modify, code_insert, before_line)

    new_code = CodeType(
        code_to_modify.co_argcount,  # integer
        code_to_modify.co_kwonlyargcount,  # integer
        code_to_modify.co_nlocals,  # integer
        code_to_modify.co_stacksize,  # integer
        code_to_modify.co_flags,  # integer
        new_bytes,  # bytes
        code_to_modify.co_consts,  # tuple
        new_names,  # tuple
        code_to_modify.co_varnames,  # tuple
        code_to_modify.co_filename,  # string
        code_to_modify.co_name,  # string
        code_to_modify.co_firstlineno,  # integer
        new_lnotab,  # bytes
        code_to_modify.co_freevars,  # tuple
        code_to_modify.co_cellvars  # tuple
    )
    return new_code
