import sys
from collections import defaultdict, namedtuple
from os import PathLike
from pprint import pp
from symtable import symtable, SymbolTable
from typing import List, Dict, Tuple

import os

from glob import glob

Category = str
Namespace = str
Name = str
Identifier = namedtuple('Identifier', ['namespace', 'name'])
Identifiers = Dict[Category, List[Identifier]]


def parse_identifiers(path: PathLike) -> Identifiers:
    if os.path.isdir(path):
        files = glob(f"{path}/**/*.py", recursive=True)
    else:
        files = [path]

    identifiers = defaultdict(list)
    for fn in files:
        with open(fn) as f:
            st = symtable(f.read(), str(path), 'exec')
            collect(st, '', identifiers)

    return identifiers


def collect(st: SymbolTable, namespace: str = '',
            identifiers: Identifiers = defaultdict(list)) -> Identifiers:

    identifier = Identifier(namespace, st.get_name())
    if st.get_type() == 'function':
        identifiers['fns'].append(identifier)
    if st.get_type() == 'class':
        identifiers['classes'].append(identifier)
    if st.get_type() == 'module':
        identifiers['modules'].append(identifier)

    namespace += f"{st.get_name()}."

    for s in st.get_symbols():
        if s.is_namespace():
            continue

        identifier = Identifier(namespace, s.get_name())

        if s.is_parameter():
            identifiers['fn_params'].append(identifier)
        elif s.is_local():
            if st.get_type() == 'function':
                identifiers['fn_locals'].append(identifier)
            elif st.get_type() == 'class':
                identifiers['cls_locals'].append(identifier)
            elif st.get_type() == 'module':
                identifiers['mod_locals'].append(identifier)
        elif s.is_global():
            identifiers['globals'].append(identifier)

    # recurse
    for c in st.get_children():
        collect(c, namespace, identifiers)


if __name__ == '__main__':
    pp(parse_identifiers(sys.argv[1]))
