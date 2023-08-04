import unittest
import preprocessor


class TestPreprocessorIncludes(unittest.TestCase):

    def test_no_include(self):
        folders = ["test/test_files"]
        program = """
print
"""
        expected = program
        actual = preprocessor.parse(program, folders)
        self.assertEqual(expected, actual)

    def test_include(self):
        folders = ["test_files"]
        program = """
#include "simple.txt"
"""
        expected = """
print "simple.txt: Line 1"
print "simple.txt: Line 2"
"""
        actual = preprocessor.parse(program, folders)
        self.assertEqual(expected, actual)

    def test_include_twice(self):
        folders = ["test_files"]
        program = """
#include "simple.txt"
#include "simple.txt"
"""
        expected = """
print "simple.txt: Line 1"
print "simple.txt: Line 2"
print "simple.txt: Line 1"
print "simple.txt: Line 2"
"""
        actual = preprocessor.parse(program, folders)
        self.assertEqual(expected, actual)

    def test_nested_includes(self):
        folders = ["test_files"]
        program = """
#include "nested_include.txt"
"""
        expected = """
print "nested_include.txt: Line 1"
print "include.txt: Line 1"
print "simple.txt: Line 1"
print "simple.txt: Line 2"
print "include.txt: Line 2"
print "nested_include.txt: Line 2"
"""
        actual = preprocessor.parse(program, folders)
        self.assertEqual(expected, actual)

    def test_file_not_found(self):
        folders = ["test/test_files"]
        program = """
#include "bad_file.txt"
"""
        with self.assertRaises(Exception) as context:
            preprocessor.parse(program, folders)

        expected = 'Include file not found (bad_file.txt)'
        actual = str(context.exception)

        self.assertEqual(expected, actual)

    def test_circular_reference(self):
        folders = ["test_files"]
        program = """
#include "circular_a_include.txt"
"""
        with self.assertRaises(Exception) as context:
            preprocessor.parse(program, folders)

        expected = 'Circular include reference detected (test_files/circular_a_include.txt)'
        actual = str(context.exception)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
