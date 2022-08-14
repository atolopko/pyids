from identifiers import package_and_module_names, find_relative_source_files


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
