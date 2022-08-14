import sys
from collections import defaultdict, namedtuple
from os import PathLike
from pprint import pp
from symtable import symtable, SymbolTable
from typing import List, Dict, Tuple

Category = str
Namespace = str
Name = str
Identifier = namedtuple('Identifier', ['namespace', 'name'])
Identifiers = Dict[Category, List[Identifier]]


def parse_identifiers(source_file: PathLike) -> Identifiers:
    with open(source_file) as f:
        st = symtable(f.read(), str(source_file), 'exec')
    return collect(st)


def collect(st: SymbolTable, namespace: str = '') -> Identifiers:
    identifiers = defaultdict(list)

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
        nested_identifiers = collect(c, namespace)
        for k in nested_identifiers.keys():
            identifiers[k].extend(nested_identifiers[k])

    return identifiers


if __name__ == '__main__':
    pp(parse_identifiers(sys.argv[1]))
