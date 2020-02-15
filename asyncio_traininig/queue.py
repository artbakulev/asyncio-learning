import asyncio
import random
import time
import weakref

import faker

WORKING_TIME = 30

MIN_ORDER_NUMBER = 1
MAX_ORDER_NUMBER = 10

WORKERS_NUMBER = 5
MIN_CLIENTS_IN_TIME = 5
MAX_CLIENTS_IN_TIME = 5

MENU = {
    '6 nuggets': 98,
    '9 nuggets': 120,
    'big mac': 130,
    'cheeseburger': 30,
    'latte': 109,
    'double espresso': 100,
}

Faker = faker.Faker()


class Order:
    _orders = set()

    @classmethod
    def get_new_order_number(cls):
        return len(cls._orders)

    def __init__(self):
        self.products_names = []
        self.product_prices = []
        self.order_number = Order.get_new_order_number()
        self._orders.add(weakref.ref(self))

    def add(self, product_name, product_price):
        self.products_names.append(product_name)
        self.product_prices.append(product_price)

    async def cook(self):
        cooking_time = len(self.products_names) / 2
        await asyncio.sleep(cooking_time)
        print(f'Order {self.order_number} was cooked. '
              f'Cooking time: {cooking_time}')

    @classmethod
    def get_instance_by_order_num(cls, order_number):
        for ref in cls._orders:
            obj: Order = ref()
            if obj is None:
                continue
            if obj.order_number == order_number:
                return obj
        return None


class Client:
    def __init__(self, name, macdonalds):
        self.name = name
        self.order = None
        self.macdonalds = macdonalds

    async def make_order(self):
        time_for_thinking = random.randint(0, 5)
        await asyncio.sleep(time_for_thinking)
        self.order = generate_order()
        await self.macdonalds.order_queue.put(self.order.order_number)
        print(f'Client {self.name}  made order  '
              f'with number {self.order.order_number} '
              f'for {time_for_thinking}s')
        return self.order


class Worker:
    def __init__(self, macdonalds):
        self.macdonalds = macdonalds
        self.name = Faker.name()
        print(f'New worker {self.name}')

    async def cook_order(self):
        while True:
            order_number = await self.macdonalds.order_queue.get()
            print(f'Worker {self.name} took order with number {order_number}')
            order = Order.get_instance_by_order_num(order_number)
            if order is None:
                raise Exception(f'Order with number {order_number}  not found')
            await order.cook()
            self.macdonalds.order_queue.task_done()
            print(f'Worker {self.name} cooked order with number {order_number}')


class Macdonalds:
    """Imitate macdonalds working"""

    def __init__(self):
        self.clients = []
        print('New macdonalds was created')
        self.order_queue = None

    def add_new_client(self):
        client = Client(Faker.name(), self)
        print(f'New client {client.name}')
        self.clients.append(client)

    async def run(self):
        # Важно объявить очередь в той корутине откуда она будет вызываться
        # Изначально объявил при инстанцировании Macdonalds и все ломалось
        self.order_queue: asyncio.Queue = asyncio.Queue()
        workers = [asyncio.create_task(worker.cook_order())
                   for worker in mac_workers]
        clients_count = random.randint(MIN_CLIENTS_IN_TIME,
                                       MAX_CLIENTS_IN_TIME)

        for j in range(clients_count):
            self.add_new_client()

        orders = [asyncio.create_task(client.make_order())
                  for client in self.clients]
        await asyncio.gather(*orders)
        await self.order_queue.join()
        for worker in workers:
            worker.cancel()


def generate_order():
    order_items_number = random.randint(MIN_ORDER_NUMBER, MAX_ORDER_NUMBER)
    order = Order()
    for i in range(order_items_number):
        product_name = random.choice(list(MENU.keys()))
        product_price = MENU[product_name]
        order.add(product_name, product_price)
    return order


async def main(macdonalds):
    await macdonalds.run()


if __name__ == '__main__':
    mac = Macdonalds()
    mac_workers = [Worker(mac) for i in range(WORKERS_NUMBER)]
    start = time.perf_counter()
    asyncio.run(main(mac))
    delta = time.perf_counter() - start
    print(f'Execution time is {delta}')
