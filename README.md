[toc]

Name: Shilpaj Bhalerao

Email Address: shilpajbhalerao@gmail.com



## Changes to `test_session8.py`

1. ```python
   import re
   ```

2. ```python
   from io import StringIO
   ```

3. In `test_indentations()` and `test_function_name_had_cap_letter()` replaced `session4` by `session8`

4. Replaced `from session8 import *` with `import session8`  to remove execution error from `test_indentations()` and `test_function_name_had_cap_letter()`

5. All the decorators are called with prefix  `@session.` like `@session8.log`

   

---



# Decorators

- Decorator extends/augments the functionality of a function
- They can be executed in two ways:
    - `@ operator`- Type `@decorator_name` above the function definition
    - `function_name = decorator_name(function_name)`
- In general, a decorator function takes a function as an argument and returns a closure
- `wraps(fn)` is usually used to decorate the closure for proper referencing function details
- This closure usually accepts any combination of parameters by using `*args` and `**kwargs` arguments
- This closure executes some functional code(with/without free variables) and returns the output of the function
- Below are applications of Decorators

### Odd second executor
```python
def odd_it(fn: types.FunctionType) -> "inner":
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
```

### Logger
```python
def logger(fn: types.FunctionType) -> "closure":
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
```



---



# Decorator Factory

- Decorator factory is used to pass arguments to the decorator

- Integer factory is nothing but the function which takes in only integer arguments

  ```python
  # Integer factory
  def function_name(a: int, b: int):
  	return a + b
  ```

- Similarly, decorator factory is nothing but a function encapsulating a decorator which can pass arguments to decorator

- As mentioned in the above section, there are two ways in which we can call decorators - 

  - Using `@decorator` and
  - Using `function_name = decorator_name(function_name)`

- Consider a following decorator function

  ```python
  def decorator(fn):
      def inner(*args, **kwargs):
          return fn(*args, **kwargs)
      return inner
  ```

  

- In order to pass argument to above decorator, we can use following approach:

  - **Function call method**

    - Modify the decorator to accept the decorator

    ```python
    def decorator(fn, arg):
        def inner(*args, **kwargs):
            # Access the argument here
            print(arg)
            return fn(*args, **kwargs)
        return inner
    
    function_name = decorator(function_name, arg=10)
    ```

     

  - **`@decorator method`**

    - The `@decorator` is equivalent to `function_name = decorator(function_name)`
    - So, passing an argument won't be possible unless decorator definition is changed
    - So, an encapsulating function (known as **decorator factory**) is added which returns the decorator
    - Following are modifications needed to code for passing an argument

    ```python
    def decorator(arg):                       # This is decorator factory
        def dec(fn):                          # This is decorator 
            def inner(*args, **kwargs):       # This is closure
                # Access the argument here
                print(arg)
                return fn(*args, **kwargs)
            return inner
        return dec
    
    @decorator(arg=10)
    def function_name():
        pass
    ```

- Below mentioned are the applications of the decorator factory

  

### Timeit

- This decorator factory can be used to calculate average elapsed time for a function over a number of repetitions
- The argument `reps_number` can be passed to check the average over those many iterations
- To use this decorator,  write `@timeit_(reps_number=10)` over the function you want to decorate

```python
def timed(reps: int) -> "decorator":
    """
    Decorator factory to calculate the average elapsed time over `reps_number` of repetition
    Use `@timeit_` above the function to use this decorator
    :param reps: Number of times function is executed to calculate average
    :return: Decorator
    """
    def dec(fn: types.FunctionType) -> "closures":
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
```



### Authentication

- This decorator returns the output of the function only if correct password is passed in the decorator
- To use this decorator,  write `@authenticate(password)` over the function you want to decorate

```python
def authenticate(set_password: str) -> "decorator":
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
```



### Privilege Access

- This decorator provides you data based on the privilege access provided as an argument

  | Access Level | Data Available                  |
  | ------------ | ------------------------------- |
  | `high`       | name, email, age, date of birth |
  | `mid`        | name, email, age                |
  | `low`        | name, email                     |
  | `no`         | name                            |

- To use this decorator, uses `@privilege_access(access_level="high")` above the function to be decorated

```python
def decorator_factory(access: str) -> "decorator":
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

    def dec(fn: types.FunctionType) -> "inner":
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
```



---



# Decorating Classes

- Till now, we have seen that decorators can be used to decorate functions

- Decorators can also be used for decorating classes

- Following is a decorator defined to to print debug info of classes

  ```python
  def debug_info(cls):
      def inner(self):
          results = []
          results.append('time: {0}'.format(datetime.now(timezone.utc)))
          results.append('class: {0}'.format(self.__class__.__name__))
          results.append('id: {0}'.format(hex(id(self))))
          
          if vars(self):
              for k, v in vars(self).items():
                  results.append('{0}: {1}'.format(k, v))
          
          # A more Pythonic way to do this would be:
          #if vars(self):
          #    results.extend('{0}: {1}'.format(k, v) 
          #                   for k, v in vars(self).items())
          
          return results
      cls.debug = inner
      return cls
  ```

- Application example

  ```python
  @debug_info
  class Person:
      def __init__(self, name, birth_year):
          self.name = name
          self.birth_year = birth_year
          
      def say_hi():
          return 'Hello there!'
  ```

  ```python
  p1 = Person('John', 1939)
  p1.debug()
  ```

  ```shell
  Output: 
  ['time: 2021-06-26 07:50:19.632075+00:00',
   'class: Person',
   'id: 0x7f0e40bab9a0',
   'name: John',
   'birth_year: 1939']
  ```

- Here, the decorator has added another method named `debug()` to the class `Person` which is used to print all the debug information about the class

- Similarly, we can add multiple methods as separate decorators to print out relevant information



---

# Classes as Decorators

- Till now, we have used nested functions as a decorators

- But we can also use class as a decorator by overriding the `__call__` method

- Following example shows class `MyClass` used as a decorator

  ```python
  class MyClass:
      def __init__(self, a, b):
          self.a = a
          self.b = b
          
      def __call__(self, fn):  # Here fn is the function to be decorated
          def inner(*args, **kwargs):
              print('MyClass instance called: a={0}, b={1}'.format(self.a, self.b))
              return fn(*args, **kwargs)
          return inner
  ```

  ```python
  @MyClass(10, 20)
  def my_func(s):
      print('Hello {0}!'.format(s))
  ```

  ```python
  my_func('Python')
  ```

  ```
  Output:
  MyClass instance called: a=10, b=20
  Hello Python!
  ```

- Similarly, we can add multiple methods to the class where each method is a decorator

- This can be used to apply multiple decorators with different instances of a class(i.e. with different values of class variable)



---



# Class Ordering

- When we define a class in Python, all the dunder methods are not initialized with the class

- We need to define these methods. Some useful methods are - `__le__`, `__gt__`, `__ge__`, etc

- Instead of writing these methods to each class, we can use a decorator to do so

- Following example show a decorator named `ordering_` decorates a class

  ```python
  def ordering_(cls):
      if '__eq__' in dir(cls) and '__lt__' in dir(cls):
          cls.__le__ = lambda self, other: self < other or self == other
          cls.__gt__ = lambda self, other: not(self < other) and not (self == other)
          cls.__ge__ = lambda self, other: not (self < other)
      return cls
  ```

   ```python
   @ordering_
  class Point:
      def __init__(self, x, y):
          self.x = x
          self.y = y
          
      def __abs__(self):
          return sqrt(self.x**2 + self.y**2)
      
      def __eq__(self, other):
          if isinstance(other, Point):
              return self.x == other.x and self.y == other.y
          else:
              return NotImplemented
              
      def __lt__(self, other):
          if isinstance(other, Point):
              return abs(self) < abs(other)
          else:
              return NotImplemented
          
      def __repr__(self):
          return '{0}({1},{2})'.format(self.__class__, self.x, self.y)
      
      def invert_coordinates(self):
          """
          Method to invert the coordinates of a point
          """
          self.x = self.y, self.y = self.x
          
      def is_origin(self) -> bool:
          """
          Method to return bool True if point is origin else False
          """
          if self.x == 0 and self.y == 0:
              return True
          return False
   ```

- Now, we can use the methods `__le__`, `__gt__`, `__ge__` for class `Grade`

- This decorator does not includes all the dunder function associated with the class

- Python has a built-in decorator to include all these dunder methods

- Following example shows how to implement all the dunder methods by using built-in decorators

  ```python
  from functools import total_ordering
  
  @total_ordering
  class Grade:
      def __init__(self, score, max_score):
          self.score = score
          self.max_score = max_score
          self.score_percent = round(score / max_score * 100)
       
      def __repr__(self):
          return 'Grade({0}, {1})'.format(self.score, self.max_score)
      
      def __eq__(self, other):
          if isinstance(other, Grade):
              return self.score_percent == other.score_percent
          else:
              return NotImplemented
      
      def __lt__(self, other):
          if isinstance(other, Grade):
              return self.score_percent < other.score_percent
          else:
              return NotImplemented
  ```

  

---



# Single Dispatch

- In python, we cannot overload a normal function twice for different behavior base on the arguments. For example:

  ```python
  def foo(number:int ):
      print('it is a integer')
      
  def foo(number: float):
      print('it is a float')
  ```

  `foo(1)` will return `it is a float`

-  The definition simply get replaced by the second definition. However, with `singledispatch`, you can define the function behavior base on the type of the argument.

  ```python
  from functools import singledispatch
  
  @singledispatch
  def foo(number):
      print(f'{type(number)}, {number}')
  ```

  Now, `foo(1)` will return `<class 'int'>, 1` and `foo(1.2)` will return `<class 'float'>, 1.2`

