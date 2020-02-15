"""Just for repeating"""
from itertools import cycle


def gen():
    yield from cycle((1, 2, 3, 4))


# j = 0
# for i in gen():
#     print(i)
#     j += 1
#     if j > 10:
#         break

g = gen()
print(g.__next__())
print(next(g))
