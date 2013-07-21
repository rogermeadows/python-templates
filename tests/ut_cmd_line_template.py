#!/usr/bin/env python
# File: unit_test_template.py

import unittest
import sys
import os
import subprocess
from pexpect import run
import six

sys.path.append(os.path.dirname(os.getcwd()))

from cmd_line_template import main as cmd_main

class TestCommandLineTemplate(unittest.TestCase):

    def test_call_with_help(self):
        result1 = run('python ../cmd_line_template.py --help')
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = collect_stdout = six.StringIO()
        sys.stderr = collect_stderr = six.StringIO()
        result2 = cmd_main(['cmd_line_template.py', '--help'])
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        std_output = collect_stdout.getvalue()
        std_error = collect_stderr.getvalue()
        self.assertEqual(result1, std_output)



if __name__ == '__main__':
    unittest.main()

