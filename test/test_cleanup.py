import unittest

from transpiler import Transpiler


class TestCleanup(unittest.TestCase):

    def test_remove_full_comment(self):
        program = """
REM This should go away
REM ...and this too
"""
        expected = """


"""
        transpiler = Transpiler(program)
        transpiler.cleanup_comments()
        actual = transpiler.program
        self.assertEqual(expected, actual)

    def test_remove_partial_comment(self):
        program = """
GOTO .end: REM This should go away
REM ...and this too
.end
"""
        expected = """
GOTO .end: 

.end
"""
        transpiler = Transpiler(program)
        transpiler.cleanup_comments()
        actual = transpiler.program
        self.assertEqual(expected, actual)

    def test_leave_quoted_rem(self):
        program = """
print "REM test"
"""
        expected = """
print "REM test"
"""
        transpiler = Transpiler(program)
        transpiler.cleanup_comments()
        actual = transpiler.program
        self.assertEqual(expected, actual)

    def test_cleanup_goto(self):
        program = """
GOTO .end: PRINT "hello"
ON x GOTO .label1, .label2, .label13: print "goodbye"
PRINT "goto 10": REM Test
.end
.label1
.label2
.label3
"""
        expected = """
GOTO .end
ON x GOTO .label1, .label2, .label13
PRINT "goto 10": REM Test
.end
.label1
.label2
.label3
"""
        transpiler = Transpiler(program)
        transpiler.cleanup_goto()
        actual = transpiler.program
        self.assertEqual(expected, actual)

    def test_cleanup_end(self):
        program = """
END : GOTO .foo
PRINT "end : GOTO .foo"
END it all
"""
        expected = """
END
PRINT "end : GOTO .foo"
END
"""
        transpiler = Transpiler(program)
        transpiler.cleanup_end()
        actual = transpiler.program
        self.assertEqual(expected, actual)

    def test_cleanup_trailing_colons(self):
        program = """
print "test";:
home :
text : home ::
"""
        expected = """
print "test";
home
text : home
"""
        transpiler = Transpiler(program)
        transpiler.cleanup_trailing_colons()
        actual = transpiler.program
        self.assertEqual(expected, actual)

    def test_collapse_whitespace(self):
        program = """
 TEXT : HOME : REM *** test ***
"""
        expected = """TEXT:HOME:REM *** test ***
"""
        transpiler = Transpiler(program)
        transpiler.collapse_whitespace()
        actual = transpiler.program
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
