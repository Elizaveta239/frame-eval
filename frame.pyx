from debugger.pydev_modify_bytecode import insert_code
from debugger.pydev_debugger import get_global_debugger, ignore_list
import dis

trace_code = None

cdef PyObject* get_bytecode_while_frame_eval(PyFrameObject *frame, int exc):
    filename = str(<object> frame.f_code.co_filename)
    skip_file = False
    for skip_filename in ignore_list:
        # avoid infinite recursion inside debugger
        if filename.endswith(skip_filename):
            skip_file = True
            break
    if not skip_file:
        debugger = get_global_debugger()
        breakpoints = debugger.get_breakpoints_for_file(filename)
        if breakpoints:
            for offset, line in dis.findlinestarts(<object> frame.f_code):
                if line in breakpoints:
                    new_code = insert_code(<object> frame.f_code, trace_code, line)
                    frame.f_code = <PyCodeObject *> new_code
    return _PyEval_EvalFrameDefault(frame, exc)

def main(my_trace_code):
    global trace_code
    trace_code = my_trace_code
    cdef PyThreadState *state = PyThreadState_Get()
    state.interp.eval_frame = get_bytecode_while_frame_eval

def stop_frame_eval():
    cdef PyThreadState *state = PyThreadState_Get()
    state.interp.eval_frame = _PyEval_EvalFrameDefault
