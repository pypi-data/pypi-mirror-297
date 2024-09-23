# tests/test_info.py
import unittest
from module_python.info import display_info

class TestInfoModule(unittest.TestCase):

    def test_display_info(self):
        # Capture the print output
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        display_info()
        sys.stdout = sys.__stdout__

        # Check if the output contains the expected strings
        self.assertIn("Roll Number: 123456", captured_output.getvalue())
        self.assertIn("Name: Himanshu Kumar Jha", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()
