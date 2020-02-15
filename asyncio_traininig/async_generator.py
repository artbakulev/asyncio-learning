import asyncio
import random


async def async_gen():
    i = 0
    while True:
        seconds = random.randint(0, 50) / 100
        await asyncio.sleep(seconds)
        print(f'waited for {seconds}')
        yield i
        i += 1
        if i > 10:
            break


def sync_gen():
    i = 0
    while True:
        seconds = random.randint(0, 50) / 100
        print(f'waited for {seconds}')
        yield i
        i += 1
        if i > 10:
            break


async def main():
    f = [i async for i in async_gen()]
    g = [i async for i in async_gen() if i % 2 == 0]
    sync_f = f = [i for i in sync_gen()]
    sync_g = [i for i in sync_gen() if i % 2 == 0]
    return f, g, sync_f, sync_g


if __name__ == '__main__':
    # Пока не понимаю в чем разница между async for и for
    f, g, sync_f, sync_g = asyncio.run(main())
    print(f)
    print(g)
    print(sync_f)
    print(sync_g)
