import os
import sys
from collections import defaultdict, namedtuple
from glob import iglob
from pathlib import PurePath
from pprint import pp
from symtable import symtable, SymbolTable
from typing import List, Dict, Tuple, Iterable

Category = str
Namespace = str
Name = str
Identifier = namedtuple('Identifier', ['package', 'module', 'namespace', 'name'])
Identifiers = Dict[Category, List[Identifier]]


def package_and_module_names(src_file) -> Tuple[str, str]:
    module = PurePath(src_file).stem
    package = '.'.join(PurePath(src_file).parent.parts)
    return package, module


def parse_identifiers(root_path, source_files: Iterable[str]) -> Identifiers:
    identifiers = defaultdict(list)
    for fn in source_files:
        with open(os.path.join(root_path, fn)) as f:
            st = symtable(f.read(), fn, 'exec')
            pkg, module = package_and_module_names(fn)
            collect(st, pkg, module, identifiers)

    return identifiers


def find_relative_source_files(path):
    if os.path.isdir(path):
        files = iglob(f"{path}/**/*.py", recursive=True)
    else:
        files = [path]

    return [str(PurePath(f).relative_to(path)) for f in files]


def collect(st: SymbolTable,
            package: str,
            module: str,
            identifiers: Identifiers,
            namespace=''):

    identifier = Identifier(package, module, namespace, st.get_name())
    if st.get_type() == 'function':
        identifiers['fns'].append(identifier)
    if st.get_type() == 'class':
        identifiers['classes'].append(identifier)
    if st.get_type() == 'module':
        identifiers['modules'].append(identifier)

    if st.get_name() != 'top':
        namespace += '.' if namespace else ''
        namespace += st.get_name()

    for s in st.get_symbols():
        if s.is_namespace():
            # must be a function or class, and this will be handled via recursion
            continue

        identifier = Identifier(package, module, namespace, s.get_name())

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
        collect(c, package, module, identifiers, namespace)


# TODO: remove builtins:
# import builtins
# dir(builtins)
if __name__ == '__main__':
    pp(parse_identifiers(sys.argv[1],
                         find_relative_source_files(sys.argv[1])))
