asynchelper
===========

.. image:: https://img.shields.io/pypi/v/asynchelper.svg
    :target: https://pypi.python.org/pypi/asynchelper
    :alt: Latest PyPI version


Allows execution of unlimited number of asynchronous tasks while limiting the amount of active concurrent ones.

Usage
-----

There are only two functions (for now):  
 * `asynchelper.TaskExecutor.map(task_generator: Iterable[callable], workers: Union(int, None) = 128)`  
    * `task_generator` can be any iterable which holds (or generates) coroutines. 
    *  `workers` is the maximum limit of active tasks concurrently. `None` for no limit.
    * This will keep pushing tasks in the iterable until it's fully consumed.
 * `asynchelper.TaskExecutor.forever(task: callable, args: Iterable = [], workers: Union(int, None) = 128)`
    * `task` is an async funtion to create a couroutine from
    * `args` is an iterable of arguments to pass to `task`
    * `workers` is the maximum limit of active tasks concurrently. `None` for no limit
    * This will keep pushing the `task(*args)`, running them forever with a limit of `workers` active tasks at any moment.

-------

`asynchelper` was written by `Mario Nascimento <mario@whitehathacking.tech>`_.
