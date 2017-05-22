import unittest
from io import StringIO

from debugger.pydev_modify_bytecode import insert_code
import sys

TRACE_MESSAGE = "Trace called"


class TestDebugger(object):
    def call_trace(self):
        print(TRACE_MESSAGE)


debugger = TestDebugger()


def tracing():
    debugger.call_trace()


class TestInsertCode(unittest.TestCase):
    def check_insert_every_line(self, func_to_modify, func_to_insert, number_of_lines):
        first_line = func_to_modify.__code__.co_firstlineno + 1
        last_line = first_line + number_of_lines
        for i in range(first_line, last_line):
            self.check_insert_to_line(func_to_modify, func_to_insert, i)

    def check_insert_to_line(self, func_to_modify, func_to_insert, line_number):
        code_orig = func_to_modify.__code__
        code_to_insert = func_to_insert.__code__
        success, result = insert_code(code_orig, code_to_insert, line_number)
        assert success, "Bytecode modification failed"
        exec(result)
        output = sys.stdout.getvalue().strip()
        self.assertTrue(TRACE_MESSAGE in output)

    def test_assignment(self):
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            def original():
                a = 1
                b = 2
                c = 3

            self.check_insert_every_line(original, tracing, 3)

        finally:
            sys.stdout = self.original_stdout

    def test_for_loop(self):
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            def original():
                n = 3
                sum = 0
                for i in range(n):
                    sum += i
                return sum

            self.check_insert_every_line(original, tracing, 5)

        finally:
            sys.stdout = self.original_stdout

    def test_if_else(self):
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            def original():
                if True:
                    a = 1
                else:
                    a = 0
                print(a)

            self.check_insert_to_line(original, tracing, original.__code__.co_firstlineno + 2)
            self.check_insert_to_line(original, tracing, original.__code__.co_firstlineno + 5)

        finally:
            sys.stdout = self.original_stdout
