"""
Module Description: Decorators for authentication, timing a function, logging and allowing function to run on odd second
Author: Shilpaj Bhalerao
Date: Jun 27, 2021
"""
import types
from typing import Union


# Decorator that allows to run a function only at odd seconds, else prints out "We're even!"
def odd_it(fn: types.FunctionType) -> "inner: types.FunctionType":
    """
    Decorators to run the function only on odd seconds
    Use `@odd_it` above the function to use this decorator
    :param fn: The function that needs to be executed on odd seconds
    :return: Closure
    """
    from datetime import datetime, timezone
    from functools import wraps

    @wraps(fn)
    def inner(*args, **kwargs) -> "function execution output/str":
        """
        Inner function of a closure
        :param args: arguments of the input function
        :param kwargs: keypoint arguments of the input function
        :return: result
        """
        dt = datetime.now()
        if not dt.second % 2 == 0:
            result = fn(*args, **kwargs)
            print(f'Output of Function "{fn.__name__}" called at {datetime.now(timezone.utc)} is {result}')
            return result
        else:
            print("We're even!")
    return inner


# The same logger that we coded in the class
# it will be tested against a function that will be sent 2 parameters, and 
# it would return some random string. 
def logger(fn: types.FunctionType) -> "closure: types.FunctionType":
    """
    Decorator to log the function call information.
    Use `@logged` above the function to use this decorator
    :param fn: Function which is decorated
    :type fn: function
    :return: Inner function of the decorator
    """
    from time import perf_counter
    from datetime import datetime, timezone
    from functools import wraps
    count = 0

    @wraps(fn)
    def inner(*args, **kwargs) -> "function output and function logs":
        """
        Inner function of the decorator which handles the logical part of data logging
        :param args: arguments passed to the function
        :param kwargs: keyword arguments passed to the function
        :return: Output of the function executed with the passed arguments
        """
        nonlocal count
        count += 1
        run_dt = datetime.now(timezone.utc)
        start = perf_counter()
        result = fn(*args, **kwargs)
        elapsed = perf_counter() - start

        args_ = [str(a) for a in args]
        kwargs_ = [f'{k} = {v}' for k, v in kwargs.items()]
        all_args = args_ + kwargs_
        args_str = ','.join(all_args)
        print(f'Function name: {fn.__name__} '
                f'\nFunction description: {fn.__doc__} '
                f'\nFunction annotations: {fn.__annotations__} '
                f'\nFunction arguments: {args_str} '
                f'\nFunction called at: {run_dt} '
                f'\nFunction called for the {count} times '
                f'\nExecution time: {elapsed: .9f} s')
        return result
    return inner


# start with a decorator_factory that takes an argument one of these strings, 
# high, mid, low or no
# then write the decorator that has 4 free variables
# based on the argument set by the factory call, give access to 4, 3, 2 or 1 arguments
# to the function being decorated from var1, var2, var3, var4
# YOU CAN ONLY REPLACE "#potentially missing code" LINES WITH MULTIPLE LINES BELOW
# KEEP THE REST OF THE CODE SAME
def decorator_factory(access: str) -> "decorator: types.FunctionType":
    """
    Decorator factory to intake `access_level` and returns data based on the access level
    :param access: Privilege Access
    :return: Decorator
    """
    # Generate name, email, date of birth and age of a person
    name = "Dan Gates"
    email = "dan.gates@gmail.com"
    dob = "Jun 30, 2000"
    age = 21

    # Defined data for each level of privilege
    privilege = {
        'high': [name, email, age, dob],
        'mid': [name, email, age],
        'low': [name, email],
        'no': [name],
    }

    def dec(fn: types.FunctionType) -> "inner: types.FunctionType":
        """
        Decorator function to intake function
        :param fn: Function to be decorated
        :return: Inner function of the decorator
        """
        from functools import wraps

        @wraps(fn)
        def inner(*args, **kwargs) -> Union[str, list]:
            """
            Inner function of decorator
            :param args: arguments of a function
            :param kwargs: keyword arguments of a function
            :return: output of function based on access level
            """
            if access in privilege:
                # Prints information based on privilege access
                print(f'Information: {privilege[access]}')
                fn(*args, **kwargs)
                return privilege[access]
            else:
                fn(*args, **kwargs)
                return "Improper access keyword set"

        return inner
    return dec


# The authenticate function. Start with a dec_factory that sets the password. It's inner
# will not be called with "password", *args, **kwargs on the fn
def authenticate(set_password: str) -> "decorator: types.FunctionType":
    """
    Decorator factory to accept the `password` argument and returns result if authenticated
    Use `@authenticate(password)` above the function to use this decorator
    :param set_password: Password(String) to use this function
    :return: Decorator for authentication
    """
    acceptable_password = set_password

    def dec(fn: types.FunctionType):
        """
        Decorator to check the authentication of a function
        :param fn: Function to be authenticated
        :return: Inner function of the decorator
        """
        from functools import wraps

        @wraps(fn)
        def inner(*args, **kwargs):
            """
            Inner function of the decorator
            :param args: arguments
            :param kwargs: keyword arguments
            :return: output of the function if correct password is entered
            """
            for key, value in kwargs.items():
                if key == "password":
                    return fn() if value == acceptable_password else "Wrong Password"

            for arg in args:
                if arg == acceptable_password:
                    return fn()
                return "Wrong Password"
            else:
                raise TypeError("Wrong password")
        return inner
    return dec


# The timing function
def timed(reps: int) -> "decorator: types.FunctionType":
    """
    Decorator factory to calculate the average elapsed time over `reps_number` of repetition
    Use `@timeit_` above the function to use this decorator
    :param reps: Number of times function is executed to calculate average
    :return: Decorator
    """
    def dec(fn: types.FunctionType) -> "closures: types.FunctionType":
        """
        Decorator to check execution time of a function
        :param fn: Function to be decorated
        :return: Inner function of the decorator
        """
        from time import perf_counter
        from functools import wraps
        from operator import truediv

        @wraps(fn)
        def inner(*args, **kwargs) -> "function output and average execution time":
            """
            Inner function of a decorator to calculate execution time
            :param args: arguments
            :param kwargs: keyword arguments
            :return: output of the function
            """
            total_time = 0
            for num in range(reps):
                start = perf_counter()
                fn(*args, **kwargs)
                end = perf_counter()
                elapsed = end - start
                total_time += elapsed
            avg_time = truediv(total_time, reps)
            print(f'Function {fn.__name__} took {avg_time} seconds over {reps} number of execution')
            return fn(*args, **kwargs)
        return inner
    return dec

