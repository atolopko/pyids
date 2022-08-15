from os.path import join

MY_CONST = 1

global1 = 1


def module_fn(fn_arg1, fn_arg2):
    fn_local1 = fn_arg1 + fn_arg2 + global1
    return fn_local1


class MyClassName:
    class_var = 1

    class NestedCls:
        def foo(self):
            return 1

    def class_fn(self, fn_arg1, fn_arg2):

        class NestedFnCls:
            def bar(self):
                return 1

        fn_local1 = self.class_var + fn_arg1 + fn_arg2
        return fn_local1


if __name__ == '__main__':
    mod_var1 = 1
    print(MyClassName().class_fn(mod_var1, 2))
    print(module_fn(mod_var1, 2))
