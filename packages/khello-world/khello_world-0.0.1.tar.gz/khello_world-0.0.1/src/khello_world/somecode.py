import random

def random_numbers(n, start=1, finish=1000):
    return [random.randint(start,finish) for i in range(n)]
