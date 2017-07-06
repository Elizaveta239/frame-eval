import threading

from debugger.pydev_file_utils import get_abs_path_real_path_and_base_from_frame, NORM_PATHS_AND_BASE_CONTAINER
from debugger.pydev_modify_bytecode import insert_code
from debugger.pydev_debugger import get_global_debugger, ignore_list, trace_wrapper, update_globals_dict
import dis

NO_BREAKS_IN_FRAME = 1


class PyDBAdditionalThreadInfo(object):
    def __init__(self):
        self.pydev_state = 1
        self.is_tracing = False


class UseCodeExtraHolder:
    # Use this flag in order to disable co_extra field
    use_code_extra = True
    # Keep the index of co_extra in a thread-local storage
    local = threading.local()
    local.index = -1


def is_use_code_extra():
    return UseCodeExtraHolder.use_code_extra

def set_use_code_extra(new_value):
    UseCodeExtraHolder.use_code_extra = new_value

cdef PyObject*get_bytecode_while_frame_eval(PyFrameObject *frame_obj, int exc):
    frame = <object> frame_obj
    cdef str filepath = frame.f_code.co_filename
    cdef bint skip_file = exc
    cdef void*extra = NULL
    cdef int*extra_value = NULL
    cdef int thread_index = -1

    if skip_file or is_use_code_extra is None or ignore_list is None:
        # Sometimes during process shutdown these global variables become None
        return _PyEval_EvalFrameDefault(frame_obj, exc)

    if is_use_code_extra():
        # Skip frames without breakpoints quickly
        extra = PyMem_Malloc(sizeof(int))
        try:
            thread_index = UseCodeExtraHolder.local.index
        except:
            pass
        if thread_index != -1:
            _PyCode_GetExtra(<PyObject*> frame.f_code, thread_index, &extra)
            if extra is not NULL:
                extra_value = <int*> extra
                if extra_value[0] == NO_BREAKS_IN_FRAME:
                    return _PyEval_EvalFrameDefault(frame_obj, exc)

    for file in ignore_list:
        # we can't call any other function without this check, because we can get stack overflow
        for path_separator in ('/', '\\'):
            if filepath.endswith(path_separator + file):
                skip_file = True
                break

    if not skip_file:
        try:
            t = threading.currentThread()
        except:
            skip_file = True

    if not skip_file:
        try:
            additional_info = t.additional_info
            if additional_info is None:
                raise AttributeError()
        except:
            additional_info = t.additional_info = PyDBAdditionalThreadInfo()
            # request `co_extra` inside every new thread
            thread_index = _PyEval_RequestCodeExtraIndex(PyMem_Free)
            UseCodeExtraHolder.local.index = thread_index

        if additional_info.is_tracing:
            return _PyEval_EvalFrameDefault(frame_obj, exc)

        additional_info.is_tracing = True
        try:
            abs_path_real_path_and_base = NORM_PATHS_AND_BASE_CONTAINER[frame.f_code.co_filename]
        except:
            abs_path_real_path_and_base = get_abs_path_real_path_and_base_from_frame(frame)

        was_break = False
        debugger = get_global_debugger()
        breakpoints = debugger.get_breakpoints_for_file(abs_path_real_path_and_base[1])
        code_object = frame.f_code
        if breakpoints:
            for offset, line in dis.findlinestarts(<object> code_object):
                if line in breakpoints:
                    success, new_code = insert_code(<object> code_object, trace_wrapper.__code__, line)
                    if success:
                        Py_INCREF(new_code)
                        frame_obj.f_code = <PyCodeObject *> new_code
                        was_break = True

            if was_break:
                update_globals_dict(<object> frame.f_globals)

        if not was_break:
            extra_value = <int*> PyMem_Malloc(sizeof(int))
            extra_value[0] = NO_BREAKS_IN_FRAME
            try:
                thread_index = UseCodeExtraHolder.local.index
            except:
                pass
            if thread_index != -1:
                _PyCode_SetExtra(<PyObject*> code_object, thread_index, extra_value)

        additional_info.is_tracing = False

    return _PyEval_EvalFrameDefault(frame_obj, exc)

def main():
    cdef PyThreadState *state = PyThreadState_Get()
    state.interp.eval_frame = get_bytecode_while_frame_eval

def stop_frame_eval():
    cdef PyThreadState *state = PyThreadState_Get()
    state.interp.eval_frame = _PyEval_EvalFrameDefault
