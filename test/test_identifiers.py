from collections import defaultdict
from symtable import symtable

from pytest import fixture

from identifiers import package_and_module_names, find_relative_source_files, collect, Identifier


def test_find_source_files():
    assert find_relative_source_files('fixtures') == ['mod1.py', 'pkg1/mod2.py']


def test_package_and_modules_names__multilevel():
    pkg, mod = package_and_module_names('pkg1/pkg2/mod.py')
    assert pkg == 'pkg1.pkg2'
    assert mod == 'mod'


def test_package_and_modules_names__no_pkg():
    pkg, mod = package_and_module_names('mod.py')
    assert pkg == ''
    assert mod == 'mod'


@fixture
def mod1_symtable():
    with open('fixtures/mod1.py') as f:
        return symtable(f.read(), 'fixtures/mod1.py', 'exec')


def test_collect(mod1_symtable):
    identifiers = defaultdict(list)

    collect(mod1_symtable, '', 'mod1', identifiers)

    assert identifiers == {
        'classes': [Identifier(package='', module='mod1', namespace='', name='MyClassName'),
                    Identifier(package='', module='mod1', namespace='MyClassName', name='NestedCls'),
                    Identifier(package='', module='mod1', namespace='MyClassName.class_fn',
                               name='NestedFnCls')],
        'cls_locals': [
            Identifier(package='', module='mod1', namespace='MyClassName', name='class_var')],
        'fn_locals': [Identifier(package='', module='mod1', namespace='module_fn', name='fn_local1'),
                      Identifier(package='', module='mod1', namespace='MyClassName.class_fn',
                                 name='fn_local1')],
        'fn_params': [Identifier(package='', module='mod1', namespace='module_fn', name='fn_arg1'),
                      Identifier(package='', module='mod1', namespace='module_fn', name='fn_arg2'),
                      Identifier(package='', module='mod1', namespace='MyClassName.NestedCls.foo',
                                 name='self'),
                      Identifier(package='', module='mod1', namespace='MyClassName.class_fn',
                                 name='self'),
                      Identifier(package='', module='mod1', namespace='MyClassName.class_fn',
                                 name='fn_arg1'),
                      Identifier(package='', module='mod1', namespace='MyClassName.class_fn',
                                 name='fn_arg2'),
                      Identifier(package='', module='mod1',
                                 namespace='MyClassName.class_fn.NestedFnCls.bar', name='self')],
        'fns': [Identifier(package='', module='mod1', namespace='', name='module_fn'),
                Identifier(package='', module='mod1', namespace='MyClassName.NestedCls', name='foo'),
                Identifier(package='', module='mod1', namespace='MyClassName', name='class_fn'),
                Identifier(package='', module='mod1', namespace='MyClassName.class_fn.NestedFnCls',
                           name='bar')],
        'mod_locals': [Identifier(package='', module='mod1', namespace='', name='MY_CONST'),
                       Identifier(package='', module='mod1', namespace='', name='global1'),
                       Identifier(package='', module='mod1', namespace='', name='mod_var1')],
        'modules': [Identifier(package='', module='mod1', namespace='', name='top')]}
