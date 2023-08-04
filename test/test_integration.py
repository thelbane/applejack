import inspect
import unittest

import preprocessor
import transpiler


class TestIntegration(unittest.TestCase):

    def test_include_rename(self):
        folders = ["test_files"]
        program = """
REM ** TEST
#INCLUDE "firstLastName.txt"
print LAST_NAME;", ";FIRST_NAME
"""
        expected = """
REM ** TEST


f$ = 'Steve'
l$ = 'Wozniak'
print l$;", ";f$
"""
        actual = preprocessor.parse(program, folders)
        actual = transpiler.rename_identifier(actual, 'lastName$', 'l$')
        actual = transpiler.rename_identifier(actual, 'firstName$', 'f$')
        self.assertEqual(expected, actual)

    def test_subroutines(self):
        folders = ["test_files"]
        program = """
REM ** TEST
#INCLUDE "subroutines.txt"

gosub .printStats
"""
        expected = """10REM ** TEST
20print "Your name is: "; n$
30return
40print "Strength: "; st
50return
60gosub 20
70gosub 40
80return
90gosub 60
"""
        actual = preprocessor.parse(program, folders)
        actual = transpiler.rename_identifier(actual, 'name$', 'n$')
        actual = transpiler.resolve_labels(actual)
        actual = transpiler.rename_identifier(actual, 'strength$', 'st')
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
