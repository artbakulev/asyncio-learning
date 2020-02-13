import asyncio

"""Эквивалентные функции, но поддержка первых будет убрана в Python 3.10, 
не стоит использовать"""


async def stuff():
    return (i for i in range(10))


@asyncio.coroutine
def py34_coro():
    """Generator-based coroutine, older syntax"""
    yield from stuff()


async def py35_coro():
    """Native coroutine, modern syntax"""
    await stuff()
