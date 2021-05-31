import unittest

from transpiler import Transpiler


class TestCleanup(unittest.TestCase):

    def test_remove_full_comment(self):
        program = """
REM This should go away
rem ...and this too
"""
        expected = """


"""
        transpiler = Transpiler(program)
        transpiler.cleanup_comments()
        actual = transpiler.program
        self.assertEqual(expected, actual)

    def test_remove_partial_comment(self):
        program = """
goto .end: REM This should go away
rem ...and this too
.end
"""
        expected = """
goto .end: 

.end
"""
        transpiler = Transpiler(program)
        transpiler.cleanup_comments()
        actual = transpiler.program
        self.assertEqual(expected, actual)

    def test_leave_quoted_rem(self):
        program = """
print "rem test"
"""
        expected = """
print "rem test"
"""
        transpiler = Transpiler(program)
        transpiler.cleanup_comments()
        actual = transpiler.program
        self.assertEqual(expected, actual)

    def test_cleanup_goto(self):
        program = """
goto .end: print "hello"
on x goto .label1, .label2, .label13: print "goodbye"
print "goto 10": rem Test
.end
.label1
.label2
.label3
"""
        expected = """
goto .end
on x goto .label1, .label2, .label13
print "goto 10": rem Test
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
end : goto .foo
print "end : goto .foo"
end it all
"""
        expected = """
end
print "end : goto .foo"
end
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
 text : home : rem *** test ***
"""
        expected = """text:home:rem *** test ***
"""
        transpiler = Transpiler(program)
        transpiler.collapse_whitespace()
        actual = transpiler.program
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
