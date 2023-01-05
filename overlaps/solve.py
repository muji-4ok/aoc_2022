def range_in(a1: int, b1: int, a2: int, b2: int) -> bool:
    return a2 <= a1 and b1 <= b2


def any_range_in(a1: int, b1: int, a2: int, b2: int) -> bool:
    return range_in(a1, b1, a2, b2) or range_in(a2, b2, a1, b1)


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

result = 0

for line in lines:
    first, second = line.split(',')
    a1, b1 = map(int, first.split('-'))
    a2, b2 = map(int, second.split('-'))
    result += any_range_in(a1, b1, a2, b2)

print(result)

