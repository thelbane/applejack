import unittest
import preprocessor


class TestPreprocessorDefines(unittest.TestCase):

    def test_no_define(self):
        folders = ["test/test_files"]
        program = """
print
"""
        expected = program
        actual = preprocessor.parse(program, folders)
        self.assertEqual(expected, actual)

    def test_simple_define(self):
        folders = ["test/test_files"]
        program = """
#define x
"""
        expected = """

"""
        actual = preprocessor.parse(program, folders)
        self.assertEqual(expected, actual)

    def test_value_substitution(self):
        folders = ["test/test_files"]
        program = """
#define prt_hello print "hello"
prt_hello
prt_hello
"""
        expected = """

print "hello"
print "hello"
"""
        actual = preprocessor.parse(program, folders)
        self.assertEqual(expected, actual)

    def test_preconfigured_defines(self):
        folders = ["test/test_files"]
        program = """
SET_X
"""
        expected = """
X=INT(RND(1) * 10)
"""
        defines = {
            "SET_X": "X=INT(RND(1) * 10)"
        }
        actual = preprocessor.parse(program, folders, defines)
        self.assertEqual(expected, actual)

    def test_single_substitution(self):
        folders = ["test/test_files"]
        program = """
#define prt(x) print x
home:prt("hi there")
"""
        expected = """

home:print "hi there"
"""
        actual = preprocessor.parse(program, folders)
        self.assertEqual(expected, actual)

    def test_multiple_substitution(self):
        folders = ["test/test_files"]
        program = """
#define random(base, range) (int(rnd(1)*range)+base)
x = random(0,5)-random(1,1)
y = random( 10, 100 )
"""
        expected = """

x = (int(rnd(1)*5)+0)-(int(rnd(1)*1)+1)
y = (int(rnd(1)*100)+10)
"""
        actual = preprocessor.parse(program, folders)
        self.assertEqual(expected, actual)

    def test_multiple_passes(self):
        folders = ["test/test_files"]
        program = """
#DEFINE ONE 1
#DEFINE INITIALS ONE
#DEFINE DISPLAY_NAME(LAST, FIRST) FIRST + " " + LEFT$(LAST,INITIALS) + "."
#DEFINE SHOW_NAME(LAST, FIRST) PRINT DISPLAY_NAME(LAST, FIRST)
D$ = DISPLAY_NAME(A$, B$)
SHOW_NAME(L$,F$)
"""
        expected = """




D$ = B$ + " " + LEFT$(A$,1) + "."
PRINT F$ + " " + LEFT$(L$,1) + "."
"""
        actual = preprocessor.parse(program, folders)
        self.assertEqual(expected, actual)

    def test_parameter_count_mismatch(self):
        folders = ["test/test_files"]
        program = """
#define random(a,b) a=(rnd(1)*b)
random(n,3,0)
"""
        with self.assertRaises(Exception) as context:
            preprocessor.parse(program, folders)

        expected = 'Parameter count mismatch: random(n,3,0)'
        actual = str(context.exception)
        self.assertEqual(expected, actual)

    def test_redefinition(self):
        folders = ["test/test_files"]
        program = """
#DEFINE FATAL(STR) LOG("ERR: " + STR) : STOP
#DEFINE LOG(STR) LOG$ = STR : GOSUB .log
#DEFINE LOG LG
LOG("Hello")
FATAL("Hello")
.log
    PRINT LG$
    RETURN
"""
        with self.assertRaises(Exception) as context:
            preprocessor.parse(program, folders)

        expected = 'Duplicate define found (LOG)'
        actual = str(context.exception)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
