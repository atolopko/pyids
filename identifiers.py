import os
import sys
from collections import defaultdict, namedtuple
from glob import iglob
from pathlib import PurePath
from pprint import pp
from symtable import symtable, SymbolTable
from typing import Dict, Tuple, Iterable, Set

import builtins

BUILTINS = dir(builtins)

Category = str
Namespace = str
Name = str
Identifier = namedtuple('Identifier', ['package', 'module', 'namespace', 'name'])
Identifiers = Dict[Category, Set[Identifier]]


def package_and_module_names(src_file) -> Tuple[str, str]:
    module = PurePath(src_file).stem
    package = '.'.join(PurePath(src_file).parent.parts)
    return package, module


def parse_identifiers_from_files(root_path, source_files: Iterable[str]) -> Identifiers:
    identifiers = defaultdict(set)
    for fn in source_files:
        with open(os.path.join(root_path, fn)) as f:
            st = symtable(f.read(), fn, 'exec')
            pkg, module = package_and_module_names(fn)
            parse_identifiers(st, pkg, module, identifiers)

    return identifiers


def find_relative_source_files(path):
    if os.path.isdir(path):
        files = iglob(f"{path}/**/*.py", recursive=True)
    else:
        files = [path]

    return [str(PurePath(f).relative_to(path)) for f in files]


# TODO: Handle lambdas ("lambda")
# TODO: Handle list/dict comprehensions ("listcomp", "dictcomp")
def parse_identifiers(st: SymbolTable,
                      package: str,
                      module: str,
                      identifiers: Identifiers,
                      namespace=''):

    identifier = Identifier(package, module, namespace, st.get_name())
    if st.get_type() == 'function':
        identifiers['fns'].add(identifier)
    if st.get_type() == 'class':
        identifiers['classes'].add(identifier)
    if st.get_type() == 'module':
        identifiers['modules'].add(identifier)

    if st.get_name() != 'top':
        namespace += '.' if namespace else ''
        namespace += st.get_name()

    for s in st.get_symbols():
        if s.is_namespace():
            # must be a function or class, and this will be handled via recursion
            continue

        identifier = Identifier(package, module, namespace, s.get_name())

        if s.get_name() in BUILTINS:
            pass
        elif s.is_imported():
            pass
        elif st.get_type() == 'module':
            assert s.is_global()
            identifiers['globals'].add(identifier)
        elif st.get_type() == 'function':
            if s.is_parameter():
                identifiers['fn_params'].add(identifier)
            elif s.is_local():
                identifiers['fn_vars'].add(identifier)
        elif st.get_type() == 'class':
            if s.is_local():
                identifiers['cls_vars'].add(identifier)

    # recurse
    for c in st.get_children():
        parse_identifiers(c, package, module, identifiers, namespace)


if __name__ == '__main__':
    identifiers = parse_identifiers_from_files(sys.argv[1], find_relative_source_files(sys.argv[1]))
    pp(identifiers)
