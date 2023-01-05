import functools


def compare(a, b) -> int:
    if isinstance(a, int) and isinstance(b, int):
        return a - b
    elif isinstance(a, list) and isinstance(b, list):
        for i in range(max(len(a), len(b))):
            if i >= len(a):
                return -1

            if i >= len(b):
                return 1

            if compare(a[i], b[i]) < 0:
                return -1

            if compare(a[i], b[i]) > 0:
                return 1

        return 0
    elif isinstance(a, int):
        return compare([a], b)
    else:
        return compare(a, [b])


with open('input.txt') as f:
    pairs = f.read().split('\n\n')[:-1]

packets = []

for i, pair in enumerate(pairs):
    first, second = map(eval, pair.split('\n'))
    packets.append(first)
    packets.append(second)

divider1 = [[2]]
divider2 = [[6]]

packets.append(divider1)
packets.append(divider2)

sorted_packets = sorted(packets, key=functools.cmp_to_key(compare))

print((sorted_packets.index(divider1) + 1) * (sorted_packets.index(divider2) + 1))
