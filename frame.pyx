

cdef show_filename_line(PyFrameObject *frame, int exc):
    _PyEval_EvalFrameDefault(frame, exc)
    print(<object> frame.f_code.co_filename, <object> frame.f_lineno)
    print('out')

def main():
    cdef PyThreadState *state = PyThreadState_Get()
    state.interp.eval_frame = show_filename_line
