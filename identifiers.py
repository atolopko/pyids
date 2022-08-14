import sys
from collections import defaultdict
from os import PathLike
from pprint import pp
from symtable import symtable, SymbolTable
from typing import List, Dict

Identifiers = Dict[str, List[str]]


def parse_identifiers(source_file: PathLike) -> Identifiers:
    with open(source_file) as f:
        st = symtable(f.read(), str(source_file), 'exec')
    return collect(st)


def collect(st: SymbolTable, namespace: str = '') -> Identifiers:
    identifiers = defaultdict(list)

    sym_name = namespace + st.get_name()
    if st.get_type() == 'function':
        identifiers['fns'].append(sym_name)
    if st.get_type() == 'class':
        identifiers['classes'].append(sym_name)
    if st.get_type() == 'module':
        identifiers['modules'].append(sym_name)

    namespace += f"{st.get_name()}."

    for s in st.get_symbols():
        if s.is_namespace():
            continue

        sym_name = namespace + s.get_name()

        if s.is_parameter():
            identifiers['fn_params'].append(sym_name)
        elif s.is_local():
            if st.get_type() == 'function':
                identifiers['fn_locals'].append(sym_name)
            elif st.get_type() == 'class':
                identifiers['cls_locals'].append(sym_name)
            elif st.get_type() == 'module':
                identifiers['mod_locals'].append(sym_name)
        elif s.is_global():
            identifiers['globals'].append(sym_name)

    # recurse
    for c in st.get_children():
        nested_identifiers = collect(c, namespace)
        for k in nested_identifiers.keys():
            identifiers[k].extend(nested_identifiers[k])

    return identifiers


if __name__ == '__main__':
    pp(parse_identifiers(sys.argv[1]))
