import asyncio
import time
import hashlib

'''Хэширующий конвейнер с использованием цепей корутин'''

LINES = ['apple', 'orange', 'melon', 'strawberry', 'banana', ]


def prepare_line(line) -> str:
    try:
        hash_hex = line.hexdigest()
        return str(hash_hex)
    except AttributeError:
        return str(line)


async def md5(line):
    line = prepare_line(line)
    start = time.perf_counter()

    # imitation of CPU-bound task
    # do not forget to use asyncio.sleep instead of time.sleep
    await asyncio.sleep(len(line) / 5 + 2)
    delta = time.perf_counter() - start
    print(f'Time of execution md5 with {line} is {delta}')
    return hashlib.md5(line.encode())


async def sha1(line):
    line = prepare_line(line)
    start = time.perf_counter()
    await asyncio.sleep(len(line) / 5)
    delta = time.perf_counter() - start
    print(f'Time of execution sha1 with {line} is {delta}')
    return hashlib.sha1(line.encode())


async def chain(i, line):
    hashed_line = await md5(line)
    hashed_line = await sha1(hashed_line)
    print(f'{i} chain. {str(hashed_line)}')


async def main(lines):
    await asyncio.gather(*(chain(i, line) for i, line in enumerate(lines)))


if __name__ == '__main__':
    main_start = time.perf_counter()
    asyncio.run(main(LINES))
    main_delta = time.perf_counter() - main_start
    print(f'Time of execution: {main_delta}s')
