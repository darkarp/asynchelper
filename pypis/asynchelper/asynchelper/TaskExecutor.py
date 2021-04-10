
import sys
import signal
import asyncio
from typing import Union, Iterable


def signal_handler(signal, frame):
    print('[-] Exiting...')
    sys.exit(0)


class TaskManager:

    def __init__(self, workers: int):
        self.semaphore = workers and asyncio.Semaphore(workers)
        self.tasks = set()

    async def _put(self, coro):
        if self.semaphore:
            await self.semaphore.acquire()
        task = asyncio.create_task(coro)
        task.add_done_callback(self._done)
        self.tasks.add(task)

    def _done(self, task):
        self.tasks.remove(task)
        if self.semaphore:
            self.semaphore.release()

    async def _join(self):
        await asyncio.gather(*self.tasks)

    async def __aenter__(self):
        return self

    def __aexit__(self, *args, **kwargs):
        return self._join()


async def forever(task: callable, args: Iterable = [], workers: Union[int, None] = 128) -> None:
    """Infinite loop for a task with arguments with a maximum limit of concurrent tasks.
    Terminates with CTRL + C (SIGINT)

    Args:
        task (callable): The asynchronous function to run
        args (Iterable, optional): Arguments for the task. Defaults to [].
        workers (int, optional): Maximum number of concurrent tasks. Defaults to 256.
    """
    async with TaskManager(workers=workers) as manager:
        while True:
            await manager._put(task(*args))


async def map(task_generator: Iterable[callable], workers: Union[int, None] = 128) -> None:
    """Schedules execution for an iterable of asynchronous functions, with a maximum limit of concurrent tasks.
    Terminates with CTRL + C (SIGINT)

    Args:
        task_generator (Iterable[callable]): An iterable of asynchronous functions, preferably a generator.
        workers (int, optional):  Maximum number of concurrent tasks. Defaults to 0.
    """
    async with TaskManager(workers=workers) as manager:
        for task in task_generator:
            await manager._put(task)

signal.signal(signal.SIGINT, signal_handler)
if __name__ == "__main__":
    pass
