import dis
from types import CodeType


def _modify_co_names_for_debugger(orig_code, insert_code):
    """
    Modify co_names for using correct variable names
    """
    orig_names_len = len(orig_code.co_names)
    code_with_new_names = list(insert_code.co_code[:-4])  # remove LOAD_CONST 0 and RETURN_VALUE instructions
    # from function bytecode
    new_names = orig_code.co_names + insert_code.co_names
    # insert variable's names into new code object
    for i in range(0, len(insert_code.co_names)):
        code_with_new_names[i * 2 + 1] = orig_names_len + i
    return bytes(code_with_new_names), new_names


def _modify_new_lines(code_to_modify, code_insert, before_line):
    new_list = list(code_to_modify.co_lnotab)
    if before_line * 2 < len(new_list):
        new_list[before_line * 2] += len(code_insert)
    return bytes(new_list)


def _modify_labels(code_obj, offset_of_inserted_code, size_of_inserted_code):
    """
    Update labels for the relative jump targets
    :param code_obj: code to modify
    :param offset_of_inserted_code: offset for the inserted code
    :param offset_of_inserted_code: size of the inserted code
    :return: bytes sequence with modified labels
    """
    offsets_for_modification = []
    for offset, op, arg in dis._unpack_opargs(code_obj):
        if arg is not None:
            if op in dis.hasjrel:
                label = offset + 2 + arg
                if offset <= offset_of_inserted_code <= label:
                    # change labels for relative jump targets if code was inserted inside
                    offsets_for_modification.append(offset)
            elif op in dis.hasjabs:
                # change label for absolute jump if code was inserted before it
                if offset_of_inserted_code <= arg:
                    offsets_for_modification.append(offset)
    code_list = list(code_obj)
    for i in range(0, len(code_obj), 2):
        op = code_list[i]
        if i in offsets_for_modification and op >= dis.HAVE_ARGUMENT:
            code_list[i + 1] += size_of_inserted_code
    return bytes(code_list)


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
    if before_line not in linestarts.values():
        return code_to_modify
    offset = None
    for off, line_no in linestarts.items():
        if line_no == before_line:
            offset = off

    code_insert, new_names = _modify_co_names_for_debugger(code_to_modify, code_to_insert)
    modified_code = _modify_labels(code_to_modify.co_code, offset, len(code_insert))
    new_bytes = modified_code[:offset] + code_insert + modified_code[offset:]

    new_lnotab = _modify_new_lines(code_to_modify, code_insert, before_line - code_to_modify.co_firstlineno)

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
