import unittest
import transpiler


class TestResolveLabels(unittest.TestCase):

    def test_no_labels(self):
        program = """
home
"""
        expected = """10home
"""
        actual = transpiler.resolve_labels(program)
        self.assertEqual(expected, actual)

    def test_remove_labels(self):
        program = """
.start home
.end end
"""
        expected = """10home
20end
"""
        actual = transpiler.resolve_labels(program)
        self.assertEqual(expected, actual)

    def test_custom_line_numbers(self):
        program = """
.start home
print"hello world"
.end end
"""
        expected = """0home
1print"hello world"
2end
"""
        actual = transpiler.resolve_labels(program, 0, 1)
        self.assertEqual(expected, actual)

    def test_substitute_labels(self):
        program = """
.start home
.end goto .start
"""
        expected = """10home
20goto 10
"""
        actual = transpiler.resolve_labels(program)
        self.assertEqual(expected, actual)

    def test_on_gosub(self):
        program = """
on x gosub .routine1, .routine2, .routine3
.routine1
home
.routine2
text
.routine3
hgr2
"""
        expected = """10on x gosub 20, 30, 40
20home
30text
40hgr2
"""
        actual = transpiler.resolve_labels(program)
        self.assertEqual(expected, actual)

    def test_piled_labels(self):
        program = """
.start
.beginning
.other
    home
    goto .start
    goto .beginning
    goto .other
"""
        expected = """10home
20goto 10
30goto 10
40goto 10
"""
        actual = transpiler.resolve_labels(program)
        self.assertEqual(expected, actual)

    def test_unexpected_line_number(self):
        program = """
10 HOME
"""
        with self.assertRaises(Exception) as context:
            transpiler.resolve_labels(program)

        expected = 'Unexpected line number found: 10 HOME'
        actual = str(context.exception)
        self.assertEqual(expected, actual)

    def test_duplicate_labels(self):
        program = """
.start HOME
PRINT"HELLO"
.start END
"""
        with self.assertRaises(Exception) as context:
            transpiler.resolve_labels(program)

        expected = 'Duplicate label found (.start)'
        actual = str(context.exception)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
