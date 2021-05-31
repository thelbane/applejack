import re
from os.path import exists, join

directive_re = re.compile(r'^ *#([a-z]+)(( +.*)?)$', re.I | re.M)
include_params_re = re.compile(r'^"([^"]*)"$', re.I)

# 1: full key, 4: params, 8: value
define_params_re = re.compile(r'^(([a-z_][a-z0-9_]*)(\( *(([a-z_][a-z0-9_]*) *(, *([a-z_][a-z0-9_]*) *)*)\))?)(( .*)?)$', re.I)

# 1: base_key, 3: params
define_key_re = re.compile(r'^([a-z_][a-z0-9_]*)(\(([^,)]+(,[^,)]+)*)\))?$', re.I)


def parse(program, folders, defines=None):
    preprocessor = Preprocessor(folders, defines)
    return preprocessor.parse(program)


class Preprocessor:

    def __init__(self, folders=None, defines=None):
        self.folders = folders or []
        self.defines = defines or {}
        self.define_keys = []
        self.filepaths = []

    def parse(self, program, filepath=None):
        self.filepaths.append(filepath)
        while True:
            match = directive_re.search(program)
            if match:
                directive = match.group(1).lower().strip()
                parameters = match.group(2).strip()
                sub = ''
                if directive == 'include':
                    sub = self.parse_include(parameters)
                if directive == 'define':
                    sub = self.parse_define(parameters)
                program = directive_re.sub(sub, program, 1)
            else:
                break
        self.filepaths.pop()
        program = self.substitute_defines(program)
        return program

    def parse_include(self, parameters):
        match = include_params_re.search(parameters)
        if match is None:
            raise Exception()
        filename = match.group(1)
        filepath = get_filepath(filename, self.folders)
        if filepath is None:
            raise Exception(f'Include file not found ({filename})')
        if filepath in self.filepaths:
            raise Exception(f'Circular include reference detected ({filepath})')
        return self.parse(get_file_contents(filepath), filepath)

    def parse_define(self, parameters):
        match = define_params_re.search(parameters)
        if match is None:
            raise Exception()
        key = match.group(1)
        base_key = match.group(2)
        if base_key in self.define_keys:
            raise Exception(f'Duplicate define found ({base_key})')
        self.define_keys.append(base_key)
        value = match.group(8).strip()
        self.defines[key] = value
        return ''

    def substitute_defines(self, program):
        while True:
            finished = True
            for key in self.defines:
                match = define_key_re.search(key)
                if match is None:
                    raise Exception()
                base_key = match.group(1)
                params = get_macro_params(match.group(3))
                value = self.defines[key]
                if len(params) == 0:
                    key_re = re.compile(f'\\b{key}\\b(?=(?:[^"]*"[^"]*")*[^"]*$)', re.M)
                    if key_re.search(program):
                        finished = False
                    program = key_re.sub(value, program, 0)
                else:
                    site_re = re.compile(f'{base_key}\\(([^)]*)\\)', re.M)
                    while True:
                        match = site_re.search(program)
                        if match is None:
                            break
                        finished = False
                        subs = get_macro_params(match.group(1))
                        if len(subs) != len(params):
                            raise Exception(f'Parameter count mismatch: {match.group(0)}')
                        new_value = value
                        for i in range(len(params)):
                            param = params[i]
                            sub = subs[i]
                            new_value = re.sub(f'\\b{param}\\b', sub, new_value, 0)
                        program = site_re.sub(new_value, program, 1)
            if finished:
                break
        return program


def get_file_contents(filepath):
    file = open(filepath, 'r')
    contents = file.read()
    file.close()
    return contents


def get_filepath(filename, folders):
    if exists(filename):
        return filename
    for folder in folders:
        filepath = join(folder, filename)
        if exists(filepath):
            return filepath
    return None


def get_macro_params(params):
    if params is None:
        return []
    return [s.strip() for s in params.split(',')]


def string_contains_term(string_value, term):
    return re.search(f'\\b{term}\\b', string_value) is not None
