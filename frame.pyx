from debugger.modify_bytecode import insert_code

trace_code = None

cdef object get_bytecode_while_frame_eval(PyFrameObject *frame, int exc):
    # Show bytecode for frame with dis.dis() function
    if (str(<object> frame.f_code.co_filename)).endswith("test.py"):
        # avoid infinite recursion
        new_code = insert_code(<object> frame.f_code, trace_code, 3)
        frame.f_code = <PyCodeObject *> new_code
    return <object> _PyEval_EvalFrameDefault(frame, exc)

def main(my_trace_code):
    global trace_code
    trace_code = my_trace_code
    cdef PyThreadState *state = PyThreadState_Get()
    state.interp.eval_frame = get_bytecode_while_frame_eval
