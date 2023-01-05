def compare(a, b) -> int:
    if isinstance(a, int) and isinstance(b, int):
        return b - a
    elif isinstance(a, list) and isinstance(b, list):
        for i in range(max(len(a), len(b))):
            if i >= len(a):
                return 1

            if i >= len(b):
                return -1

            if compare(a[i], b[i]) > 0:
                return 1

            if compare(a[i], b[i]) < 0:
                return -1

        return 0
    elif isinstance(a, int):
        return compare([a], b)
    else:
        return compare(a, [b])


with open('input.txt') as f:
    pairs = f.read().split('\n\n')[:-1]

result = 0

for i, pair in enumerate(pairs):
    first, second = map(eval, pair.split('\n'))
    # print(first)
    # print(second)

    if compare(first, second) >= 0:
        result += i + 1

print(result)
