# pyids
Parse identifiers from Python source code files. Recursively processes a directory. 

Uses [symtable](https://docs.python.org/3/library/symtable.html#) library to parse out identifiers, grouped by class names, function names, variable names, and globals. Each identifier is fully qualified by its package, module, and "namespace" (for nested classes and functions).

The resultant data structure is convenient for downstream analysis of identifier naming strategies used within a Python program.
