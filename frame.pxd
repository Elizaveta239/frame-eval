cdef extern from *:
    ctypedef void PyObject

cdef extern from "frameobject.h":
    ctypedef struct PyFrameObject:
        pass

cdef extern from "pystate.h":
    ctypedef object (*_PyFrameEvalFunction)(PyFrameObject *frame, int exc)

    ctypedef struct PyInterpreterState:
        PyInterpreterState *next
        PyInterpreterState *tstate_head

        PyObject *modules

        PyObject *modules_by_index
        PyObject *sysdict
        PyObject *builtins
        PyObject *importlib

        PyObject *codec_search_path
        PyObject *codec_search_cache
        PyObject *codec_error_registry
        int codecs_initialized
        int fscodec_initialized

        int dlopenflags

        PyObject *builtins_copy
        PyObject *import_func
        # Initialized to PyEval_EvalFrameDefault().
        _PyFrameEvalFunction eval_frame

    ctypedef struct PyThreadState:
        PyThreadState *prev
        PyThreadState *next
        PyInterpreterState *interp
        # ...

    PyThreadState *PyThreadState_Get()

cdef extern from "ceval.h":
    PyFrameObject *PyEval_GetFrame()

    PyObject *_PyEval_EvalFrameDefault(PyFrameObject *frame, int exc)
