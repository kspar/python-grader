import os
from .utils import read_code, setDescription
from functools import wraps

def test_decorator(decorator):
    @wraps(decorator)
    def _inner(f):
        if isinstance(f, list) or isinstance(f, tuple):
            return tuple(decorator(func) for func in f)
        else:
            return decorator(f)
    return _inner


@test_decorator
def set_description(d):
    def inner(f):
        setDescription(f, d)
        return f
    return inner


## File creation, deletion hooks
def create_file(filename, contents=""):
    """ Hook for creating files
        Example usage:

        @grader.test
        @grader.before_test(create_file('hello.txt', 'Hello world!'))
        @grader.after_test(delete_file('hello.txt'))
        def hook_test(m):
            with open('hello.txt') as file:
                txt = file.read()
                # ...
    """
    import collections
    if isinstance(contents, collections.Iterable) and not isinstance(contents, str):
        contents = "\n".join(map(str, contents))

    def _inner(info):
        with open(filename, "w") as f:
            f.write(contents)

    return _inner


def delete_file(filename):
    """ Hook for deleting files
        Example usage:

        @grader.test
        @grader.before_test(create_file('hello.txt', 'Hello world!'))
        @grader.after_test(delete_file('hello.txt'))
        def hook_test(m):
            with open('hello.txt') as file:
                txt = file.read()
                # ...
    """

    def _inner(result):
        try:
            os.remove(filename)
        except:
            pass

    return _inner


def create_temporary_file(filename, contents=""):
    """ Decorator for constructing a file which is available
        during a single test and is deleted afterwards.

        Example usage:
        @grader.test
        @create_temporary_file('hello.txt', 'Hello world!')
        def hook_test(m):
            with open('hello.txt') as file:
                txt = file.read()
        """
    from grader.core import before_test, after_test

    def _inner(test_function):
        before_test(create_file(filename, contents))(test_function)
        after_test(delete_file(filename))(test_function)
        return test_function
    return _inner


def add_value(value_name, value_or_fn):
    """ Post-test hook which as the value or the result of evaluating function on
        result to the test result dict.

        Example usage:
        @test
        @after_test(add_value("grade", 7))
        def graded_testcase(m):
            # ...
        """
    def _inner(result):
        value = value_or_fn
        if hasattr(value, '__call__'):
            value = value_or_fn(result)
        result[value_name] = value
    return _inner


def get_module_AST(path):
    import ast
    # encoding-safe open
    code = read_code(path)
    return ast.parse(code)


@test_decorator
def expose_ast(test_function):
    """ Pre-test hook for exposing the ast of the solution module
        as an argument to the tester. 

        Example usage:

        @grader.test
        @grader.expose_ast
        def ast_test(m, AST):
            # ...
    """
    import ast
    from grader.core import before_test

    def _hook(info):
        code = read_code(info["solution_path"])
        # add the solutions AST as a named argument to the test function
        info["extra_kwargs"]["AST"] = ast.parse(code)
    # add function _hook as a pre-hook to test_function
    return before_test(_hook)(test_function)
