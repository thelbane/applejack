import random
import re
import sys
from difflib import Differ

from preprocessor import Preprocessor

label_pattern = r'\.[a-z_][a-z0-9_]*'

label_re = re.compile(f"^{label_pattern}", re.I)
line_number_re = re.compile(r'^[\d][\d ]*')
trailing_keywords_re = re.compile(r'(then|goto|end)(?=[^"]*(?:"[^"]*"[^"]*)*$)', re.I)
delimiter_re = re.compile(r':(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)')

string_literal_pattern = r'\"(?:[^\"])*\"'

quote_lookahead_pattern = r'(?=(?:[^"]*"[^"]*")*[^"]*$)'

remark_pattern = r'REM.*$'

keyword_pattern = r'READ|IF|AND|OR|NOT|THEN|FOR|TO|NEXT|GOTO|GOSUB|RETURN|VTAB|HTAB|TEXT|HOME|INT|RND|CHR|STR\$|INPUT' \
                  r'|MID|PEEK|POKE|CALL|NORMAL|INVERSE|FLASH|PRINT|DIM|HPLOT|STEP|END|RUN|SGN|STOP|LOG|SIN|COS|LEN|GET'

string_int_identifier_pattern = r'(?:[a-z_][a-z0-9_]*?[$%])'

string_int_identifier_re = re.compile(string_int_identifier_pattern, re.I | re.M)

float_identifier_prefix = r'(?:[a-z_][a-z0-9_]*?)'

float_identifier_suffix = f'(?={keyword_pattern}|[^a-z0-9_%$]|$)'

float_identifier_pattern = f'{float_identifier_prefix}{float_identifier_suffix}'

non_identifier_pattern = f'{label_pattern}|{string_literal_pattern}|{remark_pattern}|{keyword_pattern}'

any_identifier_pattern = f'({string_int_identifier_pattern}|{float_identifier_pattern})'

all_identifiers_pattern = f'(?:{non_identifier_pattern})|{any_identifier_pattern}'

all_identifiers_re = re.compile(all_identifiers_pattern, re.I | re.M)

# CLEANUP REGEX

keyword_prefix = r'(?:(?:THEN|[^a-z]) *)'

trailing_colons_re = re.compile(f'[: ]*$', re.I | re.M)

rem_to_end_re = re.compile(f'REM{quote_lookahead_pattern}.*$', re.I | re.M)

next_colon_to_end_pattern = f'{quote_lookahead_pattern}[^:\v]*([.\v]*$)'

goto_cleanup_pattern = f'(?:THEN|\\W)GOTO{quote_lookahead_pattern}[.A-Z0-9,_ ]*(.*)$'

goto_cleanup_re = re.compile(goto_cleanup_pattern, re.I | re.M)

end_cleanup_pattern = f'(?:THEN|\\W)END{quote_lookahead_pattern}(.*)$'

end_cleanup_re = re.compile(end_cleanup_pattern, re.I | re.M)

whitespace_re = re.compile(r'"[^"\v]*"|REM[^\v]*|([ \t]+|^\s*)', re.I | re.M)


def resolve_labels(program, start=10, stride=10):
    transpiler = Transpiler(program)
    transpiler.resolve_labels(start, stride)
    return transpiler.program


def rename_all_identifiers(program, new_name):
    transpiler = Transpiler(program)
    identifiers = list(transpiler.find_identifiers())
    for identifier in identifiers:
        transpiler.rename_identifier(identifier, new_name)
    return transpiler.program


def reflow(program):
    transpiler = Transpiler(program)
    transpiler.reflow()
    return transpiler.program


def rename_identifier(program, old, new):
    transpiler = Transpiler(program)
    transpiler.rename_identifier(old, new)
    return transpiler.program


class Transpiler:

    def __init__(self, program):
        self.program = program

    def parse_directives(self, folders, defines=None):
        preprocessor = Preprocessor(folders, defines)
        self.program = preprocessor.parse(self.program)

    def cleanup_all(self, remove_comments):
        if remove_comments:
            self.cleanup_comments()
        self.cleanup_goto()
        self.cleanup_end()
        self.cleanup_trailing_colons()
        self.collapse_whitespace()
        self.explode()

    def explode(self):
        foo = re.compile('(^(?:(?!REM|GOTO|END|IF|RETURN|STOP).)*?)(:(?=(?:[^"]*"[^"]*")*[^"]*$))', re.I | re.M)
        while True:
            match = foo.search(self.program)
            if match:
                self.program = foo.sub(f'{match.group(1)}\n', self.program, 1)
            else:
                break

    def collapse_whitespace(self):
        self.replace_group(whitespace_re.finditer(self.program), 1, '')

    def cleanup_trailing_colons(self):
        self.program = trailing_colons_re.sub('', self.program)

    def cleanup_end(self):
        self.replace_group(end_cleanup_re.finditer(self.program), 1, '')

    def cleanup_goto(self):
        self.replace_group(goto_cleanup_re.finditer(self.program), 1, '')

    def cleanup_comments(self):
        self.program = rem_to_end_re.sub('', self.program)

    def rename_identifier(self, old, new):
        old = old.upper()
        identifiers = self.find_identifiers()
        other_identifier_pattern = ''
        if old in identifiers:
            identifiers.remove(old)
        else:
            raise (Exception(f'Identifier not found: {old}'))
        identifiers = list(filter(lambda x: len(x) >= len(old), identifiers))
        identifiers.sort(key=len, reverse=True)
        if len(identifiers):
            other_identifier_pattern = '|' + '|'.join([re.escape(i) for i in identifiers])
        pattern = f'(?:{non_identifier_pattern}{other_identifier_pattern})|({re.escape(old)})'
        if not string_int_identifier_re.search(old):
            pattern += float_identifier_suffix
        magic = re.compile(pattern, re.I | re.M)
        self.replace_group(magic.finditer(self.program), 1, new)

    def replace_group(self, matches, group_num, sub):
        offset = 0
        for match in matches:
            group = match.group(group_num)
            if group:
                self.program = self.program[:match.start(group_num) + offset] + sub + self.program[
                                                                                      match.end(group_num) + offset:]
                offset = offset + len(sub) - len(group)

    def find_identifiers(self):
        result = set()
        for match in all_identifiers_re.finditer(self.program):
            identifier = match.group(1)
            if identifier:
                result.add(identifier.upper())
        return result

    def resolve_labels(self, start=10, stride=10):
        line_number = start
        lines_by_label = {}
        result = ''
        for line in self.program.splitlines():
            line = line.strip()
            if line_number_re.search(line):
                raise Exception(f'Unexpected line number found: {line}')
            match = label_re.search(line)
            if match is not None:
                label = match.group(0)
                if label in lines_by_label:
                    raise Exception(f'Duplicate label found ({label})')
                lines_by_label[label] = line_number
                line = label_re.sub('', line).strip()
                pass
            if line == '':
                continue
            result += f'{line_number}{line}\n'
            line_number += stride
        for label in lines_by_label:
            line_num = f'{lines_by_label[label]}'
            re_str = f'\\{label}\\b(?=(?:[^"]*"[^"]*")*[^"]*$)'
            result = re.sub(re_str, line_num, result, 0)
        self.program = result

    def finalize(self, start=10, stride=10):
        line_number = start
        lines_by_label = {}
        result = []
        current_line = ''

        def append(new, is_labeled=False):
            nonlocal line_number, current_line
            if is_labeled:
                if len(current_line) > 0:
                    result.append(f'{line_number}{current_line}')
                    line_number += stride
                current_line = new
            else:
                line_len = self.getLen(current_line + new) + 1 + len(f'{line_number}')
                if line_len < 240:
                    # length okay, add colon and append to current line
                    if len(current_line) > 0:
                        current_line += ':'
                    current_line += new
                elif line_len >= 240:
                    # too long, store current line, increment line number, and start new line
                    # OR
                    # new content is not appendable, store current line, increment line number, and start new line
                    result.append(f'{line_number}{current_line}')
                    line_number += stride
                    current_line = new

            if re.search('^(REM|GOTO|END|IF|RETURN|STOP)', new, re.I):
                result.append(f'{line_number}{current_line}')
                line_number += stride
                current_line = ''

        for line in self.program.splitlines():
            line = line.strip()
            if line_number_re.search(line):
                raise Exception(f'Unexpected line number found: {line}')
            match = label_re.search(line)
            if match is not None:
                label = match.group(0)
                if label in lines_by_label:
                    raise Exception(f'Duplicate label found ({label})')
                line = label_re.sub('', line).strip()
                append(line, True)
                lines_by_label[label] = line_number
                continue
            if line == '':
                continue
            append(line)

        result = '\n'.join(result)
        for label in lines_by_label:
            line_num = f'{lines_by_label[label]}'
            re_str = f'\\{label}\\b(?=(?:[^"]*"[^"]*")*[^"]*$)'
            result = re.sub(re_str, line_num, result, 0)
        self.program = result + '\n'

    def getLen(self, line):
        adjust = 0
        for result in re.findall(label_pattern, line, re.I):
            adjust = adjust - len(result) + 5
        return len(line) + adjust

    def diff(self, action, diff_only=False):
        before = self.program.splitlines(keepends=True)
        action()
        after = self.program.splitlines(keepends=True)
        d = Differ()
        if diff_only:
            diff = filter(lambda x: x[0] != ' ', list(d.compare(before, after)))
        else:
            diff = list(d.compare(before, after))
        sys.stdout.writelines(diff)

    def optimize_variables(self):
        identifiers = self.find_identifiers()
        for identifier in identifiers:
            self.rename_identifier(identifier, f"__{identifier}")

        float_count = 0
        int_count = 0
        string_count = 0
        for identifier in identifiers:
            if identifier[-1] == '$':
                new = Transpiler.get_identifier(string_count) + '$'
                string_count += 1
            elif identifier[-1] == '%':
                new = Transpiler.get_identifier(int_count) + '%'
                int_count += 1
            else:
                new = Transpiler.get_identifier(float_count)
                float_count += 1
            self.rename_identifier(f"__{identifier}", new)

    @staticmethod
    def get_identifier(i):
        result = chr(i % 26 + 65) + str(int(i/26))
        return result
