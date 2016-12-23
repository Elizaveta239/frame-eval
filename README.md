PEP 523 Experiments
===================

An experimental debugger for using new frame evaluation API.

Use `python setup.py build_ext --inplace` to compile`frame` module inside the
project directory.

The most important performance compare is in the `performance_compare/main_test.py`

Example of usage (from `main.py`):

```
from debugger.pydev_debug_info import FrameDebugger
import os

filename = os.path.abspath(__file__)

debugger = FrameDebugger()
debugger.add_breakpoint(filename, 14)
debugger.run()


def foo():
    a = 1
    b = 2
    c = 3
    return a + b + c


foo()
```

In the initial realization debugger shows file, line number and values of local variables. For example, after running
the file `main.py` the output will be:

`<path>/frame-eval/main.py 14 {'b': 2, 'a': 1}`

