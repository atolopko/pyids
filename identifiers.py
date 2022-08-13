from os import PathLike
import sys

from symtable import symtable, SymbolTable, Function
from typing import Tuple


def parse_identifiers(source_file: PathLike):
    with open(source_file) as f:
        st = symtable(f.read(), str(source_file), 'exec')
    walk(st)


def print_attributes(st: SymbolTable, level, *attrs):
    indent = "  " * (level + 1)
    for a in attrs:
        val = eval(f"st.get_{a}()")
        if isinstance(val, Tuple):
            val = ' '.join(val)
        print(f"{indent}{a}: {val}")


def walk(st: SymbolTable, level: int = 0) -> None:
    indent = "  " * level
    print(f"{indent}- {st.get_name()}")
    print_attributes(st, level, "type")
    if isinstance(st, Function):
        f = st
        print_attributes(st, level, 'parameters', 'locals', 'nonlocals')
    for c in st.get_children():
        walk(c, level + 1)


if __name__ == '__main__':
    parse_identifiers(sys.argv[1])
