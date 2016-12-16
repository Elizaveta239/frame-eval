dismod = PyImport_ImportModule("dis")
disfunc = PyObject_GetAttrString(dismod, "dis")

def get_bytecode_for_python_code_obj(code):
    PyObject_CallFunction(<PyObject*> disfunc, "(O)", <PyObject*> code)

cdef object get_bytecode_while_frame_eval(PyFrameObject *frame, int exc):
    # Show bytecode for frame with dis.dis() function
    if (str(<object> frame.f_code.co_filename)).endswith("test.py"):
        # avoid infinite recursion
        print("Show bytecode for frame:", <object> frame.f_code.co_filename, <object> frame.f_lineno)
        PyObject_CallFunction(<PyObject*> disfunc, "(O)", <PyObject*> frame.f_code)
    return <object> _PyEval_EvalFrameDefault(frame, exc)

def main():
    cdef PyThreadState *state = PyThreadState_Get()
    state.interp.eval_frame = get_bytecode_while_frame_eval
