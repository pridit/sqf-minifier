#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Minifies an SQF file."""
from pathlib import Path
from re import sub, compile, DOTALL, MULTILINE
import sre_constants

INLINE_COMMENT = compile('//+[^\n]+')
BLOCK_COMMENT = compile('/\*.*?\*/', DOTALL)
STRIP_REGEX = compile(r"(?:\/\*(?:(?!\*\/)(?:.|\n))*\*\/\n|\ {2,}|\t|^\n|\ *$|\ *\/\/[^\n]*\n)", MULTILINE)

def load_code(path_or_code: (Path, str)):
    """If passed a file path, loads code from that file. Else, returns its input."""

    if Path(path_or_code).exists():
        with open(path_or_code) as f:
            return f.read()

    return path_or_code
    
def strip(text: str) -> str:
    """Removes block quotes, comments, whitespace, indentation."""
    text = STRIP_REGEX.sub('', text).replace('\n\n', '\n')
    return text

def minify_file(file_in: (Path, str), file_out: (Path, str, bool, None) = False) -> str:
    """Minifies an SQF file, optionally outputting minified text to a file."""
    file_in = Path(file_in)

    if file_out is None:
        file_out = file_in.parent / f"{file_in.stem}-min{file_in.suffix}"

    with open(file_in) as f:
        text = f.read()

    text = strip(text)
    
    output = ''
    for line in text.splitlines():
        if line[:1] == '#':
            output += f'\n{line}\n'
        else:
            output += line
    
    if output[:1] == '\n':
        output = output[1:]
    
    if file_out:
        with open(file_out, 'w') as f:
            f.write(output)

    return output

if __name__ == '__main__':
    from sys import argv

    def main(arguments: dict, do_print: bool = False):
        try:
            text = minify_file(**arguments)
            if do_print:
                # print(len(text))
                print(text)
        except FileNotFoundError:
            print(f"Cannot find file: \"{argv[1]}\"")

    if len(argv) == 3:
        args = {'file_in': argv[1], 'file_out': argv[2]}
        do_print = False
    elif len(argv) == 2:
        args = {'file_in': argv[1]}
        do_print = True
    else:
        print('minify.py by inimitable\nMinifies an SQF source file.\n\nUsage:\n\tminify.py filename_in [filename_out]')
        quit()

    main(args, do_print)