import inspect
import unittest


class TestRename(unittest.TestCase):

    def test_find_all_identifiers(self):
        program = inspect.cleandoc("""
            10 PRINT a$; : REM Hello friend
            20 TEXT: HOME
            30 DIM AB$(100),x(10),y(10): goto 10
            40 HPLOT x, y
            50 FORQQ=XXTOYYSTEPZZ
            60 Q1 = 5
            """)
        expected = {'A$', 'AB$', 'X', 'Y', 'QQ', 'XX', 'YY', 'ZZ', 'Q1'}
        from transpiler import Transpiler
        transpiler = Transpiler(program)
        actual = transpiler.find_identifiers()
        self.assertEqual(expected, actual)

    def test_rename_all_identifiers(self):
        program = inspect.cleandoc("""
            10 PRINT a$; : REM Hello friend
            20 TEXT: HOME
            30 DIM AB$(100),x(10),y(10): goto 10
            40 HPLOT x, y
            50 FORQQ=XXTOYYSTEPZZ
            """)
        expected = inspect.cleandoc("""
            10 PRINT XXX; : REM Hello friend
            20 TEXT: HOME
            30 DIM XXX(100),XXX(10),XXX(10): goto 10
            40 HPLOT XXX, XXX
            50 FORXXX=XXXTOXXXSTEPXXX
            """)
        from transpiler import rename_all_identifiers
        actual = rename_all_identifiers(program, 'XXX')
        self.assertEqual(expected, actual)

    def test_rename_containing_short_identifier(self):
        program = inspect.cleandoc("""
            10 PRINT a$; : REM Hello friend
            20 TEXT: HOME
            30 DIM AB$(100),x(10),y(10): goto 10
            40 HPLOT x, y
            50 FORQQ=XXTOYYSTEPZZ
            """)
        from transpiler import Transpiler
        transpiler = Transpiler(program)
        transpiler.rename_identifier('X', 'XXX')
        self.assertEqual(inspect.cleandoc("""
                         10 PRINT a$; : REM Hello friend
                         20 TEXT: HOME
                         30 DIM AB$(100),XXX(10),y(10): goto 10
                         40 HPLOT XXX, y
                         50 FORQQ=XXTOYYSTEPZZ
                         """),
                         transpiler.program
                         )
        transpiler.rename_identifier('ZZ', 'XXX')
        self.assertEqual(inspect.cleandoc("""
                         10 PRINT a$; : REM Hello friend
                         20 TEXT: HOME
                         30 DIM AB$(100),XXX(10),y(10): goto 10
                         40 HPLOT XXX, y
                         50 FORQQ=XXTOYYSTEPXXX
                         """),
                         transpiler.program
                         )
        transpiler.rename_identifier('YY', 'XXX')
        self.assertEqual(inspect.cleandoc("""
                         10 PRINT a$; : REM Hello friend
                         20 TEXT: HOME
                         30 DIM AB$(100),XXX(10),y(10): goto 10
                         40 HPLOT XXX, y
                         50 FORQQ=XXTOXXXSTEPXXX
                         """),
                         transpiler.program
                         )

    def test_rename_identifier(self):
        program = inspect.cleandoc("""
            10 PRINTXXXX$XX$
            20 PRINTXX$XXXX$
            """)
        expected = inspect.cleandoc("""
            10 PRINTA$XX$
            20 PRINTXX$A$
            """)
        from transpiler import rename_identifier
        actual = rename_identifier(program, 'XXXX$', 'A$')
        self.assertEqual(expected, actual)

    def test_rename_with_labels(self):
        program = inspect.cleandoc("""
            .XXXX PRINTXXXX$XX$
            .XXXX$ PRINTXX$XXXX$
            """)
        expected = inspect.cleandoc("""
            .XXXX PRINTA$XX$
            .XXXX$ PRINTXX$A$
            """)
        from transpiler import rename_identifier
        actual = rename_identifier(program, 'XXXX$', 'A$')
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
