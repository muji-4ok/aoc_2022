from dataclasses import dataclass
from typing import Callable
from functools import reduce

import operator


@dataclass
class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    test: Callable[[int], bool]
    true_monkey: int
    false_monkey: int
    inspections: int = 0


# monkeys = [
#     Monkey([79, 98], lambda x: x * 19, lambda x: x % 23 == 0, 2, 3),
#     Monkey([54, 65, 75, 74], lambda x: x + 6, lambda x: x % 19 == 0, 2, 0),
#     Monkey([79, 60, 97], lambda x: x * x, lambda x: x % 13 == 0, 1, 3),
#     Monkey([74], lambda x: x + 3, lambda x: x % 17 == 0, 0, 1),
# ]

monkeys = [
    Monkey([63, 57],
           lambda x: x * 11,
           lambda x: x % 7 == 0,
           6,
           2),
    Monkey([82, 66, 87, 78, 77, 92, 83],
           lambda x: x + 1,
           lambda x: x % 11 == 0,
           5,
           0),
    Monkey([97, 53, 53, 85, 58, 54],
           lambda x: x * 7,
           lambda x: x % 13 == 0,
           4,
           3),
    Monkey([50],
           lambda x: x + 3,
           lambda x: x % 3 == 0,
           1,
           7),
    Monkey([64, 69, 52, 65, 73],
           lambda x: x + 6,
           lambda x: x % 17 == 0,
           3,
           7),
    Monkey([57, 91, 65],
           lambda x: x + 5,
           lambda x: x % 2 == 0,
           0,
           6),
    Monkey([67, 91, 84, 78, 60, 69, 99, 83],
           lambda x: x * x,
           lambda x: x % 5 == 0,
           2,
           4),
    Monkey([58, 78, 69, 65],
           lambda x: x + 7,
           lambda x: x % 19 == 0,
           5,
           1),
]

for _ in range(20):
    for monkey in monkeys:
        for level in monkey.items:
            level = monkey.operation(level)
            level //= 3
            monkeys[monkey.true_monkey if monkey.test(level) else monkey.false_monkey].items.append(level)

        monkey.inspections += len(monkey.items)
        monkey.items.clear()

print(reduce(operator.mul, sorted([m.inspections for m in monkeys])[-2:]))

