# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from difflib import Differ

import preprocessor
from preprocessor import get_file_contents
from transpiler import Transpiler
import subprocess


def jackup(filename, output_file):
    program = get_file_contents(filename)
    transpiler = Transpiler(program)
    transpiler.parse_directives([])
    transpiler.cleanup_all(True)
    transpiler.optimize_variables()
    transpiler.finalize(0, 1)
    program = transpiler.program
    f = open(output_file, 'w')
    f.write(program)
    f.close()
    print(program)
    subprocess.run("pbcopy", universal_newlines=True, input=program + 'run\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    jackup('klondike.txt', 'klondike_output.txt')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
