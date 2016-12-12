cdef our_eval_frame(PyFrameObject *frame, int exc):
    print('in')
    _PyEval_EvalFrameDefault(frame, exc)
    print('out')

def main():
    cdef PyThreadState *state = PyThreadState_Get()
    state.interp.eval_frame = our_eval_frame
