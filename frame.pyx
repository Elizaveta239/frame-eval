dismod = PyImport_ImportModule("dis")
disfunc = PyObject_GetAttrString(dismod, "dis")

def get_bytecode_for_python_code_obj(code):
    PyObject_CallFunction(<PyObject*> disfunc, "(O)", <PyObject*> code)

cdef get_bytecode_while_frame_eval(PyFrameObject *frame, int exc):
    # This function always fails with TypeError exception inside dis.py
    _PyEval_EvalFrameDefault(frame, exc)
    if (str(<object> frame.f_code.co_filename)).endswith("test.py"):
        # avoid infinite recursion
        PyObject_CallFunction(<PyObject*> disfunc, "(O)", <PyObject*> frame.f_code)

cdef show_filename_line(PyFrameObject *frame, int exc):
    # This function work fine
    _PyEval_EvalFrameDefault(frame, exc)
    print(<object> frame.f_code.co_filename, <object> frame.f_lineno)
    print('out')

def main():
    cdef PyThreadState *state = PyThreadState_Get()
    state.interp.eval_frame = get_bytecode_while_frame_eval
