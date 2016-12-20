from debugger.pydev_modify_bytecode import insert_code
from debugger.pydev_debug_info import get_global_debugger, ignore_list

trace_code = None

cdef object get_bytecode_while_frame_eval(PyFrameObject *frame, int exc):
    filename = str(<object> frame.f_code.co_filename)
    skip_file = False
    for skip_filename in ignore_list:
        # avoid infinite recursion inside debugger
        if filename.endswith(skip_filename):
            skip_file = True
            break
    if not skip_file:
        debugger = get_global_debugger()
        breakpoints = debugger.get_breakpoints()
        if filename in breakpoints.keys():
            line = breakpoints[filename]
            new_code = insert_code(<object> frame.f_code, trace_code, line)
            frame.f_code = <PyCodeObject *> new_code
    return <object> _PyEval_EvalFrameDefault(frame, exc)

def main(my_trace_code):
    global trace_code
    trace_code = my_trace_code
    cdef PyThreadState *state = PyThreadState_Get()
    state.interp.eval_frame = get_bytecode_while_frame_eval
